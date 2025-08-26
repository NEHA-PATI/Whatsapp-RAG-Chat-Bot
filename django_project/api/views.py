import json
import os
import re
import traceback
from functools import wraps

import redis
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse
from .models import Complaint
from django_project import settings

CHAT_HISTORY_SIZE = 30

# Redis setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
assert OPENAI_API_KEY is not None

openai_client = OpenAI(api_key=settings.OPENAI.API_KEY)

SYSTEM_PROMPT = '''
You are a whatsapp chatbot who is designed to receive various types of complaints from the users.

You can receive complaints from people of Kalahandi district in Odisha state in India.

Try to classify the complaints into one of the following departments if possible:

1. Water department
2. Fire department
3. Sanitary department
4. Others

Do not accept complaints from other districts or states.

Try to gather all necessary pieces of information from the user which the corresponding field officer would need.
Make sure the key details are complete and comprehensible. For example, addresses shouldn't be incomplete.
Also collect the user's full name and address.
Ask your questions one by one.

Introduce yourself when a new conversation starts.

After all the information is received, report to usnameer all the pieces of information for their knowledge and prepare
a non-nested json format of the data. Write this json inside <json> </json> tags.
When you send the json tag, my code will save it in the db. So make sure you send it only once per complaint.
Generate the json only after user confirmation of the details.
This json is for internal use. Don't tell the user about the json.
Use these field names in the json full_name, complaint_message, department, user_address
converse with the user in english language.
'''


def twilio_error_handler(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception:
            traceback.print_exc()
            twilio_resp = MessagingResponse()
            twilio_resp.message("An internal error occurrec")
            return HttpResponse(str(twilio_resp), content_type='application/xml')

    return wrapper


def generate_text(messages):
    response = openai_client.chat.completions.create(
        model=settings.OPENAI.MODEL_NAME,
        messages=messages
    )
    print(response.model_dump_json())
    return response.choices[0].message.content


@csrf_exempt
@twilio_error_handler
def whatsapp_webhook(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=405)

    user_id = request.POST.get('From')  # format: whatsapp:+91XXXXXXXXXX
    message = request.POST.get('Body', '').strip()

    # remove the tag so that user cannot interfare with the code
    message.replace('<json>', 'REMOVED_JSON_TAG')
    print(request.POST)

    session_key = f"chat:{user_id}"

    # Check for new conversation
    # if is_new_conversation(message):
    #     print('new conversation')
    #     r.delete(session_key)
    # else:
    #     print('old conversation')

    # Load history or start new
    history = json.loads(redis_client.get(session_key) or "[]")

    # Append new user message
    history.append({"role": "user", "content": message})
    llm_messages = list()

    # insert system messages
    llm_messages.extend([
        {
            'role': 'system',
            'content': SYSTEM_PROMPT
        }
    ])
    llm_messages.extend(history)

    print(f'llm_messages: {json.dumps(llm_messages)}')
    reply = generate_text(llm_messages)

    # Append response to history
    history.append({"role": "assistant", "content": reply})

    if '<json>' in reply:
        JSON_REGEX = r"<json>(.*?)</json>"
        match = re.search(JSON_REGEX, reply, re.DOTALL)
        if match:
            complaint_json = match.group(1)
            complaint_json = json.loads(complaint_json.strip())

            complaint = Complaint(
                name=complaint_json.get('full_name', 'not-available'),
                user_phone_number=user_id.replace('whatsapp:', ''),
                user_address=complaint_json.get('user_address', 'not-available'),
                department=complaint_json.get('department', 'not-available'),
                complaint_message=complaint_json.get('complaint_message', 'not-available'),
                raw_conversation=json.dumps(history, indent=4),
                raw_complaint_json=json.dumps(complaint_json, indent=4),
            )
            complaint.save()
            reply = re.sub(JSON_REGEX, "\nTHE COMPLAINT HAS BEEN RECORDED\n", reply, flags=re.DOTALL)
        else:
            reply += "\nNo valid computer format complaint found. Could not save complaint."
    # Save back to Redis
    redis_client.set(session_key, json.dumps(history[-CHAT_HISTORY_SIZE:]), ex=3600)  # expire in 1 hour

    # Send WhatsApp response
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    print(f"reply: {reply}")
    return HttpResponse(str(twilio_resp), content_type='application/xml')

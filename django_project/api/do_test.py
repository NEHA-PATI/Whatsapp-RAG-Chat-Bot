import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import requests

default_message = """
I am Ghanshyam Agrawal.
I live at opp bhandar gharani temple, basti pada, dharamgarh, kalahandi, odisha.
The water pipe near my home has burst. There is minor leakage. No immediate risk. Same address.
Please register a complaint.
This is final. No confirmation needed.
"""

default_phone_number = '+918117014347'
phone_number = input(f"Enter the user phone number with country code (just enter for {default_phone_number}): ")
if not phone_number:
    print(f"Using default number: {default_phone_number}")
    phone_number = default_phone_number
phone_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')

while True:
    prompt = input("Enter the user message (enter blank for default): ")
    if not prompt:
        print("Sending default message")
        prompt = default_message
    payload = 'SmsMessageSid=SMf7cbe2cac02a991278c8c0f33d3e19cf&NumMedia=0&ProfileName=Ghanshyam+Agrawal&MessageType=text&SmsSid=SMf7cbe2cac02a991278c8c0f33d3e19cf&WaId=PHONE_NUMBER_PLACEHOLDER&SmsStatus=received&Body=BODY_PLACEHOLDER&To=whatsapp%3A%2B14155238886&NumSegments=1&ReferralNumMedia=0&MessageSid=SMf7cbe2cac02a991278c8c0f33d3e19cf&AccountSid=ACd71912c65babfe462ecf8d9840170c34&ChannelMetadata=%7B%22type%22%3A%22whatsapp%22%2C%22data%22%3A%7B%22context%22%3A%7B%22ProfileName%22%3A%22Ghanshyam+Agrawal%22%2C%22WaId%22%3A%22PHONE_NUMBER_PLACEHOLDER%22%7D%7D%7D&From=whatsapp%3A%2BPHONE_NUMBER_PLACEHOLDER&ApiVersion=2010-04-01'
    payload = payload.replace('PHONE_NUMBER_PLACEHOLDER', phone_number)
    payload = payload.replace('BODY_PLACEHOLDER', quote_plus(prompt))
    response = requests.post('http://localhost:8000/api/whatsapp/webhook/', data=payload,
                             headers={'content-type': 'application/x-www-form-urlencoded'})

    root = ET.fromstring(response.text)
    message_text = root.find("Message").text
    print(f"Assistant: {message_text}")

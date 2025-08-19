# 📱 Amar Sahayak – AI-powered WhatsApp Chatbot  

Amar Sahayak is a **WhatsApp-based chatbot** designed to help citizens access information quickly.  
It uses **Retrieval-Augmented Generation (RAG)** with **LangChain** and **ChromaDB**, integrates with **Twilio WhatsApp API**, and supports **bilingual (Odia + English)** answers with **source citations**.  

---

## ✨ Features  
- 🤖 **AI Q&A** – Retrieve answers from uploaded government documents.  
- 🌐 **Bilingual Support** – Odia ↔ English translation pipeline.  
- 📄 **Source Citation** – Each answer includes PDF source + page reference.  
- 💬 **WhatsApp Integration** – Real-time interaction via Twilio WhatsApp API.  
- ⚡ **Local + Cloud Ready** – Works locally with Flask, can scale to AWS/GCP.  

---

## 🛠️ Tech Stack  
- **Backend:** Flask (Python)  
- **AI / NLP:** LangChain, HuggingFace Transformers, ChromaDB  
- **Messaging:** Twilio WhatsApp API  
- **Deployment:** LocalTunnel / Ngrok (for dev), AWS/GCP (for prod)  

---

## ⚙️ Setup Instructions  

### 1️⃣ Clone the Repo  

git clone https://github.com/your-username/amar-sahayak.git
cd amar-sahayak

### 2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Setup Environment Variables (.env)

Create a file named .env in the root folder with:

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
RATE_LIMIT_COUNT=20
RATE_LIMIT_WINDOW=60

### 5️⃣ Create Vector Store (Load Docs)
python rag_engine.py

### 6️⃣ Run the App
python app.py

### 7️⃣ Expose Localhost for Twilio Webhook
lt --port 5000
# or
ngrok http 5000
Copy the generated URL (e.g., https://xyz.loca.lt/whatsapp) and paste it in Twilio → Sandbox → Webhook URL.


### 📲 Usage
Save Twilio Sandbox Number in WhatsApp: +14155238886
Send a question (e.g., "How do I get Ayushman Bharat health card in Odisha?")

### Bot replies with :
Individual health cards with ₹5 lakh annual coverage for eligible families will be issued from Feb 2025.
📄 sample.pdf, page 1  
🤖 Confidence: 0.82

### 📈 Future Enhancements:
🏛️ Web dashboard for uploading documents
🌍 Deployment on AWS/GCP for scaling to lakhs of users
🗣️ Advanced multilingual support (speech + text)
👉 Live Demo (local setup required)

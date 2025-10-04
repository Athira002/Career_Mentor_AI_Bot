# 🧑‍💼 Career Mentor AI Bot

A web-based AI-powered chatbot that provides **instant career guidance** using Hugging Face's conversational AI models. Built with **Streamlit** for a user-friendly interface.

---

## 🚀 Features

- Predefined career Q&A for quick guidance.
- Conversational AI powered by Hugging Face's `facebook/blenderbot-400M-distill` model.
- Chat history with user-friendly chat bubbles and avatars.
- Reset chat functionality.
- Scrollable, interactive chat interface.
- Fully configurable with `.env` for secure API keys.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – Web app framework for Python
- **Hugging Face Inference API** – Conversational AI
- **dotenv** – For environment variable management
- **requests** – HTTP requests to Hugging Face API

---

## 📂 Project Structure

career-mentor-ai-bot/
│
├── career_mentor.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .env.example # Environment variables (HF_API_KEY)
└── README.md # Project documentation

---

## ⚡ Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/<your-username>/career-mentor-ai-bot.git
cd career-mentor-ai-bot
```

2. **Create a virtual environment (optional but recommended):**

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. **Install dependencies:**

pip install -r requirements.txt

4. **Configure environment variables:**

Create a .env file in the root directory.

Add your Hugging Face API key:

HF_API_KEY=your_huggingface_api_key_here

5. **🏃‍♂️ Run the App**

streamlit run career_mentor.py

Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501).

---

💡 Usage

Quick Questions: Click on any predefined question to get instant guidance.

Custom Question: Type your career-related query in the chat input box.

Reset Chat: Use the "Reset Chat" button to start a new conversation.

---

⚠️ Notes

Ensure your Hugging Face API key is valid and has access to facebook/blenderbot-400M-distill.

The bot handles HTTP errors gracefully and provides friendly messages for troubleshooting.

---

📈 Future Improvements

Add user authentication for personalized chat sessions.

Store chat history in a database for long-term analysis.

Integrate additional AI models for specialized advice.

---

📬 Contact

Athira Sreekumar
Email: athisree.02@gmail.com

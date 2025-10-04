import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load Hugging Face API key
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Hugging Face model.
API_URL = "https://api-inference.huggingface.co/pipeline/conversational/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(payload):
    """
    Sends the request to the Hugging Face Inference API.
    The requests library automatically handles the Content-Type: application/json
    when using the json=payload argument.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    # Raise an exception for bad status codes (4xx or 5xx)
    response.raise_for_status() 
    return response.json()

# Page config
st.set_page_config(page_title="Career Mentor AI Bot", page_icon="🧑‍💼", layout="centered")
st.markdown("<h1 style='text-align:center;'>🧑‍💼 Career Mentor AI Bot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Get professional career guidance instantly!</p>", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Predefined Q&A
predefined_qna = [
    {"question": "How do I start a career in data analytics?", "answer": "You can start by learning SQL, Python, and data visualization tools like Power BI or Tableau. Internships and projects help gain practical experience."},
    {"question": "What skills are needed for a software developer?", "answer": "Strong programming skills, problem-solving, version control (Git), and knowledge of algorithms, data structures, and frameworks relevant to your domain."},
    {"question": "How can I improve my resume?", "answer": "Tailor your resume for each job, highlight achievements with metrics, keep it concise (1 page), and ensure proper formatting."},
    {"question": "What is the best way to prepare for interviews?", "answer": "Practice coding or domain-specific questions, do mock interviews, research the company, and prepare strong STAR-format answers for behavioral questions."},
    {"question": "How do I switch careers effectively?", "answer": "Identify transferable skills, gain relevant certifications or training, network in the new industry, and start with internships or freelance projects to build experience."}
]

# Display predefined questions
st.markdown("### Quick Questions")
cols = st.columns(5)
for i, qna in enumerate(predefined_qna):
    if cols[i].button(qna["question"]):
        st.session_state.messages.append({"role": "user", "content": qna["question"]})
        st.session_state.messages.append({"role": "assistant", "content": qna["answer"]})
        st.rerun()

# Chat container
chat_container = st.container()

# Scrollable chat history
with chat_container:
    # Applying some custom CSS for better aesthetics and chat bubble look
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            border: 1px solid #4CAF50;
            color: #4CAF50;
            background-color: #E8F8E8;
        }
        .stButton>button:hover {
            color: white;
            background-color: #4CAF50;
        }
        .user-message-bubble {
            background-color: #D0E1FF; 
            padding: 10px; 
            border-radius: 10px 10px 0 10px; 
            max-width: 70%; 
            margin-bottom: 5px;
        }
        .assistant-message-bubble {
            background-color: #D1FFD6; 
            padding: 10px; 
            border-radius: 10px 10px 10px 0; 
            max-width: 70%; 
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style='display:flex; justify-content:flex-end;'>
                    <div class='user-message-bubble'>
                        <b>You:</b> {msg['content']}
                    </div>
                    <img src='https://cdn-icons-png.flaticon.com/512/147/147144.png' width='30' style='margin-left:5px; border-radius:50%; align-self: flex-start;'>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div style='display:flex; justify-content:flex-start;'>
                    <img src='https://cdn-icons-png.flaticon.com/512/1995/1995519.png' width='30' style='margin-right:5px; border-radius:50%; align-self: flex-start;'>
                    <div class='assistant-message-bubble'>
                        <b>Mentor:</b> {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# User input (main logic change starts here)
if prompt := st.chat_input("Ask your career question here..."):
    # 1. Append user message to the session state immediately
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Prepare payload for Hugging Face Conversational API
    # history_context includes all messages *before* the current one.
    # The last message is the current prompt, which goes into the 'text' field.
    history_context = st.session_state.messages[:-1] 

    past_user_inputs = [
        m['content'] for m in history_context if m['role'] == 'user'
    ]
    generated_responses = [
        m['content'] for m in history_context if m['role'] == 'assistant'
    ]

    # Construct the correct conversational payload
    payload = {
        "inputs": {
            "past_user_inputs": past_user_inputs,
            "generated_responses": generated_responses,
            "text": prompt
        }
    }

    # 3. Hugging Face AI response
    with st.spinner("🧑‍💼 Mentor is thinking..."):
        try:
            output = query_hf(payload)

            # The response for the Conversational task contains the generated_text
            # It can also return an array of messages, but we expect generated_text
            if isinstance(output, list) and output:
                 # In some cases, the API returns a list containing one dict
                 answer = output[0].get("generated_text", "⚠️ Could not parse model response.")
            elif isinstance(output, dict) and 'generated_text' in output:
                 answer = output['generated_text']
            elif isinstance(output, dict) and output.get("error"):
                 answer = f"⚠️ API Error: {output['error']}"
            else:
                 answer = "⚠️ Sorry, I couldn’t generate a response. Please check your API Key and terminal logs."
                 print("Full API Output:", output) # Print error details for debugging

        except requests.exceptions.HTTPError as e:
             answer = f"⚠️ HTTP Error: The API call failed. Status Code: {e.response.status_code}. Please check your Hugging Face API key and verify the model is accessible."
        except Exception as e:
            answer = f"⚠️ Connection Error: {str(e)}"

    # 4. Save AI message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# Reset chat button
if st.button("Reset Chat", type="primary"):
    st.session_state.messages = []
    st.rerun()

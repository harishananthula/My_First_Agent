import streamlit as st
import requests
import json
import os
from datetime import datetime
import tempfile
import base64
import io

CHAT_DIR = "chats"
os.makedirs(CHAT_DIR, exist_ok=True)

def save_chat(chat_name, messages):
    with open(
        os.path.join(CHAT_DIR, f"{chat_name}.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(messages, f, indent=4)


def load_chat(chat_name):
    path = os.path.join(CHAT_DIR, f"{chat_name}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    return []


def get_all_chats():
    chats = []

    for file in os.listdir(CHAT_DIR):
        if file.endswith(".json"):
            chats.append(file[:-5])

    return sorted(chats, reverse=True)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hari Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

.main .block-container {
    max-width: 1000px;
    padding-top: 1rem;
}

.chat-title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:white;
}

.chat-subtitle {
    text-align:center;
    color:#94a3b8;
    margin-bottom:25px;
}

.user-msg {
    background:#2563eb;
    color:white;
    padding:15px;
    border-radius:15px;
    margin:10px 0;
}

.bot-msg {
    background:#1e293b;
    color:white;
    padding:15px;
    border-radius:15px;
    margin:10px 0;
}

.welcome-box {
    background:#111827;
    padding:20px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
}

.feature-card {
    background:#1e293b;
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
}

.sidebar-title {
    text-align:center;
    color:white;
}

.stExpander {
    border-radius: 12px;
    background: #1e293b;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "current_chat" not in st.session_state:

    chat_name = datetime.now().strftime(
        "Chat_%Y%m%d_%H%M%S"
    )

    st.session_state.current_chat = chat_name

    st.session_state.messages = []

    save_chat(chat_name, [])

# ---------------- SIDEBAR ----------------
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

with st.sidebar:

    st.image(LOGO_PATH, width=520)

    st.markdown(
        "<h2 class='sidebar-title'>🤖 Hari Chatbot</h2>",
        unsafe_allow_html=True
    )

    st.markdown("### 💬 Conversations")

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        chat_name = datetime.now().strftime(
            "Chat_%Y%m%d_%H%M%S"
        )

        st.session_state.current_chat = chat_name

        st.session_state.messages = []

        save_chat(chat_name, [])

        st.rerun()

    if st.button(
        "❌ Delete Current Chat",
        use_container_width=True
    ):

        chat_file = os.path.join(
            CHAT_DIR,
            f"{st.session_state.current_chat}.json"
        )

        if os.path.exists(chat_file):
            os.remove(chat_file)

        st.session_state.current_chat = (
            datetime.now().strftime(
                "Chat_%Y%m%d_%H%M%S"
            )
        )

        st.session_state.messages = []

        st.rerun()

    for chat in get_all_chats():

        if st.button(
            f"📁 {chat}",
            key=chat,
            use_container_width=True
        ):

            st.session_state.current_chat = chat

            st.session_state.messages = load_chat(chat)

            st.rerun()

    st.markdown("---")

    st.metric(
        "Total Chats",
        len(get_all_chats())
    )

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

st.markdown("---")

model = "llama3.2:3b"

# ---------------- HEADER ----------------
st.markdown(
    "<div class='chat-title'>🤖 Hari AI Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='chat-subtitle'>Powered by Ollama • Local AI</div>",
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <center>
    <h4 style='color:#94a3b8'>
    📁 {st.session_state.current_chat}
    </h4>
    </center>
    """,
    unsafe_allow_html=True
)
# ---------------- WELCOME ----------------
if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class='welcome-box'>
    <h3>👋 Welcome to Hari Chatbot</h3>

    Ask me anything about:

    • Python Programming

    • Artificial Intelligence

    • Machine Learning

    • Resume Building

    • Interview Preparation

    • Data Science
    </div>
    """, unsafe_allow_html=True)

    # Quick Action Buttons

    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💻 Python Programming", use_container_width=True):

            st.session_state.messages.append({
                "role": "assistant",
                "content": """
💻 Python Programming

Topics I can help with:

• Python Basics
• Variables
• Loops
• Functions
• OOP
• Projects
• Interview Questions

Ask me any Python question.
"""
            })

            st.rerun()

    with col2:
        if st.button("🤖 Artificial Intelligence", use_container_width=True):

            st.session_state.messages.append({
                "role": "assistant",
                "content": """
🤖 Artificial Intelligence

Topics:

• Generative AI
• Chatbots
• LLMs
• NLP
• Computer Vision
• AI Projects
"""
            })

            st.rerun()

    with col3:
        if st.button("📊 Machine Learning", use_container_width=True):

            st.session_state.messages.append({
                "role": "assistant",
                "content": """
📊 Machine Learning

Topics:

• Supervised Learning
• Unsupervised Learning
• Regression
• Classification
• Scikit-Learn
"""
            })

            st.rerun()

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"<div class='user-msg'>👤 {msg['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='bot-msg'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------------- INPUT ----------------
uploaded_image = st.file_uploader(
    "📷 Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:

    st.image(uploaded_image)

    if st.button("🔍 Analyze Image"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as tmp:

            tmp.write(uploaded_image.read())

            image_path = tmp.name

        try:

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llava",
                    "prompt": "Describe this image in detail.",
                    "images": [image_path],
                    "stream": False
                }
            )

            st.success(
                response.json().get("response", "")
            )

        except Exception as e:

            st.error(f"Image analysis failed: {e}")

prompt = st.chat_input(
    "Ask Hari Chatbot anything..."
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_chat(
        st.session_state.current_chat,
        st.session_state.messages
    )

    st.rerun()

with st.expander("➕ Add Attachment"):

    uploaded_image = st.file_uploader(
        "📷 Upload Image",
        type=["png", "jpg", "jpeg"],
        key="chat_image"
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Document",
        type=["pdf", "txt", "docx"],
        key="chat_document"
    )



# ---------------- RESPONSE ----------------

if (
    st.session_state.messages
    and
    st.session_state.messages[-1]["role"] == "user"
):

    user_prompt = st.session_state.messages[-1]["content"]

    # Custom Greetings
    greetings = [
        "hi",
        "hii",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if user_prompt.lower().strip() in greetings:

        answer = """
👋 Hey! I am Hari AI Assistant.

How can I assist you today?

💻 Python Programming

🤖 Artificial Intelligence

📊 Machine Learning

📄 Resume Building

🎯 Interview Preparation
"""

        response_placeholder = st.empty()

        response_placeholder.markdown(
            f"""
            <div class='bot-msg'>
            🤖 {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        save_chat(
            st.session_state.current_chat,
            st.session_state.messages
        )

        st.rerun()

    # Fallback to Ollama for other prompts
    response_placeholder = st.empty()

    full_response = ""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": user_prompt,
                "stream": True
            },
            stream=True,
            timeout=120
        )

        for line in response.iter_lines():

            if line:

                data = json.loads(
                    line.decode("utf-8")
                )

                token = data.get(
                    "response",
                    ""
                )

                full_response += token

                response_placeholder.markdown(
                    f"""
                    <div class='bot-msg'>
                    🤖 {full_response}▌
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:

        full_response = (
            f"❌ Error: {str(e)}"
        )

    response_placeholder.markdown(
        f"""
        <div class='bot-msg'>
        🤖 {full_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    save_chat(
        st.session_state.current_chat,
        st.session_state.messages
    )

    st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
    """
    <center>
    🚀 Built with Streamlit + Ollama<br>
    Developed by Harish Goud
    </center>
    """,
    unsafe_allow_html=True
)
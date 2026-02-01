import streamlit as st
import subprocess
import time

# ------------------ Page Settings ------------------
st.set_page_config(
    page_title="💪 FitBot",
    page_icon="🤖",
    layout="wide",
)

# ------------------ CSS for professional UI with background ------------------
st.markdown("""
<style>
/* Full-page gym background with overlay */
body {
    background-image: url("https://i.pinimg.com/originals/59/92/19/599219776206220585.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #FFFFFF;
    font-family: 'Arial', sans-serif;
}

/* Dark overlay for readability */
body::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.6);  /* semi-transparent black overlay */
    z-index: -1;
}

/* Input box styling */
.stTextInput>div>div>input {
    background-color: #2C2C2C;
    color: #FFFFFF;
    border-radius: 10px;
    padding: 12px;
}

/* Chat container */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #333333;
    border-radius: 10px;
    background-color: rgba(34, 34, 34, 0.8);  /* semi-transparent dark */
}

/* User bubble */
.chat-user {
    background-color: #FF5733;
    color: white;
    padding: 10px;
    border-radius: 15px 15px 0 15px;
    margin: 5px 0;
    text-align: right;
}

/* Bot bubble */
.chat-bot {
    background-color: #333333;
    color: white;
    padding: 10px;
    border-radius: 15px 15px 15px 0;
    margin: 5px 0;
    text-align: left;
}

/* Send button styling */
.stButton>button {
    background-color: #FF5733;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.title("💪 FitBot – Your Personal Fitness AI")
st.subheader("Get workout plans, fitness advice, and exercise guidance instantly!")

# ------------------ Initialize chat history ------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ Input Form ------------------
with st.form(key="input_form"):
    user_input = st.text_input("Ask FitBot something about fitness or workouts:")
    submit_button = st.form_submit_button(label="Send")

# ------------------ Handle Input & Stream Bot Responses ------------------
if submit_button and user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "message": user_input})

    # Construct prompt for Ollama
    prompt = f"""
You are FitBot, a professional fitness coach.
Answer clearly, concisely, and do not repeat previous messages.
Use bullet points or tables for exercises.

User: {user_input}
FitBot:
"""

    # Run the model
    process = subprocess.Popen(
        ["ollama", "run", "mistral"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    process.stdin.write(prompt)
    process.stdin.close()

    bot_message = ""
    placeholder = st.empty()  # Placeholder for streaming

    # Stream output line by line
    for line in process.stdout:
        bot_message += line
        placeholder.markdown(f'<div class="chat-bot">{bot_message.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        time.sleep(0.05)  # small delay for smooth streaming

    # Save final bot response
    st.session_state.history.append({"role": "bot", "message": bot_message.strip()})

# ------------------ Display Chat History ------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f'<div class="chat-user">{chat["message"]}</div>', unsafe_allow_html=True)
    else:
        response = chat["message"].replace("\n", "<br>")
        st.markdown(f'<div class="chat-bot">{response}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
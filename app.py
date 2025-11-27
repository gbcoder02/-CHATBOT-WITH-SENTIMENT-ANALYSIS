import streamlit as st
from chatbot import ChatBot
import streamlit.components.v1 as components

# --- PAGE SETUP & STYLING ---
st.set_page_config(page_title="Sentiment Analysis Chatbot", layout="centered")

st.markdown("""
<style>
.header-text { font-size: 2rem; font-weight: bold; color: #34495e; text-align: center; margin-bottom: 16px; }
.description-text { color: #555; font-size: 1.05rem; text-align: center; margin-bottom: 18px; }
.user-message { background: #e7f3fe; padding: 8px 13px; border-radius: 8px; font-weight: 600; margin-bottom: 4px; }
.bot-message { background: #d5f5e3; padding: 8px 13px; border-radius: 8px; margin-bottom: 4px; }
.sentiment-positive { color: #27ae60; font-weight: 700;}
.sentiment-neutral { color: #7f8c8d; font-weight: 700;}
.sentiment-negative { color: #c0392b; font-weight: 700;}
hr { margin: 12px 0; border: none; border-top: 1px solid #bdc3c7; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-text">Sentiment Analysis Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="description-text">Chat using your voice or keyboard. Sentiment and confidence are shown per message. Click "End Conversation" to see a summary.</div>', unsafe_allow_html=True)

# --- SESSION STATE SETUP ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
chatbot = st.session_state.chatbot

# --- VOICE INPUT WIDGET ---
st.markdown("**🎤 Voice Input:** Click Start, speak, then paste recognized text below.")
components.html("""
    <button onclick="startRecognition()">Start Voice Input</button>
    <p id="output"></p>
    <script>
    var recognition = null;
    function startRecognition() {
        if (!('webkitSpeechRecognition' in window)) {
            document.getElementById('output').innerText = 'Speech Recognition is not supported in this browser.';
            return;
        }
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            document.getElementById('output').innerText = text;
        }
        recognition.onerror = function(event) {
            document.getElementById('output').innerText = 'Error: ' + event.error;
        }
    }
    </script>
""", height=180)

# --- INPUT FORM ---
with st.form(key='chat_form', clear_on_submit=True):
    user_text = st.text_input("Your message:", max_chars=200)
    submitted = st.form_submit_button("Send")

# --- HANDLE NEW MESSAGE ---
if submitted and user_text.strip():
    bot_reply, sentiment = chatbot.handle_user_message(user_text.strip())
    st.session_state.chat_history.append((user_text.strip(), bot_reply, sentiment))

# --- DISPLAY CHAT HISTORY (with TTS for bot reply) ---
for user, bot, sentiment in st.session_state.chat_history:
    st.markdown(f'<div class="user-message">You: {user}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-message">Bot: {bot}</div>', unsafe_allow_html=True)

    senti_css = {
        "Positive": "sentiment-positive",
        "Neutral": "sentiment-neutral",
        "Negative": "sentiment-negative"
    }.get(sentiment['label'], "sentiment-neutral")

    st.markdown(f'<div class="{senti_css}">Sentiment: {sentiment["label"]} (Conf: {sentiment["score"]:.2f})</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Text-to-speech: bot speaks reply aloud
    components.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{bot}");
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- END CONVERSATION BUTTON & SUMMARY ---
if st.button("End Conversation", disabled=(len(st.session_state.chat_history) == 0)):
    overall = chatbot.conversation_sentiment()
    mood = chatbot.mood_trend()
    st.markdown(f"### Overall conversation sentiment: {overall}")
    st.markdown(f"### Mood trend across messages:")
    st.markdown(mood)
    st.session_state.chat_history.clear()
    chatbot.history.clear()
    chatbot.sentiments.clear()

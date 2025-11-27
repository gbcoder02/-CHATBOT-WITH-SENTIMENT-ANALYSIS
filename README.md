# Sentiment Analysis Chatbot

This project implements a chatbot that keeps the full conversation history and performs sentiment analysis on user messages. It supports conversation-level sentiment (Tier 1 – mandatory) and per-message sentiment with mood trend (Tier 2 – additional credit).

## How to run

1. Clone the repository:
git clone <your-repo-url>
cd <your-repo-folder>

text
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:
pip install -r requirements.txt

text
4. Run the command-line chatbot:
python main.py

text
5. Run the Streamlit web app:
streamlit run app.py

text
6. The first run may take some time because the Hugging Face sentiment model is downloaded from the internet.

## Chosen technologies

- **Python 3.x** – main programming language.
- **Hugging Face Transformers** – pre-trained sentiment analysis model (labels: `Positive`, `Neutral`, `Negative`).
- **Streamlit** – lightweight web framework for the interactive chatbot UI.
- **unittest** – Python’s built‑in framework for automated tests.

## Explanation of sentiment logic

### Statement-level sentiment (Tier 2)

- Every user message is passed to the transformer-based sentiment model.
- The model returns:
- `label`: `Positive`, `Neutral` or `Negative`.
- `score`: confidence value between 0 and 1.
- The application displays:
- The original user message.
- The detected sentiment label and confidence for that message.
- In the Streamlit app, sentiment labels are color‑coded:
- Green for Positive.
- Grey for Neutral.
- Red for Negative.

### Conversation-level sentiment (Tier 1)

- For each user message, the chatbot stores the sentiment result in an internal list.
- When the user ends the conversation:
- All confidence scores of messages labeled `Positive` are summed.
- All confidence scores of messages labeled `Negative` are summed.
- If total positive score is greater than total negative score, the final result is **Overall Positive**.
- If total negative score is greater than total positive score, the final result is **Overall Negative**.
- If they are roughly balanced, the final result is **Neutral**.

### Mood trend across the conversation (Tier 2 enhancement)

- A helper function builds a string showing sentiment for each message in order, for example:  
`Msg 1: Positive (0.85) | Msg 2: Neutral (0.60) | Msg 3: Negative (0.78)`.
- This “mood trend” is shown at the end of the conversation to highlight how the user’s emotional tone changes over time.

### Intent-aware responses

- A simple keyword‑based intent classifier is used with four intents:
- `greeting` – e.g. “hello”, “hi”.
- `thanks` – e.g. “thank you”, “thanks”.
- `complaint` – e.g. “disappoint”, “problem”, “issue”.
- `praise` – e.g. “good”, “great”, “better”.
- Both intent and sentiment are used to choose chatbot replies:
- Praise intent → friendly thank‑you message (for example, “Thank you for your kind words!”).
- Complaint or strong negative sentiment → empathetic response acknowledging the concern.
- Greeting → welcome message.
- Thanks → polite acknowledgement.

## Status of Tier 2 implementation

- **Per‑message sentiment:** Implemented.  
Every user message is analyzed individually and displayed with sentiment label and confidence in both the terminal and the Streamlit UI.
- **Mood trend summary:** Implemented.  
A `mood_trend()` function produces a sequential summary of sentiment for all messages and is displayed when the user ends the conversation.
- **Intent‑based responses:** Implemented.  
Different responses are used for greetings, thanks, complaints and praise to make the conversation more natural.
- **Extra UI features:** Implemented.  
The Streamlit interface includes styled user/bot message blocks, color‑coded sentiments, and optional browser‑based voice input and text‑to‑speech for bot replies (where supported by the browser).

## Tests

- Unit tests are written using `unittest`:
- `TestSentimentAnalysis` checks that clearly positive, negative and neutral sentences are classified with the expected labels and reasonable confidence.
- `TestIntentClassifier` confirms that example phrases are mapped to the appropriate intents (greeting, complaint, praise, etc.).
- `TestChatBotBehaviour` verifies that:
 - `handle_user_message` returns a string reply and a sentiment dictionary.
 - Complaint messages trigger an empathetic style response.
 - Praise messages (such as “Last experience was better”) trigger a thank‑you style response.
 - Conversation‑level sentiment and mood trend functions return non‑empty, meaningful summaries.

## Possible future improvements

- Replace the keyword‑based intent classifier with a machine‑learning model trained on labeled intent data.
- Store conversation histories in a database or log file for later analysis.
- Add charts or dashboards (for example with Plotly or Matplotlib inside Streamlit) to visualize sentiment trends over many conversations.# -CHATBOT-WITH-SENTIMENT-ANALYSIS
This project is a machine learning–powered chatbot that not only responds to user inputs but also detects sentiment (Positive, Negative, Neutral) behind every message. It combines NLP (Natural Language Processing) techniques with a rule-based or ML-based chatbot system, making conversations more human-like and emotionally aware.

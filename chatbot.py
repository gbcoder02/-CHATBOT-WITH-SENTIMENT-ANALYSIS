from sentiment import SentimentAnalyzer

class IntentClassifier:
    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "thanks": ["thank", "thanks", "thx", "appreciate"],
            "complaint": ["disappoint", "bad", "terrible", "problem", "issue", "late", "concern", "not happy", "unhappy"],
            "praise": ["good", "great", "love", "excellent", "awesome", "better"]
        }

    def classify(self, text):
        text = text.lower()
        for intent, keywords in self.intents.items():
            if any(word in text for word in keywords):
                return intent
        return "unknown"

class ChatBot:
    def __init__(self):
        self.history = []
        self.sentiments = []
        self.intent_classifier = IntentClassifier()
        self.sentiment_analyzer = SentimentAnalyzer()

    def handle_user_message(self, message):
        intent = self.intent_classifier.classify(message)
        sentiment = self.sentiment_analyzer.analyze_sentiment(message)
        self.history.append(message)
        self.sentiments.append(sentiment)
        response = self.generate_response(intent, sentiment)
        return response, sentiment

    def generate_response(self, intent, sentiment):
        # Prioritize praise intent to always reply positively
        if intent == "praise":
            return "Thank you for your kind words!"
        last_msg = self.history[-1].lower() if self.history else ""
        complaint_keywords = ["disappoint", "bad", "terrible", "problem", "issue", "concern", "not happy", "unhappy"]

        if intent == "complaint" or (sentiment['label'] == 'Negative' and any(kw in last_msg for kw in complaint_keywords)):
            return "I’ll make sure your concern is addressed."
        elif intent == "greeting":
            return "Hello! How can I assist you today?"
        elif intent == "thanks":
            return "You’re welcome! Glad to help."
        else:
            if sentiment['label'] == 'Negative':
                return "I understand your concern. We appreciate your feedback."
            elif sentiment['label'] == 'Positive':
                return "Great to hear that!"
            else:  # Neutral or unknown
                return "Thank you for sharing that."

    def conversation_sentiment(self):
        if not self.sentiments:
            return "No conversation data."
        pos_scores = [s['score'] for s in self.sentiments if s['label'] == 'Positive']
        neg_scores = [s['score'] for s in self.sentiments if s['label'] == 'Negative']
        if sum(pos_scores) > sum(neg_scores):
            return "Overall Positive"
        elif sum(neg_scores) > sum(pos_scores):
            return "Overall Negative"
        else:
            return "Neutral"

    def mood_trend(self):
        if not self.sentiments:
            return "No conversation data."
        trend = [f"Msg {i+1}: {s['label']} ({s['score']:.2f})" for i, s in enumerate(self.sentiments)]
        return " | ".join(trend)


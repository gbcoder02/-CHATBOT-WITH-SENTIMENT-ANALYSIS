from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

    def analyze_sentiment(self, text):
        result = self.classifier(text)[0]
        label = result['label'].capitalize()  # 'Positive', 'Neutral', or 'Negative'
        return {"label": label, "score": result['score']}

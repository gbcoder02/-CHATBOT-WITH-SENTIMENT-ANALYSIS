import unittest
from sentiment import SentimentAnalyzer
from chatbot import ChatBot, IntentClassifier


class TestSentimentAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        result = self.analyzer.analyze_sentiment("I love this product!")
        self.assertEqual(result["label"], "Positive")
        self.assertGreater(result["score"], 0.7)

    def test_negative_sentiment(self):
        result = self.analyzer.analyze_sentiment("This is terrible and disappointing.")
        self.assertEqual(result["label"], "Negative")
        self.assertGreater(result["score"], 0.7)

    def test_neutral_sentiment(self):
        result = self.analyzer.analyze_sentiment("It is an average experience.")
        self.assertEqual(result["label"], "Neutral")


class TestIntentClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = IntentClassifier()

    def test_greeting_intent(self):
        intent = self.classifier.classify("Hi there")
        self.assertEqual(intent, "greeting")

    def test_complaint_intent(self):
        intent = self.classifier.classify("Your service disappoints me")
        self.assertEqual(intent, "complaint")

    def test_praise_intent(self):
        intent = self.classifier.classify("Last experience was better")
        self.assertEqual(intent, "praise")


class TestChatBotBehaviour(unittest.TestCase):
    def setUp(self):
        self.bot = ChatBot()

    def test_handle_user_message_structure(self):
        reply, sentiment = self.bot.handle_user_message("Hello")
        self.assertIsInstance(reply, str)
        self.assertIn("label", sentiment)
        self.assertIn("score", sentiment)

    def test_complaint_triggers_empathetic_response(self):
        text = "Your service disappoints me"
        reply, sentiment = self.bot.handle_user_message(text)
        self.assertIn("concern", reply.lower())  # matches your template like “make sure your concern is addressed”

    def test_praise_triggers_thank_you_response(self):
        text = "Last experience was better"
        reply, sentiment = self.bot.handle_user_message(text)
        self.assertIn("thank you", reply.lower())

    def test_conversation_overall_positive(self):
        self.bot.handle_user_message("I love this service")
        self.bot.handle_user_message("You were very helpful")
        overall = self.bot.conversation_sentiment()
        self.assertIn("Positive", overall)

    def test_mood_trend_has_message_indices(self):
        self.bot.handle_user_message("I love this")
        self.bot.handle_user_message("This is bad")
        trend = self.bot.mood_trend()
        self.assertIn("Msg 1:", trend)
        self.assertIn("Msg 2:", trend)


if __name__ == "__main__":
    unittest.main()

from chatbot import ChatBot

def main():
    bot = ChatBot()
    print("Chatbot started. Type 'exit' to end.\n")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response, sentiment = bot.handle_user_message(user_input)
        print(f'→ Sentiment: {sentiment["label"]} (Confidence: {sentiment["score"]:.2f})')
        print(f'Chatbot: "{response}"\n')

    overall_sentiment = bot.conversation_sentiment()
    print(f"Final Output: Overall conversation sentiment: {overall_sentiment} – general summary")

if __name__ == "__main__":
    main()

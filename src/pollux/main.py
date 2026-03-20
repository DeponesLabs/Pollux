from pollux.clients import GeminiClient

def main():
    
    gclient = GeminiClient()

    print(gclient.models)

    # print("#####__ Gemini Terminal is Ready! __#####")
    # print("To exit, type 'quit' or 'exit'...\n")

    # while True:
    #     user_input = input("\nYou: ")
        
    #     if user_input.lower() in ['quit', 'exit']:
    #         print("See you later!")
    #         break
            
    #     if not user_input.strip():
    #         continue

    #     try:
    #         response = chat.send_message(user_input)
    #         print(f"\nGemini: {response.text}")
            
    #         # Save to file using Append mod
    #         with open(DAILY_LOG_FILE, "a", encoding="utf-8") as f:
    #             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             f.write(f"\n[{timestamp}] You: {user_input}\n")
    #             f.write(f"[{timestamp}] Gemini: {response.text}\n")
    #             f.write("-" * 50 + "\n")
                
    #     except Exception as error:
    #         print(f"\nAn error occured: {error}")


if __name__ == '__main__':
    main()
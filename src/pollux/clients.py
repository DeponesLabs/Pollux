import os
from datetime import datetime
import json
from dotenv import load_dotenv
from google import genai

from google.genai import types

load_dotenv()

from pollux.models import GeminiModel
from pollux.enums import GeminiModelType
class PolluxClient:
    
    today = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    api_key = os.environ.get("GEMINI_API_KEY")
    daily_log_file = f"chat_records/gemini_records_{today}.txt"
        
    def __init__(self, model_type=GeminiModelType.FLASH_2_5):

        if not PolluxClient.api_key:
            print("API Key not found! Please set the GEMINI_API_KEY environment variable.")
            exit()
            
        self.models : list[GeminiModel] = []
        self.safety_config = None

        self.client = genai.Client(api_key=PolluxClient.api_key)
        self.set_safety_config()
        self.init_chat(model_type)
        self.fetch_models()

    def set_safety_config(self, hate_speech=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, 
                                harassment=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                                sexually_explicit=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                                dangerous_content=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE):
        
        config = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=hate_speech
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=harassment
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=sexually_explicit
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=dangerous_content
            ),
        ]
        
        self.safety_config = types.GenerateContentConfig(safety_settings=config)

    def init_chat(self, model = GeminiModelType.FLASH_2_5):
        
        self.chat = self.client.chats.create(model=model, config=self.safety_config)
        
    def _chat_stream(self):
        
        print("#####__ Gemini Terminal is Ready! __#####")
        print("To exit, type 'quit' or 'exit'...\n")

        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("See you later!")
                break
                
            if not user_input.strip():
                continue

            try:
                response = self.chat.send_message(user_input)
                print(f"\nGemini: {response.text}")
                yield user_input, response.text
    
            except Exception as error:
                print(f"\nAn error occured: {error}")

    def fetch_models(self):
        
        for raw_model in self.client.models.list():
            gmodel = GeminiModel.from_api(raw_model)
            self.models.append(gmodel)
    
    def export_models_to_json(self, path="gemini_models_catalog.json"):
            
        models_dict_list = [model.to_dict() for model in self.models]
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(models_dict_list, f, indent=4, ensure_ascii=False)

    def exec_chat(self, archiver):
        
        print(f"#####__ Pollux Terminal is Ready! (Archiving to: {archiver.filename}) __#####")
        
        for user_input, response_text in self._chat_stream():
            archiver.append_message("User", user_input)
            archiver.append_message("Pollux", response_text)
            
        archiver.save()

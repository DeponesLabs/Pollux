import os
from dotenv import load_dotenv

from pollux.clients import PolluxClient
from mercury.archivers import DocxArchiver

load_dotenv()

def main():
    
    filename = os.environ.get("CHAT_RECORDS_PATH")
    
    pollux = PolluxClient()
    # pollux.export_models_to_json()
    archiver = DocxArchiver(filename=filename)
    pollux.exec_chat(archiver=archiver)
   

if __name__ == '__main__':
    main()

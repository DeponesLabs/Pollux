import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from pollux.clients import PolluxClient
from pollux.archivers import DocxArchiver


load_dotenv()

# load_env_vars
CHAT_DIR = os.environ.get("CHAT_RECORDS_DIR")
DOCX_BASE= os.environ.get("DOCX_BASE")
MD_BASE= os.environ.get("MD_BASE")

def main():
    
    filename = "pollux-chat"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename}-{timestamp}"    
    
    p = CHAT_DIR / Path(filename)
    
    pollux = PolluxClient()
    archiver = DocxArchiver(filename=p.absolute())
    pollux.exec_chat(archiver=archiver)
   

if __name__ == '__main__':
    main()

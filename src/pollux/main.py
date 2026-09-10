import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from pollux.clients import PolluxClient
from pollux.archivers import DocxArchiver

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():

    env_chat_dir  = os.environ.get("CHAT_RECORDS_DIR")
    env_docx_base = os.environ.get("DOCX_BASE")
    env_md_base = os.environ.get("MD_BASE")

    chat_dir = Path(env_chat_dir) if env_chat_dir else Path.home() / ".pollux" / "chats"
    docx_base = Path(env_docx_base) if env_docx_base else Path.home() / ".pollux" / "docx"
    md_base = Path(env_md_base) if env_md_base else Path.home() / ".pollux" / "md"

    filename = "pollux-chat"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename}-{timestamp}"

    # Ensure the directory exists before attempting to read or write
    chat_dir.mkdir(parents=True, exist_ok=True)
    docx_base.mkdir(parents=True, exist_ok=True)
    md_base.mkdir(parents=True, exist_ok=True)

    p = Path(chat_dir) / Path(filename)
    
    pollux = PolluxClient()
    archiver = DocxArchiver(filename=p.absolute())
    pollux.exec_chat(archiver=archiver)

if __name__ == '__main__':
    main()

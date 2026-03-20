from pollux.clients import PolluxClient
from mercury.archivers import DocxArchiver

def main():
    
    pollux = PolluxClient()
    # pollux.export_models_to_json()
    archiver = DocxArchiver("session_2026_03_20")
    pollux.exec_chat(archiver=archiver)
   

if __name__ == '__main__':
    main()

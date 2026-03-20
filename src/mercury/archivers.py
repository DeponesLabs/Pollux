import os
from datetime import datetime
import json
from abc import ABC, abstractmethod
from docx import Document

class BaseArchiver(ABC):
    
    def __init__(self, base_filename):
    
        self.filename = base_filename

    @abstractmethod
    def append_message(self, role: str, text: str):
        pass

    @abstractmethod
    def save(self):
        pass


class DocxArchiver(BaseArchiver):
    
    def __init__(self, base_filename, heading='Pollux AI - Session Record', level=0):
        
        super().__init__(f"{base_filename}.docx")
        
        self.doc = Document()
        self.doc.add_heading(heading, level)

    def append_message(self, role: str, text: str):
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        p = self.doc.add_paragraph()
        
        p.add_run(f"[{timestamp}] {role}: ").bold = True
        p.add_run(text)
        
        self.save() 

    def save(self):
        
        self.doc.save(self.filename)


class TxtArchiver(BaseArchiver):
    
    def __init__(self, base_filename):
        
        super().__init__(f"{base_filename}.txt")

    def append_message(self, role: str, text: str):
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {role}: {text}\n")
            f.write("-" * 40 + "\n")

    def save(self):
        pass


class JsonArchiver(BaseArchiver):
    
    def __init__(self, base_filename):
        
        super().__init__(f"{base_filename}.json")
        
        self.history = []

    def append_message(self, role: str, text: str):
        
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "text": text
        })

    def save(self):
        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

if TYPE_CHECKING:
    # This block is only read by Pylance (Static Type Checker). 
    # # At runtime, Python completely ignores this, meaning Circular Import never occurs.
    from pollux.archivers import BaseArchiver, DocxArchiver, MdArchiver

def iter_block_items(parent_document):
    
    for child in parent_document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent_document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent_document)
            
class IArchiveConverter(ABC):

    @abstractmethod
    def convert(self, source: BaseArchiver, target: BaseArchiver):
        pass
            
class DocxToMdConverter(IArchiveConverter):
    
    def convert(self, source: DocxArchiver, target: MdArchiver):
         
        for block in iter_block_items(source.doc):
            # Use "Structural Pattern Matching"
            match block.__class__.__name__:
                case 'Paragraph':
                    # Extract runs (bold, italic) and convert to MD string
                    md_string = self._process_paragraph(block)
                    target.append_block(md_string)
                case 'Table':
                    # Extract rows/cells and format as MD table
                    md_table_string = self._process_table(block)
                    target.append_block(md_table_string)
                    
    def _parse_block(self, element) -> str:
        """Pattern matching for block-level elements."""
        match type(element).__name__:
            case 'Paragraph':
                return self._process_paragraph(element)
            case 'Table':
                return self._process_table(element)
            case _:
                # Ignore unknown shapes, images, etc. for now
                return ""

    def _process_paragraph(self, paragraph: Paragraph) -> str:
        """Iterate through runs to extract formatting."""
        md_text = ""
        for run in paragraph.runs:
            text = run.text
            if not text:
                continue
                
            # Markdown formatting rules
            if run.bold:
                text = f"**{text}**"
            if run.italic:
                text = f"*{text}*"
                
            md_text += text
            
        return md_text + "\n"

class MdToDocxConverter(IArchiveConverter):
    
    def convert(self, source: MdArchiver, target: DocxArchiver):
        # Iterate through Markdown lines or blocks
        for line in source.get_raw_lines(): 
            
            # Block-level routing based on Markdown prefixes
            if line.startswith('#'):
                self._process_heading(line, target)
            elif line.startswith('|'):
                self._process_table_row(line, target)
            else:
                self._process_paragraph(line, target)

    def _process_paragraph(self, line: str, target: DocxArchiver):
        # Create a new paragraph in the target Document
        p = target.doc.add_paragraph()
        
        # ... Inline regex parsing for **bold** and *italic* runs goes here
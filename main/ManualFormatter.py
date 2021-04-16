import os
import PyPDF2
import nltk
import jsonlines
from nltk import tokenize
nltk.download('punkt')


class ManualFormatter:
    path = "resources/manuals"

    def __init__(self):
        pass

    def get_pdf_manuals(self):
        manuals = []
        for manual in os.listdir(self.path):
            # adds only pdf files to convert
            if os.path.isfile(os.path.join(self.path, manual)) and manual.endswith(".pdf") and not manuals.__contains__(manual):
                manuals.append(manual)
        return manuals
    
    def convert_pdf_manuals(self):
        manuals = self.get_pdf_manuals()
        texts = []
        for manual in manuals:
            with open(self.path + "/" + manual, 'rb') as m:
                pdfReader = PyPDF2.PdfFileReader(m)
                for pageNum in range(pdfReader.numPages):
                    texts.append(pdfReader.getPage(pageNum).extractText())
        return texts

        
    
    def format_manuals(self):
        unformatted_texts = self.convert_pdf_manuals()
        char_limit = 1300
        formatted_texts = []
        for text in unformatted_texts:
            formatted_text = tokenize.sent_tokenize(text, language="english")
            chars = 0
            new_text = ""
            for f_text in formatted_text:
                if len(f_text) + chars <= char_limit:
                    new_text += f_text
                    chars += len(f_text)
                else:
                    formatted_texts.append(new_text)
                    chars = 0
            if chars != 0:
                formatted_texts.append(new_text)
        #print(formatted_texts)
        print(len(formatted_texts))
        print(sum(len(s) for s in formatted_texts))
        return formatted_texts
    
    def jsonl_write(self, formatted_texts):
        with jsonlines.open('resources/manuals/temp.jsonl', mode='w') as writer:
            writer.write_all(formatted_texts)


        

m = ManualFormatter()
m.jsonl_write(m.format_manuals())

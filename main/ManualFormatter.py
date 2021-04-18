import os
import PyPDF2
import nltk
import jsonlines
import json
import xmltodict
from nltk import tokenize
from tqdm import tqdm


class Formatter:
    PATH = "resources/manuals"
    manuals = []

    def __init__(self):
        for manual in os.listdir(self.PATH):
            if os.path.isfile(os.path.join(self.PATH, manual)) and manual != "temp.jsonl" and manual != "api.txt":
                self.manuals.append(manual)

    
    def convert_pdf_manual(self, manual):
        texts = []
        with open(self.PATH + "/" + manual, 'rb') as m:
            pdfReader = PyPDF2.PdfFileReader(m)
            for pageNum in range(pdfReader.numPages):
                text = pdfReader.getPage(pageNum).extractText()
                text = text.replace("\n", ' ')
                text = text.replace("\"", "\\\"")
                text.encode('ascii', 'ignore')


                texts.append(text)
        return texts
        
    
    def format_manuals(self):
        jsonl_texts = []
        print("Formatting manuals:")
        for manual in self.manuals:
            if manual.endswith(".pdf"):
                jsonl_texts.append(self.convert_pdf_manual(manual))
            elif manual.endswith(".json") or manual.endswith(".txt"):
                with open(self.PATH + '/' + manual, 'r') as f:
                    texts = f.readlines()
                    f_texts = []
                    bool1 = False
                    prev_text = ""
                    for text in texts:
                        text = text.replace("\n", ' ')
                        text = text.replace("\\\"", "")
                        text = text.replace("\"", "\\\"")
                        text = text.replace("  ", "")
                        text.encode('ascii', 'ignore')
                        text_lowercase = text.lower()
                        if text.__contains__("instruction") or text.__contains__("shortdesc") or text.__contains__("cause"):
                            bool1 = True
                        if text.__contains__('label'):
                            bool1 = False
                        if text_lowercase.islower() and not text.__contains__("@") and text.__contains__("$") and bool1:
                            text = text.replace("{", "").replace("}", "").replace("$", "").replace(":", "").replace("[", "").replace("]", "").replace("\\\"instruction\\\"", "").replace("\\\"shortdesc\\\"", "").replace("\\\"cause\\\"", "").replace("\\\"", "")
                            if len(prev_text) + len(text) <= 1500:
                                prev_text += text
                                continue
                            else:
                                f_texts.append(prev_text)
                                prev_text = text
                                continue
                            f_texts.append(text)
                    if prev_text != "":
                        f_texts.append(prev_text)
                    jsonl_texts.append(f_texts)
            elif manual.endswith(".jsonl"):
                with open(self.PATH + '/' + manual, 'r') as f:
                    jsonl_texts.append(f.readlines())   
            else:
                print("Could not read this file: " + manual)
        
        with open('resources/manuals/temp.jsonl', mode='w') as writer:
            for text in jsonl_texts:
                for line in tqdm(text):
                    inserted_line = line
                    char_limit = 1500
                    while len(inserted_line) >= char_limit:
                        writer.write("{\"text\":\"" + inserted_line[:char_limit-1]+ "\"}\n")
                        inserted_line = inserted_line[char_limit-1:]
                    if inserted_line != "":
                        writer.write("{\"text\":\"" + inserted_line + "\"}\n")
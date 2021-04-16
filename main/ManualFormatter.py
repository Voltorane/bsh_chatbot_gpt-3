import os
import PyPDF2
import nltk
import jsonlines
import json
import xmltodict
from nltk import tokenize


class ManualFormatter:
    PATH = "resources/manuals"
    manuals = []

    def __init__(self):
        for manual in os.listdir(self.PATH):
            # adds only pdf files to convert
            if os.path.isfile(os.path.join(self.PATH, manual)):
                self.manuals.append(manual)


    def get_pdf_manuals(self):
        manuals = []
        for manual in os.listdir(self.PATH):
            # adds only pdf files to convert
            if os.path.isfile(os.path.join(self.PATH, manual)) and manual.endswith(".pdf") and not manuals.__contains__(manual):
                manuals.append(manual)
        return manuals
    
    def convert_pdf_manual(self, manual):
        texts = []
        with open(self.PATH + "/" + manual, 'rb') as m:
            pdfReader = PyPDF2.PdfFileReader(m)
            for pageNum in range(pdfReader.numPages):
                text = pdfReader.getPage(pageNum).extractText()
                text = text.replace("\n", '')


                texts.append(text)
        return texts

    def convert_json_manual(self, manual):
        manuals = []
        
    
    def format_manuals(self):
        jsonl_texts = []
        for manual in self.manuals:
            if manual.endswith(".pdf"):
                jsonl_texts.append(self.convert_pdf_manual(manual))
            elif manual.endswith(".json"):
                with open(self.PATH + '/' + manual, 'r') as f:
                    texts = f.readlines()
                    f_texts = []
                    for text in texts:
                        text = text.replace("\n", '')
                        text_lowercase = text.lower()
                        if text_lowercase.islower():
                            f_texts.append(text)
                    jsonl_texts.append(f_texts)
            elif manual.endswith(".txt"):
                with open(self.PATH + '/' + manual, 'r') as f:
                    jsonl_texts.append(f.readlines())
            # elif manual.endswith(".xml"):
            #     with open(self.PATH + '/' + manual, 'rb') as f:
            #         x = xmltodict.parse(f.read)
            #         j = json.dumps(x)
            #         unformatted_texts.append(j)
            elif manual.endswith(".jsonl"):
                with open(self.PATH + '/' + manual, 'r') as f:
                    jsonl_texts.append(f.readlines())
                    
            else:
                pass
                # raise RuntimeError('Incorrect type of data')
        
        with open('resources/manuals/temp.jsonl', mode='w') as writer:
            # writer.write_all(formatted_texts)
            for text in jsonl_texts:
                for line in text:
                    inserted_line = line
                    char_limit = 700
                    while len(inserted_line) >= char_limit:
                        writer.write("{\"text\":\"" + inserted_line[:char_limit-1]+ "\"}\n")
                        inserted_line = inserted_line[char_limit-1:]
                    writer.write("{\"text\":\"" + inserted_line + "\"}\n")
                    # while len(inserted_line) >= char_limit:
                    #     writer.write(inserted_line[:char_limit-1])
                    #     inserted_line = inserted_line[char_limit-1:]
                    # writer.write(inserted_line)
                    # writer.write(line)
        
        # for text in unformatted_texts:
        #     formatted_text = tokenize.sent_tokenize(text, language="english")
        #     chars = 0
        #     new_text = ""
        #     for f_text in formatted_text:
        #         if len(f_text) + chars <= char_limit:
        #             new_text += f_text
        #             chars += len(f_text)
        #         else:
        #             formatted_texts.append(new_text + "}\n")
        #             new_text = "{\"text\":"
        #             chars = 0
        #     if chars != 0:
        #         formatted_texts.append(new_text + "}\n")
        #print(formatted_texts)
        # print(len(formatted_texts))
        # print(sum(len(s) for s in formatted_texts))
        # return formatted_texts
    
    def jsonl_write(self, formatted_texts):
        with jsonlines.open('resources/manuals/temp.jsonl', mode='w') as writer:
            writer.write_all(formatted_texts)


        

m = ManualFormatter()
m.format_manuals()
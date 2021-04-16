import os
import requests
import openai
import json

class Bot:
    api_key = ""

    def __init__(self):
        with open("resources/api_v.txt", 'r') as f:
            self.api_key = f.readline()
    
b = Bot()

jsonFILE = None

# with open("resources/manuals/index.json", 'r') as f:
#     jsonFILE = f.readlines()

# with open("resources/manuals/index1.jsonl", 'w') as f:
#     for entry in jsonFILE:
#         json.dump(entry, f)
#         f.write('\n')


openai.api_key = b.api_key
print(openai.File.create(
  file=open("resources/manuals/temp.jsonl"),
  purpose='answers'
))


import os
import requests
import openai
import json

class Bot:
    api_key = "sk-OXawTe7IHhSE6c4rlCZ9kb7lItrskyEdvIeXDHR2"

    def __init__(self):
        pass
    
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


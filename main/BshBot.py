import os
import requests
import openai
import json
import time

class Bot:
    api_key = ""

    def __init__(self):
        with open("resources/api_v.txt", 'r') as f:
            self.api_key = f.readline()

    
b = Bot()

openai.api_key = b.api_key

for el in openai.File.list()['data']:
    openai.File.delete(el['id'])

response = openai.File.create(
  file=open("resources/manuals/temp.jsonl"),
  purpose='answers'
)

# print(response)

time.sleep(10)

# print(openai.File.list())
print(openai.Answer.create(
    search_model="ada",
    model="curie",
    question="What is the max volume?",
    file=response['id'],
    examples_context="In 2017, U.S. life expectancy was 78.6 years.",
    examples=[["What is human life expectancy in the United States?", "78 years."]],
    max_rerank=10,
    max_tokens=100,
    stop=["\n", "<|endoftext|>"]
))


import os
import requests
import openai
import json
import time
import re

class Bot:
    api_key = ""

    def __init__(self):
        with open("resources/api_v.txt", 'r') as f:
            self.api_key = f.readline()
    
    def create_questions(self, furniture_type, times):
        question_set = []

        for i in range(times):
            questions = []
            response = openai.Completion.create(
            engine="davinci",
            prompt="Six users contact customer support regarding " + furniture_type +". The users have problems. Create a list of six specific questions they have:\n1:",
            temperature=0.8,
            max_tokens=100,
            top_p=0.75,
            frequency_penalty=0.75,
            presence_penalty=0.0,
            )
            questions = (response['choices'][0]['text'].split("\n"))
            regex = re.compile(r'^\d$\:')
            new_questions = []
            for question in questions:
                if question != "":
                    new_question = re.sub(regex, "", question)
                    new_questions.append(new_question)
            question_set.append(new_questions)
        
        return question_set
    
    def create_answers(self, question_set, file_id = "file-TWQlnW4kO5VMEKuV6Fjo9u1D"):
        qa_dict = {}

        i = 1
        for questions in question_set:
            for question in questions:
                question = question.replace("\"", "")
                try:
                    response = openai.Answer.create(
                        search_model="davinci",
                        model="curie",
                        question=question,
                        file=file_id,
                        examples_context="In 2017, U.S. life expectancy was 78.6 years.",
                        examples=[["What is human life expectancy in the United States?", "78 years."]],
                        max_rerank=10,
                        max_tokens=200,
                        stop=["\n", "<|endoftext|>"]
                    )
                    qa_dict[i] = {}
                    answer = response['answers'][0]
                    qa_dict[i]['Question'] = question
                    if answer == "":
                        qa_dict[i]['Answer Description'] = "Did not found any result in manual :("
                    else:
                        qa_dict[i]['Answer Description'] = ""
                    qa_dict[i]['Answer'] = answer
                    qa_dict[i]['Selected documents'] = response['selected_documents']
                    # print(str(i) + ")" + "Question: " + question)
                    # print(str(i) + ")" + "Answer: " + response['answers'][0] + "\n______________________________________________________________\n")
                    # print(response)
                except Exception as e:
                    print(e)
                i += 1
        
        return qa_dict


    
b = Bot()

openai.api_key = b.api_key

sample_question_set = [["I think my dishwasher is broken because it won't stop beeping.",
 "What is the total cycle time for the dishwasher?", "How much water does it use per cycle?", "Is there a guarantee on this product?",
 "Why does the door latch fail to engage when the dishwasher door is closed?", "I have a small kitchen and don't have room for a dishwasher. Can I stack it?"]]

# qa_dict = b.create_answers(b.create_questions("dishwasher", 1))
qa_dict = b.create_answers(sample_question_set)
t = time.localtime()
current_time = time.strftime("%m_%d_%H_%M", t)
print(current_time)
with open("main/results/result" + current_time + ".json", 'a+') as json_file:
    json.dump(qa_dict, json_file)

# for el in openai.File.list()['data']:
#     openai.File.delete(el['id'])

# response = openai.File.create(
#   file=open("resources/manuals/temp.jsonl"),
#   purpose='answers'
# )

# print(response)

# time.sleep(10)

# print(openai.File.list())

# response = openai.Answer.create(
#     search_model="davinci",
#     model="curie",
#     question="Which electrical device is this text about?",
#     file="file-TWQlnW4kO5VMEKuV6Fjo9u1D",
#     examples_context="Bosch Security Systems | 2007-10 | PLE-2MA120-EU, PLE-2MA240-EU en Plena Mixer Amplifier | Installation and User Instructions | Installation en | 13 3Installation 3.1 Unpack unit 1Remove the unit from the box, and discard the packaging material accord ing to local regulations.2Use your fingernails to carefully peel off the protective plastic film from the label holders. Do not use sharp or pointed objects. 3.2 Install unit in rack (optional) The Plena Mixer Amplifier is intended for tabletop use, but you can also mount the unit in a 19 rack (see figure 3.1).If you mount the unit in a rack, you must: •ensure that it does no t exceed the overheating temperature (55 °C ambient). •us",
#     examples=[["Which electrical device is this text about?", "Car Amplifier"]],
#     max_rerank=10,
#     max_tokens=200,
#     stop=["\n", "<|endoftext|>"]
# )

# print(response)




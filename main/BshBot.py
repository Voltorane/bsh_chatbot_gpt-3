import os
import requests
import openai
import json
import time
import re
from tqdm import tqdm
from ManualFormatter import Formatter

class Bot:

    def __init__(self):
        with open("resources/api.txt", 'r') as f:
            openai.api_key = f.readline()
    
    def create_questions(self, times):
        question_set = []
        try:
            print("Generating questions")
            for i in tqdm(range(int(times))):
                questions = []
                response = openai.Completion.create(
                engine="davinci",
                prompt="Six users contact customer support regarding car amplifier or dishwasher. The users have problems. Create a list of six specific questions they have:\n1:",
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
        except Exception as e:
            print(e)
        
        return question_set
    
    def create_answers(self, question_set, file_id = "file-3rNeRHnwyfTonykKvwClKih6"):
        qa_dict = {}

        i = 1
        print("Answering the question sets!")
        for questions in tqdm(question_set):
            for question in questions:
                question = question.replace("\"", "")
                try:
                    response = openai.Answer.create(
                        search_model="davinci",
                        model="curie",
                        question=question,
                        file=file_id,
                        examples_context="If the dishwasher is installed above or below other domestic appliances, follow the information on installation in combination with"
                        + "a dishwasher in the installation instructions for the individual appliances. If there is no information or if the installation instructions do not"
                        + "include the relevant information, contact the manufacturer of these appliances to check that the dishwasher can be installed above or below these"
                        + "appliances. If no information is available from the manufacturer, the dishwasher should not be installed above or below such appliances. To ensure"
                        + "the safe operation of all domestic appliances, continue following the installation instructions for the dishwasher. Do not ins"
                        + "tall the dishwasher under a hob. Do not install the dishwasher near heat sources, e.g. radiators, heat storage tanks, ovens or other appliances that generate heat.,",
                        examples=[["I have a small kitchen and don't have room for a dishwasher. Can I stack it?", "No. The dishwasher must be installed on a level surface"]],
                        max_rerank=20,
                        max_tokens=200,
                        stop=["\n", "<|endoftext|>"]
                    )
                    qa_dict[i] = {}
                    answer = response['answers'][0]
                    qa_dict[i]['Question'] = question
                    if answer == "":
                        qa_dict[i]['Answer Description'] = "Did not find any result in manual :("
                        gpt3_response = openai.Completion.create(
                                        engine="davinci",
                                        prompt="Answer the question if it is about dishwashers. Respond with n/a if the question is not about dishwashers or nonsense.\n###\nQ: How can I clean the dishwasher?\nA: Wipe down door seals with a damp, soft cloth.\n###\nQ: What is the square root of banana?\nA: n/a\n###\nQ: what's the square root of 3?\nA:  n/a\n###\nQ: Why does the door latch fail to engage when the dishwasher door is closed?\nA: The door latch is designed to engage when the door is closed. If the door is not closed properly, the door latch may not engage.\n###\nQ:{}\nA:".format(question),
                                        temperature=0.3,
                                        max_tokens=50,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0,
                                        stop=["\n"]
                                        )
                        answer = gpt3_response['choices'][0]['text']
                    else:                        
                        qa_dict[i]['Answer Description'] = "Answer found in the user manual"
                    qa_dict[i]['Answer'] = answer
                    # qa_dict[i]['Selected documents'] = response['selected_documents']
                    # print(str(i) + ")" + "Question: " + question)
                    # print(str(i) + ")" + "Answer: " + response['answers'][0] + "\n______________________________________________________________\n")
                    # print(response)
                except Exception as e:
                    print(e)
                i += 1
        
        return qa_dict
    
    def save_result_json(self, qa_dict):
        t = time.localtime()
        current_time = time.strftime("%m_%d_%H_%M", t)
        with open("results/Q&A_" + "_" + current_time + ".json", 'a+') as json_file:
            json.dump(qa_dict, json_file)
        print("Your Q&A is ready to use!")
        return current_time

    def create_file(self):
        response = openai.File.create(
            file=open("resources/manuals/temp.jsonl"),
            purpose='answers'
        )
        return response['id']
    
    def save_result_txt(self, qa_dict):
        lines = []
        for item in qa_dict.values():
            s = "Q: " + item["Question"] + "\n" + "A: " + item["Answer"] + "\n" + "___________________________________________________\n"
            lines.append(s)
        with open("results/Q&A_result" + ".txt", 'a+') as txt_file:
            for line in lines:
                txt_file.write(line)


def main():
    print("Please upload manuals in 'manuals' folder(.pdf, .json, .txt)!")
    amount = input("Chose an amount of 6x question sets to generate:\n")
    m = Formatter()
    m.format_manuals()
    print("Manuals are ready to use!")
    print("Connecting to GPT-3")
    b = Bot()
    file_id = b.create_file()
    questions = b.create_questions(amount)
    qa_dict = b.create_answers(questions, file_id=file_id)
    b.save_result_json(qa_dict)
    b.save_result_txt(qa_dict)
    input()


# for el in openai.File.list()['data']:
#     openai.File.delete(el['id'])



# print(response)

# time.sleep(10)

# print(openai.File.list())



# print(response)




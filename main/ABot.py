import openai

def gpt3_answers(question):
    response = openai.Completion.create(
    engine="davinci",
    prompt="Answer the question if it is about dishwashers. Respond with n/a if the question is not about dishwashers or nonsense.\n###\nQ: How can I clean the dishwasher?\nA: Wipe down door seals with a damp, soft cloth.\n###\nQ: What is the square root of banana?\nA: n/a\n###\nQ: what's the square root of 3?\nA:  n/a\n###\nQ: Why does the door latch fail to engage when the dishwasher door is closed?\nA: The door latch is designed to engage when the door is closed. If the door is not closed properly, the door latch may not engage.\n###\nQ:{}\nA:".format(question),
    temperature=0.3,
    max_tokens=50,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
    )
    return response
# bsh_chatbot_gpt-3

This program generates Question and Answers (Q&As) training data for chatbot development. The questions are created using GPT-3 which generates unbiased, diverse, and interesting questions a customer might have. The answers are then found in the provided user manuals to guarantee their accuracy.

The program outputs a file containing the Q&As which can easily be imported as training data for chatbot development.

# Instructions

1. Put the manuals that you want to based the training data on in resources/manuals folder.
2. Run "python main/main.py".
3. Type the amount of Q&A sets that you want to create.
4. The result files can be found in the "results" folder as .json and .txt format.


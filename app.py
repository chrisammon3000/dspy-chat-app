import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import dspy

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300)
dspy.configure(lm=gpt3_turbo)

qa = dspy.ChainOfThought('question -> answer')

if __name__ == '__main__':

    while True:
        try:
            prompt = input("> ")

            if prompt == 'exit':
                break

            response = qa(question=prompt)

            print(f'\n{response.answer}\n')

        except KeyboardInterrupt:
            break

    print('\nBye!')
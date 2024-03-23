import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import dspy

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300)
dspy.configure(lm=gpt3_turbo)

if __name__ == '__main__':

    while True:
        try:
            prompt = input("> ")

            if prompt == 'exit':
                break

            response = gpt3_turbo(prompt)[0]

            print(f'\n{response}\n')
        except KeyboardInterrupt:
            break
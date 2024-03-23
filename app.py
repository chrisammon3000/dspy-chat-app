import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import dspy

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300)
dspy.configure(lm=gpt3_turbo)

class AIMessage(dspy.Signature):
    """Respond to the user's message"""

    message = dspy.InputField(desc="The user's message")
    response = dspy.OutputField(desc="Your response")

respond = dspy.ChainOfThought(AIMessage)


if __name__ == '__main__':

    while True:
        try:
            prompt = input("> ")

            if prompt == 'exit':
                break

            response = respond(message=prompt)

            print(f'\n{response.response}\n')

        except KeyboardInterrupt:
            break

    print('\nBye!')
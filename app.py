import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
import dspy

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300)
dspy.configure(lm=gpt3_turbo)

class ResponseWithContext(dspy.Signature):
    """Respond to the user's message"""

    context = dspy.InputField(desc="The context of the conversation")
    message = dspy.InputField(desc="The user's message")
    response = dspy.OutputField(desc="Your response")

respond = dspy.ChainOfThought(ResponseWithContext)


if __name__ == '__main__':

    context = []
    while True:
        try:
            interaction = {}

            prompt = input("> ")
            if prompt == 'exit':
                break

            interaction.update({'message': prompt})

            response = respond(
                context=context,
                message=prompt
                )
            
            interaction.update({'response': response.response})
            
            print(f'\n{response.response}\n')

        except KeyboardInterrupt:
            break

    print('\nBye!')
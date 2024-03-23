import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
from src.chat import respond_cot, UserInteraction, ConversationContext, gpt3_turbo


if __name__ == '__main__':

    context = ConversationContext(window_size=5)
    while True:
        try:
            interaction = UserInteraction()

            interaction.message = input(">>> ")

            if interaction.message == ':exit':
                break
            elif interaction.message == ':history':
                print(context.render())
                continue
            elif interaction.message == ':inspect':
                print(gpt3_turbo.inspect_history())
                continue

            interaction.response = respond_cot(
                context=context.render(),
                message=interaction.message
                ).response
                        
            print(f'\n<<< {interaction.response}\n')

            context.update(interaction)

        except KeyboardInterrupt:
            break

    print('\nBye!')
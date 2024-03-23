import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv());
from datetime import datetime
from pydantic import BaseModel
import dspy

gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300)
dspy.configure(lm=gpt3_turbo)

class ResponseWithContext(dspy.Signature):
    """Respond to the user's message"""

    context = dspy.InputField(desc="The context of the conversation")
    message = dspy.InputField(desc="The user's message")
    response = dspy.OutputField(desc="A useful response to the user's message within the context of the conversation")

respond_cot = dspy.ChainOfThought(ResponseWithContext)

local_tz = str(datetime.now().astimezone().tzinfo)
def get_timestamp(local_tz=local_tz):
    return datetime.now().astimezone().isoformat()[:-9] + local_tz

class UserInteraction(BaseModel):
    message: str = None
    response: str = None

    def serialize_by_role(self):
        return [
            {
                "role": "user",
                "content": f"{self.message}"
            },
            {
                "role": "assistant",
                "content": f"{self.response}"
            }
        
        ]

class ConversationContext(BaseModel):
    window_size: int = 3
    content: list[UserInteraction] = []

    @staticmethod
    def _format_interaction(interaction):
        return f"User: {interaction.message}\n\nAssistant: {interaction.response}\n\n"

    def render(self):
        formatted = [
            self._format_interaction(interaction)
            for interaction in self.content
        ]

        return "".join(formatted)
    
    def update(self, interaction: UserInteraction):
        # Keep the last `window_size` interactions
        self.content = self.content[-self.window_size:] + [interaction]

    def __str__(self):
        return self.render()

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

            interaction.response = respond_cot(
                context=context.render(),
                message=interaction.message
                ).response
                        
            print(f'\n<<< {interaction.response}\n')

            context.update(interaction)

        except KeyboardInterrupt:
            break

    print('\nBye!')
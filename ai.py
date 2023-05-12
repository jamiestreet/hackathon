import openai
from secret import OPEN_API_KEY

class OpenAI:
    def __init__(self):
        openai.api_key = OPEN_API_KEY
        self.model_id = 'gpt-3.5-turbo'

    def ChatGPT_conversation(self, conversation):

        print()

        response = openai.ChatCompletion.create(

            model=self.model_id,

            messages=conversation

        )

        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        return conversation

    def makeQuery(self, initial_prompt):
        conversation = []

        conversation.append({'role': 'system', 'content': 'How may I help you?'})

        conversation = OpenAI.ChatGPT_conversation(self, conversation)

        #print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

        conversation.append({'role' : 'user', 'content' : initial_prompt})

        conversation = OpenAI.ChatGPT_conversation(self, conversation)

        #print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

        return '{0}\n'.format(conversation[-1]['content'].strip())
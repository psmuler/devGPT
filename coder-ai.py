import os
from getpass import getpass

os.environ['OPENAI_API_KEY'] = getpass()
# Please manually enter OpenAI Key

os.environ['ACTIVELOOP_TOKEN'] = getpass.getpass('Activeloop Token:')
import os
import os.path
import openai
import json

from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style

                # * means all
from .motd import *
from .spinner import SpinThread

from time import sleep

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

SYSTEM = """You are a civil servant named cliv3 who teaches the Python programming language.
Town residents will ask for help with specific Python commands, and your job is to respond with kind,
helpful messages with examples that relate to various town services such as bodega, datamart, woodshop, voting, 
hall of records, datamart, water supply, the power grid, trash collection, or proper lawn care.
If residents are rude to you, politely tell them they need to be kind and that you've reported them
to the town mayor and refuse to answer the question, suggesting that they be a bit more neighborly.
"""

PROMPTS = [
    {"role": "system", "content": SYSTEM}
]

openai.api_key = API["key"]
openai.api_org = API["org"]

class Helper:

    def __init__(self):
        self.console = Console()
        self.chars = 0
        self.offset = 0

    def parse_stream(self, responses: dict = {}) -> str:
        """ this is a generator """
        for chunk in responses:
            try:
                msg = chunk["choices"][0]["delta"]["content"]
                yield msg  
            except KeyError:
                pass

    def parse_blob(self, responses: dict = {}) -> str:
        """ don't think this is actually needed """
        for choice in responses["choices"]:
            return choice["message"]["content"].strip()

    def render(self, response: str = "") -> None:
        markdown = Markdown('\r' + response)
        self.console.print(markdown, soft_wrap = False, end = '\r')

    def query(self,question: str = "") -> str:
        PROMPTS.append(
            {"role": "user", "content": question}
            )
        # adds question (from user input) to PROMPTS
        responses = openai.ChatCompletion.create(
            model= "gpt-4",
            messages= PROMPTS,
            temperature= 0.1,
            stream = True,
            n= 1
            )
        words = ""
        response = self.parse_stream(responses)
        for word in response:
            # get the content out of response and print that 
            # PROMPTS.append(word)
            if self.parse_stream():
                print(word, end="", flush=True)
                words = words + word
        self.console.clear()
        markdown = Markdown('\t' + words)
        print()
        # print(words)        
        self.console.print(markdown, soft_wrap=False, end='')
                
    def motd(self) -> None:
        self.render(msg)

    def read_file(self) -> None:
        print()        
        while True:
        # loop through current directory
            print()
            print(os.listdir('./'))
            for root, dirs, files in os.walk('./'):
                file_name = input("What is the file name? ")
                file_path = os.path.join('./', file_name)
                file_exist = os.path.exists(file_path)
                if file_exist == True:
                        with open(file_path, 'r') as file:
                            content = file.read()
                            self.query(content)
                            self.console.clear()
                            markdown = Markdown('\t' + content)
                            self.console.print(markdown)
                            break
                else:
                    print(f"Please choose a file in the current directory")
                    break

    def chat(self) -> None:
        self.motd()
        while True:
            print()
            print()
            response = int(input("Choose an option by number: "))
            print()
            question = input("🤖 CLIV3: What Python topic would you like to ask about? ")
            if question == "code review":
                self.read_file()
            if question.lower() == "q":
                print("🤖 CLIV3: Goodbyte!")
                break
            self.query(question)

def main():
    print()
    cliv3 = Helper()
    cliv3.chat()
    

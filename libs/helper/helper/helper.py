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
        folder_name = input("What is the folder name? ")
        file_name = input("What is the file name? ")
        file_path = os.path.join(folder_name, file_name)
        file_exist = os.path.exists(file_path)

        # root_dir = folder_name
        # for dir_path, dir_names, file_names in os.walk(root_dir):
        #     for name in file_names:
        #         new_path = os.path.join(root, name)

        while file_exist == False:
            ''' if file not in folder then add subfolder to file path '''
            try:
                inputs = [folder_name, file_name]
                sub_folder = input("What is the subfolder name? ")
                add_input = inputs.append(sub_folder)
                new_path = str(input + ',')
                file_paths = os.path.join(new_path)
                file_exists = os.path.exists(file_paths)
                dir_exists = os.path.isdir(sub_folder)
                is_file = os.path.isfile(file_paths)
                with open(file_paths, 'r') as file:
                    content = file.read()
                    self.query(content)
                    self.console(clear)
                    markdown = Markdown('\t' + content)
                    self.console.print(markdown)
            except:
                """ currently only allows for one subfolder input, otherwise user recieves below error """
                print(f"It looks like '{file_name}' does not exist in '{folder_name}' or '{sub_folder}'")
                break 

            #     folder_input = input("What is the subfolder name? ")
            #     new_path = str(folder_input) + ' ,'
            #     file_pathss = os.path.join(folder_name, sub_folder, subb_folder, file_name)
            #     file_exists = os.path.exists(file_pathss)
            #     dir_exists = os.path.isdir(subb_folder)
            #     is_file = os.path.isfile(file_pathss)
            #     with open(file_pathss, 'r') as file:
            #         content = file.read()
            #         self.query(content)
            #         self.console(clear)
            #         markdown = Markdown('\t' + content)
            #         self.console.print(markdown)
        
        else: 
            with open(file_path, 'r') as file:
                content = file.read() 
                self.query(content) 
                self.console.clear()
                markdown = Markdown('\t' + content)
                self.console.print(markdown)
        # folder_files = os.listdir(folder_name)
        # print(folder_files)
        # if folder
        #     file_name = input("What is the file name? ")
        #     file_path = os.path.join(folder_name, file_name)
        #     with open(file_path, 'r') as file:
        #         content = file.read()
        #         self.query(content)
        #         self.console(clear)
        #         markdown = Markdown('\t' + content)
        #         self.console.print(markdown)

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
    

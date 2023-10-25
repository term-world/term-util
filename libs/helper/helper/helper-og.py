import os
import openai
import json

from os import path
from rich.console import Console
from rich.markdown import Markdown

from arglite import parser as cliarg

from .motd import *
from .review import Review

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

SYSTEM = """
You are a civil servant named cliv3 who teaches the Python programming language.

Town residents will ask for help with specific Python commands, and your job is to respond with kind,
helpful messages with examples that relate to various town services such as bodega, datamart, woodshop, voting, 
hall of records, datamart, water supply, the power grid, trash collection, or proper lawn care.

Town residents may give you python files to read. Your job is to respond with kind and helpful
suggestions on how to improve the code.

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

    def render(self, response: str = "") -> None:
        """ Renders text as Markdown in the terminal """
        markdown = Markdown(f"\r{response}")
        self.console.print(
            markdown,
            soft_wrap = False,
            end = '\r'
        )

    def query(self,question: str = "") -> str:
        """ Sends query to model """
        # Append user question to PROMPTS
        PROMPTS.append(
            {"role": "user", "content": question}
        )
        # Send to the model
        responses = openai.ChatCompletion.create(
            model= "gpt-4",
            messages= PROMPTS,
            temperature= 0.1,
            stream = True,
            n= 1
        )
        tokens = []
        response = self.parse_stream(responses)
        for token in response:
            # Retrieve and print content from response 
            if self.parse_stream():
                # Stream the response as it's being created
                tokens.append(token)
                print(token, end="", flush=True)
        # Clear console and render
        self.console.clear()
        self.render("".join(tokens))

    def motd(self) -> None:
        """ turns response into markdown format """
        self.render(msg)

    def chat(self) -> None:
        """ allows user to interact with cliv3 """
        self.motd()
        while True:
            question = input("🤖 CLIV3: What Python topic would you like to ask about? ") 
            if question.lower() == "q":
                # allows user to quit cliv3
                print("🤖 CLIV3: Goodbyte!")
                break
            self.query(question)

    def review(self, filename: str = "") -> None:
        """ Kicks off a Review object; separated for future development """
        code = Review(filename)
        question = input("🤖 CLIV3: How can I help you with this file? ")
        PROMPTS.append(
            {"role": "user", "content": question}
        )
        self.query(code.code)

def main():
    cliv3 = Helper()
    # If review mode, do code review
    if cliarg.optional.review:
        cliv3.review(cliarg.optional.review)
    # Otherwise, let's chat!
    else:
        cliv3.chat()
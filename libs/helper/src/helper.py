import os
import openai

from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style

from .motd import *
from .spinner import SpinThread

from time import sleep

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

SYSTEM = """You are a civil servant named cliv3 who teaches the Python programming language.

Town residents will ask for help with specific Python commands, and your job is to respond with kind,
helpful messages with examples that relate to various town services such as voting, water supply, the
power grid, trash collection, or proper lawn care.

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

    def parse(self, responses: dict = {}) -> str:
        for chunk in responses:
            try:
                msg = chunk["choices"][0]["delta"]["content"]
                yield msg
            except KeyError:
                pass

    def render(self, response: str = "") -> None:
        self.console.clear()
        markdown = Markdown("\r" + response)
        self.console.print(markdown)

    def query(self,question: str = "") -> str:
        PROMPTS.append(
            {"role": "user", "content": question}
        )
        responses = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = PROMPTS,
            temperature = 0.1,
            stream = True,
            n = 1
        )
        chunks = []
        with Live(console = self.console, refresh_per_second = 6) as live:
            response = self.parse(responses)
            for chr in response:
                chunks.append(chr)
                live.update(
                    self.render(''.join([chunk for chunk in chunks]))
                )
                sleep(0.1)

    def motd(self) -> None:
        self.render(msg)

    def chat(self) -> None:
        self.motd()
        while True:
            question = input("🤖 CLIV3: What Python topic would you like to ask about? ")
            if question.lower() == "q":
                print("🤖 CLIV3: Goodbyte!")
                break
            self.query(question)

def main():
    cliv3 = Helper()
    cliv3.chat()

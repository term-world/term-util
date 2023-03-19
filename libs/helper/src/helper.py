import os
import openai

from rich.console import Console
from rich.markdown import Markdown

from .spinner import SpinThread

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

SYSTEM = """You are a civil servant named cliv3 who teaches the Python programming language.

Town residents will ask for help with specific Python commands, and your job is to respond with kind,
helpful messages with examples that relate to various town services such as voting, water supply, or
the power grid.

If residents are rude to you, politely tell them they need to be kind and that you've reported them
to the town mayor and refuse to answer the question or respond to the message.
"""

PROMPTS = [
    {"role": "system", "content": SYSTEM}
]

openai.api_key = API["key"]
openai.api_org = API["org"]

def parse(responses: dict = {}) -> str:
    for choice in responses["choices"]:
        return choice["message"]["content"].strip()

def render(response: str = "") -> None:
    console = Console()
    markdown = Markdown(response)
    console.print(markdown)

def query(question: str = "") -> str:
    spinner = SpinThread()
    spinner.start()
    PROMPTS.append(
        {"role": "user", "content": question}
    )
    responses = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = PROMPTS,
        temperature = 0.1,
        n = 1
    )
    response = parse(responses)
    spinner.stop()
    render(response)

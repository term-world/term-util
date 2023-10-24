import os
import openai
import json

from os import path
from rich.console import Console
from rich.markdown import Markdown

from arglite import parser as cliarg

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

openai.api_key = API["key"]
openai.api_org = API["org"]

class Persona:

    def __init__(self, system: str = "", greeting: str = ""):
        self.console = Console()
        self.chars = 0
        self.offset = 0
        self.prompts = []
        self.set_persona_greet(greeting)
        self.set_system_prompt(system)
        self.user_question_string = ">>> "

    def __is_prompted(self) -> bool:
        for value in self.prompts:
            if value["role"] == "system":
                return True
        return False

    def set_system_prompt(self, prompt: str = "") -> None:
        if prompt:
            self.prompts.append(
                {"role": "system", "content": prompt}
            )

    def set_persona_greet(self, greeting: str = "") -> None:
        if greeting:
            self.greeting = greeting

    def parse_stream(self, responses: dict = {}) -> str:
        """ Generator creating chunks from read stream """
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
        self.prompts.append(
            {"role": "user", "content": question}
        )
        # Send to the model
        responses = openai.ChatCompletion.create(
            model= "gpt-4",
            messages= self.prompts,
            temperature= 0.1,
            stream = True,
            n = 1
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
        self.render(self.greeting)

    def chat(self) -> None:
        """ Allows user to carry on a chat with the Persona """
        # Outward-facing user greeting dialog. This is _not_ the system prompt.
        self.motd()
        # Checks if a system prompt has been provided; if not, inform and bail
        if not self.__is_prompted():
            print("I have no system prompt. Perhaps my creator should give me one.")
            return
        while True:
            question = input(self.user_question_string) 
            if question.lower() == "q":
                self.query("Goodbye.")
                break
            self.query(question)

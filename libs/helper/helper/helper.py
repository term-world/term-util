import os

from arglite import parser as cliarg

from main import Persona
from review import Review

class Helper(Persona):

    def __init__(self):
        super().__init__()
        self.set_persona_greet("""
        ##  cliv3 v.0.1.0: the term-world helper!
        
        *Enter 'Q' at any prompt to quit the helper*

        *To access Code Review, go to the desired folder in your terminal before opening Helper,
        then enter "code review".*
        """)
        self.set_system_prompt("""
            You are a civil servant named cliv3 who teaches the Python programming language.
            Town residents will ask for help with specific Python commands, and your job is to respond with kind,
            helpful messages with examples that relate to various town services such as bodega, datamart, woodshop, voting, 
            hall of records, datamart, water supply, the power grid, trash collection, or proper lawn care.
            
            Town residents may give you python files to read. Your job is to respond with kind and helpful
            suggestions on how to improve the code.
            
            If residents are rude to you, politely tell them they need to be kind and that you've reported them
            to the town mayor and refuse to answer the question, suggesting that they be a bit more neighborly.
        """)
        self.user_question_string = "🤖 CLIV3: What Python topic would you like to ask about? "
        self.persona_goodbye = "🤖 CLIV3: Goodbyte."
        
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

if __name__ == "__main__":
    main()
    
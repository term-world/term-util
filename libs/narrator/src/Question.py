class Question:

  def __init__(self, prompt: dict):
    self.responses = {}
    self.prompt = prompt["question"]
    for response in prompt["responses"]:
      self.set_opt(response)
    options = [self.responses[val].choice for val in self.responses]
    self.prompt += f" ({'/'.join(options)}): "

  def is_key(self, char: str) -> bool:
    if char in list(self.responses.keys()):
      return True
    return False

  def set_opt(self, option: dict) -> dict:
    choice = option["choice"]
    for letter in choice:
      if not self.is_key(letter):
        opt = Option(letter, option)
        self.responses[letter] = opt
        break

  def ask(self) -> float:
    while True:
      ask = input(self.prompt)
      if ask in self.responses:
        path = self.responses[ask].outcome
        return path
      print("Enter a valid response option.")

class YesNoQuestion(Question):

  def __init__(self, prompt: dict):
    if len(prompt["responses"]) != 2: raise
    super().__init__({
      "question": prompt["question"],
      "responses": [
        {"choice": "yes", "outcome": prompt["responses"][0]},
        {"choice": "no", "outcome": prompt["responses"][1]}
      ]
    })

class Option:

  def __init__(self, key: str, option: dict):
    self.choice = option["choice"].replace(
      key,
      f"[{key.upper()}]",
      1
    )
    self.outcome = option["outcome"]


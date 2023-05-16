import narrator

n = narrator.Narrator()
n.narrate()

q = narrator.Question(
  {
    "question": "Yo, Nah, or Sha",
    "responses": [
      {"choice": "yo", "outcome": {"act":"yo","scene":"statement"}},
      {"choice": "nah", "outcome": {"act":"nah","scene":"statement"}},
      {"choice": "sha", "outcome": {"act":"sha","scene":"short"}}
    ]
  }
)

n.path.change(q.ask())
n.narrate()

q = narrator.Question(
  {
    "question": "How many, bruh?",
    "responses": [
      {"choice": "1", "outcome": {"act":"bruh","scene":"short","scenes": 1}},
      {"choice": "2", "outcome": {"act":"bruh","scene":"short","scenes": 2}},
      {"choice": "3", "outcome": {"act":"bruh","scene":"short","all": True}}
    ]
  }
)

result = q.ask()
n.path.change(result)
n.narrate(**result)

q = narrator.YesNoQuestion(
  {
    "question":"Yes or no?",
    "outcomes": [
      {"act":"yo","scene":"statement"},
      {"act":"nah","scene":"statement"}
    ]
  }
)

n.path.change(q.ask())

n.narrate(all = True)

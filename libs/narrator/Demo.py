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

# TODO: Make this variable; i.e. any number of frames from question,
#       default 1
for _ in range(2):
  n.narrate()

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

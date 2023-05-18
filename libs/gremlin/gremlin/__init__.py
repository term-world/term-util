from .npc import *

API = {
    "key": os.getenv("OPEN_AI_KEY"),
    "org": os.getenv("OPEN_AI_ORG")
}

openai.api_key = API["key"]
openai.api_org = API["org"]
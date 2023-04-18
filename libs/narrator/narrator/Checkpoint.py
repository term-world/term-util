import os
import json

from .Path import *

def exists(filepaths: list) -> bool:
  for file in filepaths:
    if not os.path.exists(file):
      return False
  return True

def set_flag(flag: str, val:int = 1) -> None:
  flags = {}
  if not exists([".flags"]):
    with open(".flags", "w+") as fh:
      fh.write("{}")
  with open(".flags", "r+") as fh:
    flags = json.load(fh)
  flags[flag] = val
  with open(".flags", "w") as fh:
    json.dump(flags, fh, indent=2)

def check_flag(flag: str):
  flags = {}
  try:
    with open(".flags", "r+") as fh:
      flags = json.load(fh)
    return flags[flag]
  except:
    return False

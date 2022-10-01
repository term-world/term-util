#! /usr/bin/python

import sys
import click
import requests

URL = "https://raw.githubusercontent.com/term-world/world-building/main/"

def gitignore(lang:str = "python") -> str:
  file = requests.get(
    f"{URL}{lang}.gitignore"
  )
  return file.text

@click.group()
def create():
  pass

@create.command()
def assignment():
  ignore = gitignore()
  with open(".gitignore", "w") as fh:
    fh.write(ignore)
  with open(".flags", "w") as fh:
    fh.write("{}")
  with open(".events", "w") as fh:
    fh.write("#! /bin/bash")
  with open(".gatorgrade.yml") as fh:
    fh.write("")

if __name__ == "__main__":
  create(prog_name='create')

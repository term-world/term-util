import yaml
from time import sleep

from .Path import Path

class Narrator:

  def __init__(self):
    fh = open(".paths.yml")
    self.paths = yaml.safe_load(fh)
    self.path = Path()

  def narrate(self, all: bool = False):
    lines = []
    chosen_path = self.paths[self.path.number]
    if all:
      for scenes in list(chosen_path.values()):
        lines += scenes
    else:
      lines = chosen_path[self.path.scene]
    for line in lines:
      print(line)
      sleep(1)
    self.path.scene += 1

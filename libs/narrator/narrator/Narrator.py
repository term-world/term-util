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

    chosen_path = self.paths[self.path.act] if self.path.act in self.paths else list(self.paths)[0]
    print(chosen_path)
    if all:
      for scenes in list(chosen_path.values()):
        lines += scenes
    else:
      lines = chosen_path[self.path.scene] if self.path.scene in chosen_path.values() else list(self.paths.values())[0]

    for line in lines:
      print(line)
      sleep(1)

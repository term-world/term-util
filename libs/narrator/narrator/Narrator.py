import yaml
from time import sleep

from .Path import Path

class Narrator:

  def __init__(self):
    fh = open(".paths.yml")
    self.paths = yaml.safe_load(fh)
    self.path = Path(list(self.paths.keys())[0],list(self.paths.values())[0])

  def narrate(self, all: bool = False):
    lines = []
    acts = list(self.paths)

    chosen_path = self.paths[self.path.act] if self.path.act in acts else self.paths[acts[0]]

    if all:
      for scenes in list(chosen_path.values()):
        lines += scenes
    else:
      scenes = list(chosen_path)
      lines = chosen_path[self.path.scene] if self.path.scene in scenes else chosen_path[scenes[0]]

    for line in lines:
      print(line)
      sleep(1.5)

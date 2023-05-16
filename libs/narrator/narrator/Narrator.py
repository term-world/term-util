import yaml
from time import sleep

from .Path import Path

class Narrator:

  def __init__(self):
    fh = open(".paths.yml")
    self.paths = yaml.safe_load(fh)
    self.path = Path(
        paths = {
          "act": list(self.paths.keys())[0],
          "scene": list(self.paths.values())
        }
    )

  def narrate(self, all: bool = False):
    lines = []
    acts = list(self.paths)
    
    # Try to choose a given path, if key exists
    try:
        chosen_path = self.paths[self.path.act] 
    except KeyError:
        chosen_path = self.paths[acts[0]]
    
    if all:
      for scenes in list(chosen_path.values()):
        lines += scenes
    else:
      scenes = list(chosen_path)
      try:
        lines = chosen_path[self.path.scene]
      except KeyError:
        lines = chosen_path[scenes[0]]

    for line in lines:
      print(line)
      sleep(1.5)

    self.path.get_next_scene(self.paths)

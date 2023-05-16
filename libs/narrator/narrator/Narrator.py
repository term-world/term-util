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
          "scene": list(self.paths.values())[0]
        }
    )

  def narrate(self, **kwargs):
    lines = []
    acts = list(self.paths)
    
    # Try to choose a given path, if key exists
    try:
        chosen_path = self.paths[self.path.act] 
    except KeyError:
        chosen_path = self.paths[acts[0]]
    
    if "all" in kwargs and kwargs["all"] == True:
      # Play all scenes
      for scenes in list(chosen_path.values()):
        lines += scenes
    elif "scenes" in kwargs:
        try:
          scenes = int(kwargs["scenes"])
        except ValueError:
          print("ERROR: Scene value is not an integer!")
          exit()
        if scenes < len(chosen_path.values()):
          for idx in range(scenes):
            lines += chosen_path.values()[idx]
    else:
      # Play one
      try:
        lines = chosen_path[self.path.scene]
      except KeyError:
        scenes = list(chosen_path)
        lines = chosen_path[scenes[0]]

    for line in lines:
      print(line)
      sleep(1.5)

    self.path.get_next_scene(self.paths)

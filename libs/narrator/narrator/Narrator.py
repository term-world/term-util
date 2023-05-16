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
      # From the current scene, play a number of scenes specified
      try:
        scenes = int(kwargs["scenes"])
      except ValueError:
        print("ERROR: Scene count is not a number!!")
        exit()
      try:
        scene_location = list(chosen_path.keys()).index(self.path.scene)
        for idx in range(scene_location, scene_location + scenes):
          lines += list(chosen_path.values())[idx]
      except IndexError:
        # If we go beyond the scene boundary, just stop.
        pass
    else:
      # Play only one scene from the selected point
      try:
        lines = chosen_path[self.path.scene]
      except KeyError:
        scenes = list(chosen_path)
        lines = chosen_path[scenes[0]]

    for line in lines:
      print(line)
      sleep(1.5)

    self.path.get_next_scene(self.paths)

from itertools import islice

class Path:

  def __init__(self, paths: dict = {}):
    """ Constructor """
    self.act = paths["act"]
    self.scene = list(paths["scene"].keys())[0]

  def get_next_scene(self, paths: dict):
    """ If there's another scene to go to, well, go to it! """
    scenes = list(
        paths[self.act]
    )
    try:
        idx = scenes.index(self.scene)
    except ValueError:
        return
    idx += 1
    if(idx < len(scenes)):
        self.scene = scenes[idx]

  def change(self, path: dict = {"act": 1, "scene": 1}):
    """ Change a scene in a currently-running path """
    self.act = path["act"]
    self.scene = path["scene"]
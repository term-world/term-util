class Path:

  def __init__(self, paths: dict = {}):
    """ Constructor """
    self.act = paths["act"]
    self.scene = list(list(paths["scene"])[0].keys())[0]

  def get_next_scene(self, paths):
    scenes = list(
        paths[self.act]
    )
    idx = scenes.index(self.scene)
    if(idx + 1 <= len(scenes)):
        self.scene = paths[self.act][scenes[idx+1]]

  def change(self, path: dict = {"act": 1, "scene": 1}):
    """ Change a scene in a currently-running path """
    self.act = path["act"]
    self.scene = path["scene"]
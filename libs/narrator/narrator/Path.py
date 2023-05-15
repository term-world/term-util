from collections import namedtuple

class Path:

  def __init__(self, act: str = "act", scene: str = "intro"):
    self.act = act
    self.scene = scene

  def next_scene(self):
    self.scene += 1

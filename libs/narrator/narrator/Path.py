from collections import namedtuple

class Path:

  def __init__(self, act: str, scene: str):
    self.act = act
    self.scene = scene

  def next_scene(self):
    self.scene += 1

  def change(self, path):
    self.act = path["act"]
    self.scene = path["scene"]

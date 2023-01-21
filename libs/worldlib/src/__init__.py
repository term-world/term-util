# System libraries
import os
import narrator
from glob import glob

# term-world libraries
import inventory
from narrator.Checkpoint import check_flag
from narrator.Checkpoint import set_flag
from inventory.Item import FixtureSpec
from inventory.Item import ItemSpec
from inventory.Item import BoxSpec

# term-world objects
try:
    n = narrator.Narrator()
except Exception as e:
    print(e)

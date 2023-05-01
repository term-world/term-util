import json
import sys
import os

class PowerGrid:

    def add_power(wind = 0, solar = 0, coal = 0, oil = 0, nuclear = 0, natural_gass = 0):
        # sorts power based on its source and adds it to the power grid
        path = os.path.dirname(__file__)
        renewable_energy = wind + solar
        exhaustable_energy = coal + oil + nuclear + natural_gass
        with open(f"{path}/worldbattery.json", "r") as fh:
            world_battery = json.load(fh)
            world_battery["renewable_energy"] += renewable_energy
            world_battery["exhaustable_energy"] += exhaustable_energy
        with open(f"{path}/worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)

        # Takes a perameter that is the ammount of power it takes to run the object
    def use_power(power):
        path = os.path.dirname(__file__)
        with open(f"{path}/worldbattery.json", "r") as fh:
            world_battery = json.load(fh)

        if world_battery["renewable_energy"] >= power:
            world_battery["renewable_energy"] -= power
            print("You Can Feel Good Knowing This Was Powered By Renewable Energy! ")
        elif world_battery["exhaustable_energy"] >= power:
            world_battery["exhaustable_energy"] -= power
            print("Hope you are happy.  You powered it, but now the earth is a little more polluted.")
            print("🏭")
        elif world_battery["renewable_energy"] < power and world_battery["exhaustable_energy"] < power:
            print("There Is Not Enough Power In The World. Generate Some More And Try Again. ")
            sys.exit()

        with open(f"{path}/worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)
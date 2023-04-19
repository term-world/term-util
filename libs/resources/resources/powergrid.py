import json

class PowerGrid:

    def add_power(wind = 0, solar = 0, coal = 0, oil = 0, nuclear = 0, natural_gass = 0):
        with open("worldbattery.json", "r") as fh:
            
            world_battery = json.load(fh)
            world_battery["power"] += int(wind)
            world_battery["power"] += solar
            world_battery["power"] += coal
            world_battery["power"] += oil
            world_battery["power"] += nuclear
            world_battery["power"] += natural_gass
        with open("worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)

        #make an if statement to keep from going to 0
    def use_power(power):
        with open("../term-util-power-planters/libs/resources/resources/worldbattery.json", "r") as fh:
            world_battery = json.load(fh)
            world_battery["power"] -= power
        with open("../term-util-power-planters/libs/resources/resources/worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)


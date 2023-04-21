import json

class PowerGrid:

    def add_power(wind = 0, solar = 0, coal = 0, oil = 0, nuclear = 0, natural_gass = 0):
        #more generalizable way to do this path
        renewable_energy = wind + solar
        exhaustable_energy = coal + oil + nuclear + natural_gass
        with open("../../term-util-power-planters/libs/resources/resources/worldbattery.json", "r") as fh:
            world_battery = json.load(fh)
            world_battery["renewable_energy"] += renewable_energy
            world_battery["exhaustable_energy"] += exhaustable_energy
        with open("../../term-util-power-planters/libs/resources/resources/worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)

        #make an if statement to keep from going to 0
    def use_power(power):
        with open("../term-util-power-planters/libs/resources/resources/worldbattery.json", "r") as fh:
            world_battery = json.load(fh)
        if world_battery["power"] >= power:
            world_battery["power"] -= power
        else:
            print("There It Not Enough Power In The World To Run This! ")
        with open("../term-util-power-planters/libs/resources/resources/worldbattery.json", "w") as add_battery:
            json.dump(world_battery, add_battery)


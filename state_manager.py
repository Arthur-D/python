from gametest import *



class StateManager:
    def __init__(self):
        self.turn = 0
        self.turns_left_building_queue = 0

        self.air_purifier_amount = 0
        self.house_amount = 0
        self.robot_factory_amount = 0
        self.water_purifier_amount = 0

        self.air_purifier_amountStringVar = StringVar()
        self.house_amountStringVar = StringVar()
        self.robot_factory_amountStringVar = StringVar()
        self.water_purifier_amountStringVar = StringVar()
        self.turn_numberStringVar = StringVar()
        self.turn_numberStringVar.set("Turn %s" % self.turn)
        self.turns_left_building_queueStringVar = StringVar()


    def set_turn(self, turn):
        self.turn = turn
        self.set_StringVars()


    def set_turns_left_building_queue(self, turns):
        self.turns_left_building_queue = turns
        self.set_StringVars()


    def set_air_purifier_amount(self, amount):
        print("amount in StateManager.set_air_purifier_amount(): ", amount)
        self.air_purifier_amount = amount


    def set_house_amount(self, amount):
        self.house_amount = amount


    def set_robot_factory_amount(self, amount):
        self.robot_factory_amount = amount


    def set_water_purifier_amount(self, amount):
        self.water_purifier_amount = amount


    # Sets all StringVars.
    def set_StringVars(self):
        self.turn_numberStringVar.set("Turn %s" % self.turn)

        self.air_purifier_amountStringVar.set("Air purifiers: %s" % self.air_purifier_amount)
        self.house_amountStringVar.set("Houses: %s" % self.house_amount)
        self.robot_factory_amountStringVar.set("Robot factories: %s" % self.robot_factory_amount)
        self.water_purifier_amountStringVar.set("Water purifiers: %s" % self.water_purifier_amount)


    # def set_StringVars(self, stringvar):
    #     self.StringVars[stringvar] = StringVar()
    #     print("self.StringVars in StateManager.set_StringVars(): ", self.StringVars)
    #     print("self.StringVars[0] in StateManager.set_StringVars(): ", self.StringVars[stringvar].get())
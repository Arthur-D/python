from gametest import *



class StateManager:
    def __init__(self):
        self.turn_number = 1
        self.turns_left_building_queue = 0

        self.energy_resource = 100

        self.air_purifier_amount = 0
        self.house_amount = 0
        self.robot_factory_amount = 0
        self.water_purifier_amount = 0

        self.confirm_function = None


    def set_turn_number(self, turn_number):
        self.turn_number = turn_number


    def set_turns_left_building_queue(self, turns):
        self.turns_left_building_queue = turns


    def set_energy_resource(self, amount):
        self.energy_resource = amount


    def set_air_purifier_amount(self, amount):
        self.air_purifier_amount = amount


    def set_house_amount(self, amount):
        self.house_amount = amount


    def set_robot_factory_amount(self, amount):
        self.robot_factory_amount = amount


    def set_water_purifier_amount(self, amount):
        self.water_purifier_amount = amount


    def set_confirm_function(self, confirm_function):
        self.confirm_function = confirm_function

from tkinter import StringVar



# Class managing all turns.
class TurnManager():
    def __init__(self):
        self.turn = 0
        self.turns_left_building_queue = 0
        self.turns_left_current_building = 0

        self.turn_numberStringVar = StringVar()
        self.turn_numberStringVar.set("Turn %s" % self.turn)
        self.turns_left_building_queueStringVar = StringVar()
        self.turns_left_current_buildingStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Decreases the amount of turns for the foremost building in the queue if End turn button is pressed.
    def decrease_building_turns(self):
        if self.queuemanager.building_queue:
            building = self.queuemanager.building_queue[self.buildingmanager.get_currently_building_index()]
            building.decrease_turns()
            self.set_turns_left_current_building()
            self.set_turns_left_building_queue()
            self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % building.get_turns())
            if building.get_turns() == 0:
                self.buildingmanager.add_built()


    # Logic for displaying how many turns are left to build the whole building queue.
    def set_turns_left_building_queue(self):
        turn_amount = 0
        for index, building in enumerate(self.queuemanager.building_queue):
            if index != self.buildingmanager.get_currently_building_index():
                turn_amount += building.get_turns()
            else:
                turn_amount += self.turns_left_current_building
        self.turns_left_building_queue = turn_amount
        if len(self.queuemanager.building_queue) > 0:
            self.turns_left_building_queueStringVar.set("Turns left for\nbuilding queue: %s" % self.turns_left_building_queue)
        else:
            self.turns_left_building_queueStringVar.set("")
        print("Turns left for building queue: ", self.turns_left_building_queue)


    # Logic for displaying how many turns are left building the foremost building in the queue.
    def set_turns_left_current_building(self):
        if self.queuemanager.building_queue:
            building = self.buildingmanager.get_currently_building()
            self.turns_left_current_building = building.get_turns()
            self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % self.turns_left_current_building)
        else:
            self.turns_left_current_buildingStringVar.set("")


    # Increments the global turn counter. See GameLogic.run_simulation() for the other things happening when clicking End turn.
    def increase_game_turns(self):
        if self.turn < 100:
            self.turn += 1
            self.turn_numberStringVar.set("Turn %s" % self.turn)
            print("Turn", self.turn)

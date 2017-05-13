from tkinter import StringVar



# Class managing all turns.
class TurnManager():
    def __init__(self):
        self.turn = 0
        self.turns_left_building_queue = 0

        self.turn_numberStringVar = StringVar()
        self.turn_numberStringVar.set("Turn %s" % self.turn)
        self.turns_left_building_queueStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Decreases the amount of turns for the foremost building in the queue if End turn button is pressed.
    def decrease_building_turns(self):
        if self.queuemanager.building_queue:
            building = self.queuemanager.building_queue[self.buildingmanager.get_currently_building_index()]
            building.decrease_turns()
            self.set_turns_left_building_queue()
            if building.get_turns() == 0:
                self.buildingmanager.add_built()


    # Logic for displaying how many turns are left to build the whole building queue.
    def set_turns_left_building_queue(self):
        turn_amount = 0
        for index, building in enumerate(self.queuemanager.building_queue):
            turn_amount += building.get_turns()
        self.turns_left_building_queue = turn_amount
        if len(self.queuemanager.building_queue) > 0:
            self.turns_left_building_queueStringVar.set("Turns left for\nbuilding queue: %s" % self.turns_left_building_queue)
        else:
            self.turns_left_building_queueStringVar.set("")
        print("Turns left for building queue: ", self.turns_left_building_queue)


    # Increments the global turn counter. See GameLogic.run_simulation() for the other things happening when clicking End turn.
    def increase_game_turns(self):
        if self.turn < 100:
            self.turn += 1
            self.turn_numberStringVar.set("Turn %s" % self.turn)
            print("Turn", self.turn)

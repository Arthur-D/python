from tkinter import StringVar



# Class managing all turns.
class TurnManager():
    def __init__(self):
        self.turn_numberStringVar = StringVar()
        self.turns_left_building_queueStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Decreases the amount of turns for the foremost building in the queue if End turn_number button is pressed.
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
        self.statemanager.set_turns_left_building_queue(turn_amount)
        if len(self.queuemanager.building_queue) > 0:
            self.turns_left_building_queueStringVar.set(
                "Turns left for\nbuilding queue: %s" % self.statemanager.turns_left_building_queue)
        else:
            self.turns_left_building_queueStringVar.set("")


    # Increments the global turn_number counter. See GameLogic.run_simulation() for the other things happening when clicking End turn.
    def increase_game_turns(self):
        turn_number = self.statemanager.turn_number
        turn_number += 1
        self.statemanager.set_turn_number(turn_number)
        self.turn_numberStringVar.set("Turn %s" % self.statemanager.turn_number)
        if self.guimanager.confirmButton.winfo_viewable():
            print("Aborting action needing confirmation")
            self.guimanager.abort()
        self.guimanager.building_queueListbox.see(len(self.queuemanager.building_queue) - 1)
        print("Turn", self.statemanager.turn_number)

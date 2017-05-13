from gui_manager import *
from queue_manager import *
from tkinter import *
from turn_manager import *
from building_manager import *



# The initializing function. Also contains references to setters in a specific order so as to make the various classes aware of each other.
def main():
    root = Tk()
    gamelogic = GameLogic()
    queuemanager = QueueManager()
    turnmanager = TurnManager()
    buildingmanager = BuildingManager()

    gamelogic.set_turnmanager(turnmanager)
    gamelogic.set_buildingmanager(buildingmanager)
    queuemanager.set_buildingmanager(buildingmanager)
    queuemanager.set_turnmanager(turnmanager)
    turnmanager.set_buildingmanager(buildingmanager)
    turnmanager.set_queuemanager(queuemanager)
    buildingmanager.set_turnmanager(turnmanager)
    buildingmanager.set_queuemanager(queuemanager)

    app = GUI(root, gamelogic, buildingmanager, queuemanager, turnmanager)
    root.mainloop()



# High level class getting the simulation started.
class GameLogic():
    def __init__(self):
        self.playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    # This defines what happens when clicking End turn.
    def run_simulation(self):
        self.turnmanager.increase_game_turns()
        self.turnmanager.decrease_building_turns()
        self.buildingmanager.set_building_queue_turns()


    # Logic for saving playername to labels in GUI.
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        saving_name = str(self.playernameStringVar.get())
        if saving_name != "":
            saved_nameLabel.grid()
            self.saved_playernameStringVar.set(saving_name)
            error_playernameLabel.grid_remove()
        else:
            error_playernameLabel.grid()
            saved_nameLabel.grid_remove()



if __name__ == "__main__":
    main()

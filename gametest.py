from gui_manager import *
from queue_manager import *
from tkinter import *
from tkinter import ttk
from turn_manager import *
from building_manager import *
from save_manager import *
from stringvar_manager import *



# The initializing function. Also contains references to setters in a specific order so as to make the various classes aware of each other.
def main():
    root = Tk()
    gamelogic = GameLogic()
    stringvarmanager = StringVarManager()
    queuemanager = QueueManager()
    turnmanager = TurnManager()
    buildingmanager = BuildingManager()
    savemanager = SaveManager()
    # guimanager = GUI(Frame, gamelogic, buildingmanager, queuemanager, turnmanager, savemanager)

    # gamelogic.set_guimanager(guimanager)
    gamelogic.set_turnmanager(turnmanager)
    gamelogic.set_buildingmanager(buildingmanager)
    gamelogic.set_savemanager(savemanager)
    gamelogic.set_stringvarmanager(stringvarmanager)
    queuemanager.set_buildingmanager(buildingmanager)
    queuemanager.set_turnmanager(turnmanager)
    turnmanager.set_buildingmanager(buildingmanager)
    turnmanager.set_queuemanager(queuemanager)
    buildingmanager.set_turnmanager(turnmanager)
    buildingmanager.set_queuemanager(queuemanager)
    buildingmanager.set_stringvarmanager(stringvarmanager)
    savemanager.set_gamelogic(gamelogic)
    savemanager.set_buildingmanager(buildingmanager)
    savemanager.set_stringvarmanager(stringvarmanager)

    app = GUI(root, gamelogic, buildingmanager, queuemanager, turnmanager, savemanager)
    root.mainloop()



# High level class getting the simulation started.
class GameLogic():
    def __init__(self):
        self.playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()
        self.save_nameStringVar = StringVar()
        self.save_nameStringVar.set("gametest_save")

        # self.savemanager.set_saved_games()


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_savemanager(self, savemanager):
        self.savemanager = savemanager


    def set_stringvarmanager(self, stringvarmanager):
        self.stringvarmanager = stringvarmanager


    # This defines what happens when clicking End turn.
    def run_simulation(self):
        self.turnmanager.increase_game_turns()
        self.turnmanager.decrease_building_turns()
        self.buildingmanager.set_building_queue_turns()


    # Logic for saving playername to labels in GUI.
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        self.saving_name = str(self.playernameStringVar.get())
        if self.saving_name != "":
            saved_nameLabel.grid()
            self.saved_playernameStringVar.set("Welcome, %s" % self.saving_name)
            error_playernameLabel.grid_remove()
        else:
            error_playernameLabel.grid()
            saved_nameLabel.grid_remove()


    def save_game(self, saved_gamesCombobox):
        self.save_name = str(self.save_nameStringVar.get())
        if self.save_name != "":
            self.savemanager.save_game_state(self.save_name)
            print("Saving game as %s" % self.save_name)
            self.savemanager.set_saved_games()
            self.set_saved_games(saved_gamesCombobox)
        else:
            print("Error saving game: name empty!")


    def set_saved_games(self, saved_gamesCombobox):
        self.savemanager.set_saved_games()
        saved_gamesCombobox["values"] = self.savemanager.get_saved_games()


    def select_saved_game(self, saved_gamesCombobox):
        selection = saved_gamesCombobox.current()
        saved_gamesCombobox.select_clear()


    def load_game(self, saved_gamesCombobox):
        selection = saved_gamesCombobox.current()
        if selection > -1:
            save_game = self.savemanager.saved_games[selection]
            stringvar = "self.buildingmanager.air_purifier_amountStringVar"
            self.savemanager.load_game_state(save_game)
            self.savemanager.set_game_state()
            print("Loading save '%s'" % save_game)
            # SaveManager.set_game_state(self)
        else:
            print("Select a save game!")



if __name__ == "__main__":
    main()

from gui_manager import *
from queue_manager import *
from tkinter import *
from tkinter import ttk
from turn_manager import *
from building_manager import *
from resource_manager import *
from save_manager import *
from state_manager import *



# The initializing function. Also contains references to setters in a specific order so as to make the various classes aware of each other.
def main():
    root = Tk()
    gamelogic = GameLogic()
    statemanager = StateManager()
    queuemanager = QueueManager()
    turnmanager = TurnManager()
    buildingmanager = BuildingManager(statemanager)
    resourcemanager = ResourceManager()
    savemanager = SaveManager()

    gamelogic.set_turnmanager(turnmanager)
    gamelogic.set_buildingmanager(buildingmanager)
    gamelogic.set_resourcemanager(resourcemanager)
    gamelogic.set_savemanager(savemanager)
    gamelogic.set_statemanager(statemanager)
    gamelogic.set_queuemanager(queuemanager)

    queuemanager.set_buildingmanager(buildingmanager)
    queuemanager.set_resourcemanager(resourcemanager)
    queuemanager.set_turnmanager(turnmanager)

    turnmanager.set_buildingmanager(buildingmanager)
    turnmanager.set_statemanager(statemanager)
    turnmanager.set_queuemanager(queuemanager)

    buildingmanager.set_resourcemanager(resourcemanager)
    buildingmanager.set_turnmanager(turnmanager)
    buildingmanager.set_queuemanager(queuemanager)

    resourcemanager.set_statemanager(statemanager)

    savemanager.set_gamelogic(gamelogic)
    savemanager.set_buildingmanager(buildingmanager)
    savemanager.set_resourcemanager(resourcemanager)
    savemanager.set_statemanager(statemanager)
    savemanager.set_turnmanager(turnmanager)
    savemanager.set_queuemanager(queuemanager)

    app = GUI(root, gamelogic, buildingmanager, queuemanager, turnmanager, resourcemanager, savemanager, statemanager)
    buildingmanager.set_guimanager(app)
    gamelogic.set_guimanager(app)
    savemanager.set_guimanager(app)
    turnmanager.set_guimanager(app)
    queuemanager.set_guimanager(app)
    root.mainloop()



# High level class getting the simulation started.
class GameLogic():
    def __init__(self):
        self.playernameStringVar = StringVar()
        self.error_playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()
        self.save_nameStringVar = StringVar()
        self.save_nameStringVar.set("gametest_save")


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_savemanager(self, savemanager):
        self.savemanager = savemanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # This defines what happens when clicking End turn_number.
    def run_simulation(self):
        if self.statemanager.turn_number < 100:
            self.turnmanager.increase_game_turns()
            self.resourcemanager.increase_energy_resource()
            self.turnmanager.decrease_building_turns()
            self.queuemanager.set_building_queue_names()
            # self.buildingmanager.set_building_queue_turns()
        else:
            print("Turn number is 100, game over")


    # Logic for saving playername to labels in GUI.
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        self.saving_name = str(self.playernameStringVar.get())
        if self.saving_name == "":
            self.error_playernameStringVar.set("Enter a name!")
            error_playernameLabel.grid()
        elif len(self.saving_name) > 8:
            self.error_playernameStringVar.set("Name can't be more\nthan 8 characters")
            error_playernameLabel.grid()
        else:
            self.saved_playernameStringVar.set(self.saving_name)
            saved_nameLabel.grid()
            error_playernameLabel.grid_remove()


    def save_game(self, saved_gamesCombobox):
        self.save_name = str(self.save_nameStringVar.get())
        if self.save_name not in self.savemanager.saved_games:
            if self.save_name != "":
                self.savemanager.save_game_state(self.save_name)
                self.set_saved_games(saved_gamesCombobox)
            else:
                print("Error saving game: name empty!")
        else:
            self.guimanager.show_confirm_and_abortButton()
            self.statemanager.set_confirm_function("save_game")


    def set_saved_games(self, saved_gamesCombobox):
        self.savemanager.set_saved_games()
        saved_gamesCombobox["values"] = self.savemanager.get_saved_games()
        print("savemanager.get_saved_games() in GameLogic.set_saved_games(): ", self.savemanager.get_saved_games())


    def select_saved_game(self, saved_gamesCombobox):
        saved_gamesCombobox.select_clear()


    def load_game(self, saved_gamesCombobox):
        selection = saved_gamesCombobox.current()
        if selection > -1:
            save_game = self.savemanager.saved_games[selection]
            self.savemanager.load_game_state(save_game)
            self.savemanager.set_game_state()
            print("Loading save '%s'" % save_game)
        else:
            print("Select a save game!")


    def delete_saved_game(self, saved_gamesCombobox):
        save_game = self.savemanager.saved_games[saved_gamesCombobox.current()]
        self.savemanager.delete_saved_game(save_game)
        self.set_saved_games(saved_gamesCombobox)



if __name__ == "__main__":
    main()

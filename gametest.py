import threading
from os import execl
from sys import executable

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
    buildingmanager = BuildingManager()
    resourcemanager = ResourceManager()
    savemanager = SaveManager()
    saveandloadgui = SaveAndLoadGUI(root, savemanager)

    gamelogic.set_turnmanager(turnmanager)
    gamelogic.set_buildingmanager(buildingmanager)
    gamelogic.set_resourcemanager(resourcemanager)
    gamelogic.set_root(root)
    gamelogic.set_savemanager(savemanager)
    gamelogic.set_statemanager(statemanager)
    gamelogic.set_queuemanager(queuemanager)

    queuemanager.set_buildingmanager(buildingmanager)
    queuemanager.set_resourcemanager(resourcemanager)
    queuemanager.set_turnmanager(turnmanager)

    turnmanager.set_buildingmanager(buildingmanager)
    turnmanager.set_statemanager(statemanager)
    turnmanager.set_queuemanager(queuemanager)

    buildingmanager.set_gamelogic(gamelogic)
    buildingmanager.set_resourcemanager(resourcemanager)
    buildingmanager.set_statemanager(statemanager)
    buildingmanager.set_turnmanager(turnmanager)
    buildingmanager.set_queuemanager(queuemanager)

    resourcemanager.set_statemanager(statemanager)

    savemanager.set_gamelogic(gamelogic)
    savemanager.set_buildingmanager(buildingmanager)
    savemanager.set_resourcemanager(resourcemanager)
    savemanager.set_root(root)
    savemanager.set_saveandloadgui(saveandloadgui)
    savemanager.set_statemanager(statemanager)
    savemanager.set_turnmanager(turnmanager)
    savemanager.set_queuemanager(queuemanager)

    app = GUI(root, gamelogic, buildingmanager, queuemanager, turnmanager, resourcemanager, savemanager, statemanager, saveandloadgui)
    buildingmanager.set_guimanager(app)
    gamelogic.set_guimanager(app)
    savemanager.set_guimanager(app)
    turnmanager.set_guimanager(app)
    queuemanager.set_guimanager(app)
    root.mainloop()



# Object for creating threads. Not in use and may be deleted later.
class ThreadObject (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        print("Starting ", self.name)
        if __name__ == "__main__":
            main()
        # print("Exiting ", self.name)



# High level class getting the simulation started.
class GameLogic():
    def __init__(self):
        self.game_statusStringVar = StringVar()
        self.playernameStringVar = StringVar()
        self.error_playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_root(self, root):
        self.root = root


    def set_savemanager(self, savemanager):
        self.savemanager = savemanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    def start_new_game(self):
        # restart_thread = ThreadObject(1, "RestartThread", 1)
        # restart_thread.start()
        # self.root.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)


    # This defines what happens when clicking End turn_number.
    def run_simulation(self):
        if self.statemanager.turn_number < 100:
            self.turnmanager.increase_game_turns()
            self.resourcemanager.increase_energy_resource()
            self.turnmanager.decrease_building_turns()
            self.queuemanager.set_building_queue_names()
            if self.guimanager.confirmButton.winfo_viewable():
                print("Aborting action needing confirmation")
                self.guimanager.abort()
            self.guimanager.building_queueListbox.see(len(self.queuemanager.building_queue) - 1)
            self.buildingmanager.building_errorStringVar.set("")
        else:
            print("Turn number is 100, game over")


    def set_game_statusStringVar(self, color, content):
        self.guimanager.game_statusLabel.grid()
        self.guimanager.game_statusLabel["foreground"] = color
        self.game_statusStringVar.set(content)
        self.root.after(5000, lambda: self.guimanager.game_statusLabel.grid_remove())


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



if __name__ == "__main__":
    main()

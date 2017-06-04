import shelve
import os
from state_manager import *



class SaveManager:
    def __init__(self):
        self.saved_games = []


    def set_gamelogic(self, gamelogic):
        self.gamelogic = gamelogic


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Populates the saved_games list with the files found in Saves directory. Only adds files with no file ending or .dat files since under Windows there are 3 files generated by saving and just one without file ending under Linux.
    def set_saved_games(self):
        if os.path.exists("Saves"):
            for filename in os.listdir("Saves/"):
                if filename in self.saved_games or filename[:-4] in self.saved_games:
                    print("Skipping file ", filename)
                else:
                    if "." not in filename:
                        self.saved_games.append(filename)
                        print("Adding %s to saved games list" % filename)
                    elif filename.endswith(".dat"):
                        self.saved_games.append(filename[:-4])
                        print("Adding %s to saved games list" % filename[:-4])
        else:
            print("No Saves directory found!")


    def get_saved_games(self):
        return self.saved_games


    # Function for deleting a save game. Only deletes files in the saved_games list with no file extension or with the Windows save game file extensions.
    def delete_saved_game(self, save_name):
        if save_name in self.saved_games:
            print("Deleting save '%s'" % save_name)
            self.saved_games.remove(save_name)
            if os.path.exists("Saves/%s" % save_name):
                os.remove("Saves/%s" % save_name)
            if os.path.exists("Saves/%s.bak" % save_name):
                os.remove("Saves/%s.bak" % save_name)
            if os.path.exists("Saves/%s.dat" % save_name):
                os.remove("Saves/%s.dat" % save_name)
            if os.path.exists("Saves/%s.dir" % save_name):
                os.remove("Saves/%s.dir" % save_name)
            self.gamelogic.set_game_statusStringVar("red", "Deleted save \n{}".format(save_name))
        else:
            print("Can't find save '%s' in saved games list; not deleting!" % save_name)


    # For saving games. Makes sure there's a Saves folder to put them in. For Linux, one file without file extension is generated, while under Windows it will create .dat .dir and .bak files.
    def save_game_state(self, save_name):
        if not os.path.exists("Saves"):
            print("Creating Saves folder")
            os.mkdir("Saves")
        print("Saving game as %s" % save_name)
        saveFile = shelve.open("Saves/%s" % save_name)
        saveFile["StateManager.turn_number"] = self.statemanager.turn_number
        saveFile["StateManager.energy_resource"] = self.statemanager.energy_resource
        saveFile["GUIManager.building_amountsStringVar"] = self.guimanager.building_amountsStringVar.get()

        saveFile["QueueManager.building_queue"] = self.queuemanager.building_queue
        saveFile["GameLogic.playernameStringVar"] = self.gamelogic.saved_playernameStringVar.get()
        saveFile.close()
        self.gamelogic.set_game_statusStringVar("green", "Saved game \n{}".format(save_name))


    # Loads a game from the saved_games list and sets temporary variables. See set_game_state for setting the game's variables.
    def load_game_state(self, save_name):
        saveFile = shelve.open("Saves/%s" % save_name)
        try:
            self.turn_number = saveFile["StateManager.turn_number"]
            self.energy_resource = saveFile["StateManager.energy_resource"]
            self.building_amountsStringVar = saveFile["GUIManager.building_amountsStringVar"]

            self.building_queue = saveFile["QueueManager.building_queue"]
            self.saved_playernameStringVar = saveFile["GameLogic.playernameStringVar"]
        except KeyError:
            print("Could not load save {}".format(save_name))
            self.gamelogic.set_game_statusStringVar("red", "Could not load save\n{}".format(save_name))
        else:
            self.set_game_state()
            self.gamelogic.set_game_statusStringVar("green", "Loaded save\n{}".format(save_name))
        finally:
            saveFile.close()


    # Sets the game state again after loading a game. Also resets GUI StringVars.
    def set_game_state(self):
        self.statemanager.set_turn_number(self.turn_number)
        self.statemanager.set_energy_resource(self.energy_resource)
        self.queuemanager.set_finished_buildings()
        self.queuemanager.set_building_queue(self.building_queue)
        self.queuemanager.set_building_queue_names()
        self.guimanager.set_building_queue_turns()
        self.turnmanager.set_turns_left_building_queue()
        self.guimanager.set_building_construction()
        self.guimanager.set_building_queueScrollbar_visibility()

        # Resetting the labels when loading.
        self.turnmanager.turn_numberStringVar.set("Turn %s" % self.statemanager.turn_number)
        self.resourcemanager.energy_resourceStringVar.set("Energy: {}".format(self.statemanager.energy_resource))
        self.guimanager.building_amountsStringVar.set(self.building_amountsStringVar)
        self.buildingmanager.built_buildingStringVar.set("")
        self.buildingmanager.building_descriptionStringVar.set("")
        self.gamelogic.playernameStringVar.set("")
        self.gamelogic.saved_playernameStringVar.set(self.saved_playernameStringVar)

import shelve
import os
import datetime
import pdb
from tkinter import StringVar



class SaveManager:
    def __init__(self):
        self.saved_games = []
        self.save_name = ""

        self.confirm_function = None

        self.saved_gamesStringVar = StringVar()
        self.save_nameStringVar = StringVar()
        self.saved_game_infoStringVar = StringVar()


    def set_gamelogic(self, gamelogic):
        self.gamelogic = gamelogic


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_root(self, root):
        self.root = root


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_saveandloadgui(self, saveandloadgui):
        self.saveandloadgui = saveandloadgui


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    def set_confirm_function(self, confirm_function):
        self.confirm_function = confirm_function


    def confirm(self):
        selection_id = self.saveandloadgui.get_selection_saved_game()
        if self.confirm_function == "delete_saved_game":
            self.delete_saved_game(self.saved_games[selection_id])
        elif self.confirm_function == "save_game":
            self.save_game_state(self.save_name)
        self.set_saved_game_infoStringVar()
        self.abort()


    def abort(self):
        self.set_confirm_function(None)
        self.saveandloadgui.confirmButton.grid_remove()
        self.saveandloadgui.abortButton.grid_remove()


    def set_save_name_from_selection(self, selection):
        if self.saveandloadgui.get_selection_saved_game() != None:
            selection_id = self.saved_games[self.saveandloadgui.get_selection_saved_game()]
            self.save_nameStringVar.set(selection_id)
            self.set_saved_game_infoStringVar()


    def save_game_main_window(self):
        print("self.save_name in SaveManager.save_game_main_window(): ", self.save_name)
        if self.save_name == "":
            self.saveandloadgui.set_save_load_window()
        elif self.save_name not in self.saved_games:
            self.saveandloadgui.set_save_load_window()
            print("self.save_name, self.saved_games in SaveManager.save_game_main_window(): ", self.save_name, self.saved_games)
        else:
            self.save_game_state(self.save_name)


    def save_game(self):
        self.save_name = str(self.save_nameStringVar.get())
        if self.save_name not in self.saved_games:
            if self.save_name != "":
                self.save_game_state(self.save_name)
                self.set_saved_games()
            else:
                print("Error saving game: name empty!")
                self.saveandloadgui.set_save_statusStringVar("red", "Save name empty")
        else:
            self.saveandloadgui.show_confirm_and_abortButton()
            self.set_confirm_function("save_game")


    def load_game(self):
        if self.saveandloadgui.get_selection_saved_game() != None:
            selection_id = self.saved_games[self.saveandloadgui.get_selection_saved_game()]
            print("Loading save '{}'".format(selection_id))
            self.load_game_state(selection_id)
        else:
            print("Select a save game!")
            self.saveandloadgui.set_save_statusStringVar("red", "Select a save game")


    def delete_game(self):
        if self.saveandloadgui.get_selection_saved_game() != None:
            # selection_id = self.saveandloadgui.get_selection_saved_game()
            self.saveandloadgui.show_confirm_and_abortButton()
            self.set_confirm_function("delete_saved_game")
        else:
            print("Select a save game!")
            self.saveandloadgui.set_save_statusStringVar("red", "Select a save game")


    def set_saved_game_infoStringVar(self):
        saved_game_info = ""
        if self.saveandloadgui.get_selection_saved_game() != None:
            saveFile = shelve.open("Saves/{}".format(self.saved_games[self.saveandloadgui.get_selection_saved_game()], flag = "r"))
            try:
                if saveFile["GameLogic.playernameStringVar"] != "":
                    saved_game_info += "{}\n".format(saveFile["GameLogic.playernameStringVar"])
                else:
                    saved_game_info += "No playername\n"
                saved_game_info += "{:%d.%m.%Y %H.%M}\n".format(saveFile["DateAndTime"])
                saved_game_info += "Turn: {}".format(saveFile["StateManager.turn_number"])
            except KeyError:
                saved_game_info = "Could not load info"
            finally:
                saveFile.close()
        self.saved_game_infoStringVar.set(saved_game_info)


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
        saves = ""
        for save in self.saved_games:
            saves += "{}\n".format(save)
        self.saved_gamesStringVar.set(saves)
        self.saveandloadgui.set_saved_gamesScrollbar_visibility()


    def get_saved_games(self):
        return self.saved_games


    # Function for deleting a save game. Only deletes files in the saved_games list with no file extension or with the Windows save game file extensions.
    def delete_saved_game(self, save_name):
        extensions = ["", ".bak", ".dat", ".dir"]
        for extension in extensions:
            if os.path.exists("Saves/{}{}".format(save_name, extension)):
                try:
                    os.remove("Saves/{}{}".format(save_name, extension))
                except OSError as error:
                    print("Removal failed with: {}{}".format(save_name, extension), error.strerror)
                else:
                    print("Deleted file {}{}".format(save_name, extension))
        self.saveandloadgui.set_selection_saved_game(self.saved_games.index(save_name))
        self.saved_games.remove(save_name)
        self.saveandloadgui.set_save_statusStringVar("red", "Deleted save {}".format(save_name))
        self.set_saved_games()


    # For saving games. Makes sure there's a Saves folder to put them in. For Linux, one file without file extension is generated, while under Windows it will create .dat .dir and .bak files.
    def save_game_state(self, save_name):
        if not os.path.exists("Saves"):
            print("Creating Saves folder")
            os.mkdir("Saves")
        print("Saving game as %s" % save_name)
        saveFile = shelve.open("Saves/%s" % save_name)
        saveFile["DateAndTime"] = datetime.datetime.now()
        saveFile["StateManager.turn_number"] = self.statemanager.turn_number
        saveFile["StateManager.energy_resource"] = self.statemanager.energy_resource
        saveFile["GUIManager.building_amountsStringVar"] = self.guimanager.building_amountsStringVar.get()

        saveFile["QueueManager.building_queue"] = self.queuemanager.building_queue
        saveFile["GameLogic.playernameStringVar"] = self.gamelogic.saved_playernameStringVar.get()
        saveFile.close()
        print("Saved game as {}".format(save_name))
        if self.saveandloadgui.save_load_window.winfo_exists() == 1:
            self.saveandloadgui.set_save_statusStringVar("green", "Saved game {}".format(save_name))
        else:
            self.guimanager.set_game_statusStringVar("green", "Saved game {}".format(save_name))


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
            self.saveandloadgui.set_save_statusStringVar("red", "Could not load save {}".format(save_name))
        else:
            self.set_game_state()
            self.guimanager.set_game_statusStringVar("green", "Loaded save\n{}".format(save_name))
            if self.saveandloadgui.save_load_window.winfo_exists() == 1:
                self.saveandloadgui.close_save_load_window()
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

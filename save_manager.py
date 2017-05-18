import shelve
import os
from tkinter import StringVar
from state_manager import *



class SaveManager:
    def __init__(self):
        self.saved_games = []


    def set_gamelogic(self, gamelogic):
        self.gamelogic = gamelogic


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def set_saved_games(self):
        if os.path.exists("Saves"):
            for filename in os.listdir("Saves/"):
                if filename in self.saved_games or filename[:-4] in self.saved_games:
                    print("Skipping file ", filename)
                else:
                    if "." not in filename:
                        self.saved_games.append(filename)
                        print("Adding %s to saved games list" % filename)
                    else:
                        self.saved_games.append(filename[:-4])
                        print("Adding %s to saved games list" % filename[:-4])
        else:
            print("No Saves directory found!")


    def get_saved_games(self):
        return self.saved_games


    def delete_saved_game(self, save_name):
        if save_name in self.saved_games or save_name[:-4] in self.saved_games:
            print("Deleting save '%s'" % save_name)
            self.saved_games.remove(save_name)
            if os.path.exists("Saves/%s" % save_name):
                os.remove("Saves/%s" % save_name)
            elif os.path.exists("Saves/%s.dat" % save_name):
                os.remove("Saves/%s.dat" % save_name)
        else:
            print("Can't find save '%s' in saved games list; not deleting!" % save_name)


    def save_game_state(self, save_name):
        if not os.path.exists("Saves"):
            os.mkdir("Saves")
        saveFile = shelve.open("Saves/%s" % save_name)
        saveFile["StateManager.air_purifier_amount"] = self.statemanager.air_purifier_amount
        saveFile["StateManager.house_amount"] = self.statemanager.house_amount
        saveFile["StateManager.robot_factory_amount"] = self.statemanager.robot_factory_amount
        saveFile["StateManager.water_purifier_amount"] = self.statemanager.water_purifier_amount
        saveFile.close()


    def load_game_state(self, save_name):
        saveFile = shelve.open("Saves/%s" % save_name)
        self.air_purifier_amount = saveFile["StateManager.air_purifier_amount"]
        self.house_amount = saveFile["StateManager.house_amount"]
        self.robot_factory_amount = saveFile["StateManager.robot_factory_amount"]
        self.water_purifier_amount = saveFile["StateManager.water_purifier_amount"]
        saveFile.close()


    def set_game_state(self):
        self.statemanager.set_air_purifier_amount(self.air_purifier_amount)
        self.statemanager.set_house_amount(self.house_amount)
        self.statemanager.set_robot_factory_amount(self.robot_factory_amount)
        self.statemanager.set_water_purifier_amount(self.water_purifier_amount)
        self.statemanager.set_StringVars()

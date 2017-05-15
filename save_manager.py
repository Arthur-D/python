import shelve
import os
from tkinter import StringVar
from stringvar_manager import *



class SaveManager:
    def __init__(self):
        self.saved_games = []


    def set_gamelogic(self, gamelogic):
        self.gamelogic = gamelogic


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_stringvarmanager(self, stringvarmanager):
        self.stringvarmanager = stringvarmanager


    def set_saved_games(self):
        if os.path.exists("Saves"):
            for filename in os.listdir("Saves/"):
                if filename not in self.saved_games:
                    if filename.endswith(".dat"):
                        self.saved_games.append(filename[:-4])
                    else:
                        self.saved_games.append(filename)
        else:
            print("No Saves directory found!")


    def get_saved_games(self):
        return self.saved_games


    def save_game_state(self, save_name):
        if not os.path.exists("Saves"):
            os.mkdir("Saves")
        saveFile = shelve.open("Saves/%s" % save_name)
        # saveFile["SaveManager.saved_games"] = self.saved_games
        saveFile["BuildingManager.air_purifier_amount"] = self.buildingmanager.air_purifier_amount
        print("self.buildingmanager.air_purifier_amountStringVar.get() in SaveManager.save_game_state(): ", self.buildingmanager.air_purifier_amountStringVar.get())
        saveFile["BuildingManager.air_purifier_amountStringVar"] = self.buildingmanager.air_purifier_amountStringVar.get()
        saveFile.close()
        # self.set_saved_games()


    def load_game_state(self, save_name):
        saveFile = shelve.open("Saves/%s" % save_name)
        # self.saved_games = saveFile["SaveManager.saved_games"]
        self.air_purifier_amount = saveFile["BuildingManager.air_purifier_amount"]
        self.air_purifier_amountStringVar = saveFile["BuildingManager.air_purifier_amountStringVar"]
        saveFile.close()


    def set_game_state(self):
        print("self.air_purifier_amountStringVar in SaveManager.set_game_state(): ", self.air_purifier_amountStringVar)
        self.stringvarmanager.set_air_purifier_amountStringVar(self.air_purifier_amountStringVar)
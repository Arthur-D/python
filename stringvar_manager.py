from tkinter import StringVar
from gametest import *



class StringVarManager:
    def __init__(self):
        # self.content = content
        self.StringVars = {}
        self.air_purifier_amountStringVar = StringVar()
        # vars["name"] = self.StringVars = StringVar()


    def set_air_purifier_amountStringVar(self, content):
        print("content in StringVarManager.set_air_purifier_amountStringVar(): ", content)
        self.air_purifier_amountStringVar.set(content)


    # def set_StringVars(self, content):
    #     self.set_air_purifier_amountStringVar(content)


    # def set_StringVars(self, stringvar):
    #     self.StringVars[stringvar] = StringVar()
    #     print("self.StringVars in StringVarManager.set_StringVars(): ", self.StringVars)
    #     print("self.StringVars[0] in StringVarManager.set_StringVars(): ", self.StringVars[stringvar].get())

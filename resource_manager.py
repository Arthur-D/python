from tkinter import StringVar



class ResourceManager:
    def __init__(self):
        self.energy_resourceStringVar = StringVar()


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


    def increase_energy_resource(self):
        amount = self.statemanager.energy_resource + 5
        self.statemanager.set_energy_resource(amount)
        self.energy_resourceStringVar.set("Energy: {}".format(self.statemanager.energy_resource))


    def increase_resources(self, amount):
        self.statemanager.set_energy_resource(self.statemanager.energy_resource + amount)
        self.energy_resourceStringVar.set("Energy: {}".format(self.statemanager.energy_resource))

    def decrease_resources(self, amount):
        self.statemanager.set_energy_resource(self.statemanager.energy_resource - amount)
        self.energy_resourceStringVar.set("Energy: {}".format(self.statemanager.energy_resource))

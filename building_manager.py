from tkinter import StringVar



# Building object to derive from for all buildings. Also handles its own turns.
class Building():
    def __init__(self, properties):
        self.name = properties["Name"]
        self.turns = properties["Turn amount"]
        self.cost = properties["Cost"]


    def get_name(self):
        return self.name


    def get_turns(self):
        return self.turns


    def get_cost(self):
        return self.cost


    def decrease_turns(self):
        if self.turns > 0:
            self.turns -= 1
            if self.turns == 0:
                print("Building complete: ", self.name)



# Class for handling the buildings.
class BuildingManager:
    def __init__(self, statemanager):
        self.buildings_names = ""
        self.buildings_names_list = []
        self.building_turns = ""
        self.previous_building = ""
        self.finished_buildings = []
        self.finished_buildings_names = []
        self.finished_buildings_amounts = {}

        self.buildingsStringVar = StringVar()
        self.building_descriptionStringVar = StringVar()
        self.building_buildingStringVar = StringVar()
        self.building_building_turnsStringVar = StringVar()
        self.built_buildingStringVar = StringVar()
        self.building_amountsStringVar = StringVar()
        self.building_turnsStringVar = StringVar()
        self.air_purifier_amountStringVar = StringVar()
        self.house_amountStringVar = StringVar()
        self.robot_factory_amountStringVar = StringVar()
        self.water_purifier_amountStringVar = StringVar()

        self.statemanager = statemanager
        self.set_building_properties()
        self.set_building_turns()


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Sets initial properties for buildings and instanciates them.
    def set_building_properties(self):
        self.building_properties = [
            {"Name" : "Air purifier", "Turn amount" : 4, "Cost" : "80"},
            {"Name" : "House", "Turn amount" : 5, "Cost" : "25"},
            {"Name" : "Robot factory", "Turn amount" : 7, "Cost" : "200"},
            {"Name" : "Water purifier", "Turn amount" : 4, "Cost" : "80"}
        ]
        self.set_building_names()

        self.air_purifier = Building(properties = self.get_building_properties("Air purifier"))
        self.house = Building(properties = self.get_building_properties("House"))
        self.robot_factory = Building(properties = self.get_building_properties("Robot factory"))
        self.water_purifier = Building(properties = self.get_building_properties("Water purifier"))

        self.building_objects = [self.air_purifier, self.house, self.robot_factory, self.water_purifier]


    # Returns all the building properties if the building name correlates.
    def get_building_properties(self, name):
        for building in self.building_properties:
            if building["Name"] == name:
                return building
        return None


    def get_building_cost(self, name):
        for building in self.building_properties:
            if building["Name"] == name:
                return int(building["Cost"])
        return None


    # Returns the foremost building instance in the building queue.
    def get_currently_building(self):
        if self.queuemanager.building_queue:
            return self.queuemanager.building_queue[self.get_currently_building_index()]
        else:
            return None


    # Populate the list of possible buildings to build, both for display purposes and also in an actual list.
    def set_building_names(self):
        for building_property in self.building_properties:
            self.buildings_names += "{{{:15}{}}}\n".format(building_property["Name"], building_property["Turn amount"])
            self.buildings_names_list.append(building_property["Name"])
        self.buildingsStringVar.set(self.buildings_names)


    # For showing how many turns each building in the building list would take.
    def set_building_turns(self):
        for building_property in self.building_properties:
            self.building_turns += "%s" % (building_property["Turn amount"])
        self.building_turnsStringVar.set(self.building_turns)


    # Sets the building description of each building which shows up when browsing the building list.
    def set_building_description(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        if selection:
            selection_id = int(selection[0])
            if self.buildings_names_list[selection_id] == "Air purifier":
                self.building_descriptionStringVar.set("Air purifier\ncost: {}".format(self.get_building_cost("Air purifier")))
            elif self.buildings_names_list[selection_id] == "House":
                self.building_descriptionStringVar.set("House\ncost: {}".format(self.get_building_cost("House")))
            elif self.buildings_names_list[selection_id] == "Robot factory":
                self.building_descriptionStringVar.set("Robot factory\ncost: {}".format(self.get_building_cost("Robot factory")))
            elif self.buildings_names_list[selection_id] == "Water purifier":
                self.building_descriptionStringVar.set("Water purifier\ncost: {}".format(self.get_building_cost("Water purifier")))
            else:
                self.building_descriptionStringVar.set("")


    # Similar to set_buildings_list() but is for the buildings that are in the building queue.
    def set_building_queue_turns(self):
        building_queue_turns = ""
        for building in self.queuemanager.building_queue:
            building_queue_turns += "%s" % building.get_turns()
        self.building_building_turnsStringVar.set(building_queue_turns)


    # For getting the name of the foremost building in the queue.
    def get_currently_building_name(self):
        if self.queuemanager.building_queue:
            return self.queuemanager.building_queue[len(self.queuemanager.building_queue) - 1].get_name()


    # For getting the index of the foremost building in the queue.
    def get_currently_building_index(self):
        if self.queuemanager.building_queue:
            return len(self.queuemanager.building_queue) - 1


    # Sets what the previous building in the queue were, for showing what has just finished building.
    def set_previous_building(self):
        if self.get_currently_building_name():
            self.previous_building = self.get_currently_building_name()
        else:
            self.previous_building = None


    # Sets what building is currently being constructed for display purposes only.
    def set_building_construction(self):
        if self.get_currently_building_name():
            self.building_buildingStringVar.set("Building %s" % self.get_currently_building_name())
        else:
            self.building_buildingStringVar.set("")


    # Controls what happens when double clicking an item in the building list.
    def add_buildings(self):
        selection_id = self.guimanager.get_buildingsListbox_selection()
        print("selection_id in BuildingManager.add_buildings(): ", selection_id)
        if self.statemanager.energy_resource >= self.get_building_cost(self.buildings_names_list[selection_id]):
            self.resourcemanager.decrease_resources(self.get_building_cost(self.buildings_names_list[selection_id]))
            self.queuemanager.add_to_building_queue(selection_id)
            self.set_building_queue_turns()
            self.turnmanager.set_turns_left_building_queue()
            self.set_building_construction()
            self.guimanager.set_building_queueScrollbar_visibility()
        else:
            print("Insufficient energy to build!")


    # This defines what happens when finishing building something.
    def add_built(self):
        self.set_previous_building()
        if self.previous_building:
            self.built_buildingStringVar.set("Built %s" % self.previous_building)
        self.set_finished_buildings()
        self.queuemanager.remove_from_building_queue()
        self.set_building_construction()
        self.turnmanager.set_turns_left_building_queue()
        self.set_building_queue_turns()
        self.guimanager.set_building_queueScrollbar_visibility()


    def set_finished_buildings(self):
        if self.get_currently_building_index() != None:
            self.finished_buildings.append(self.queuemanager.building_queue[self.get_currently_building_index()])
        building_amounts = ""
        building_names = [building.get_name() for building in self.finished_buildings]
        for building_name in self.buildings_names_list:
            self.finished_buildings_amounts[building_name] = building_names.count(building_name)
            if building_name.endswith("y"):
                building_amounts += "{}ies:{:4}\n".format(building_name[:-1], building_names.count(building_name))
            else:
                building_amounts += "{}s:{:4}\n".format(building_name, building_names.count(building_name))
        self.building_amountsStringVar.set(building_amounts.rstrip("\n"))

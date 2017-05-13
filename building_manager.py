from tkinter import StringVar



# Building object to derive from for all buildings. Also handles its own turns.
class Building():
    def __init__(self, properties):
        self.name = properties["Name"]
        self.turns = properties["Turn amount"]


    def get_name(self):
        return self.name


    def get_turns(self):
        return self.turns


    def decrease_turns(self):
        if self.turns > 0:
            self.turns -= 1
            if self.turns == 0:
                print("Building complete: ", self.name)



# Class for handling the buildings.
class BuildingManager():
    def __init__(self):
        self.air_purifier_amount = 0
        self.house_amount = 0
        self.robot_factory_amount = 0
        self.water_purifier_amount = 0

        self.buildings_names = ""
        self.buildings_names_list = []
        self.building_turns = ""
        self.previous_building = ""

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

        self.set_building_properties()
        self.set_building_amountStringVars()
        self.set_building_turns()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Sets initial properties for buildings and instanciates them.
    def set_building_properties(self):
        self.building_properties = [{"Name" : "Air purifier", "Turn amount" : 4}, {"Name" : "House", "Turn amount" : 5}, {"Name" : "Robot factory", "Turn amount" : 7}, {"Name" : "Water purifier", "Turn amount" : 4}]
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


    # Returns the foremost building instance in the building queue.
    def get_currently_building(self):
        if self.queuemanager.building_queue:
            return self.queuemanager.building_queue[self.get_currently_building_index()]
        else:
            return None


    # Populate the list of possible buildings to build, both for display purposes and also in an actual list.
    def set_building_names(self):
        for building_property in self.building_properties:
            self.buildings_names += "{%s}\n" % (building_property["Name"])
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
                self.building_descriptionStringVar.set("Air purifier\ndescription")
            elif self.buildings_names_list[selection_id] == "House":
                self.building_descriptionStringVar.set("House\ndescription")
            elif self.buildings_names_list[selection_id] == "Robot factory":
                self.building_descriptionStringVar.set("Robot factory\ndescription")
            elif self.buildings_names_list[selection_id] == "Water purifier":
                self.building_descriptionStringVar.set("Water purifier\ndescription")
            else:
                self.building_descriptionStringVar.set("")


    # Sets the relevant StringVars for displaying how many buildings have been built.
    def set_building_amountStringVars(self):
        self.air_purifier_amountStringVar.set("Air purifiers: %s" % self.air_purifier_amount)
        self.house_amountStringVar.set("Houses: %s" % self.house_amount)
        self.robot_factory_amountStringVar.set("Robot factories: %s" % self.robot_factory_amount)
        self.water_purifier_amountStringVar.set("Water purifiers: %s" % self.water_purifier_amount)


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
        return len(self.queuemanager.building_queue) - 1


    # Sets what the previous building in the queue were, for showing what has just finished building.
    def set_previous_building(self):
        if self.get_currently_building_name():
            self.previous_building = self.get_currently_building_name()
        else:
            self.previous_building = None


    # Sets how many finished buildings there are of each type.
    def set_building_amounts(self):
        # self.building_amounts = [{ self.air_purifier_amountStringVar : "Air purifiers", self.house_amountStringVar : 0, self.robot_factory_amountStringVar : 0 }]
        # for building in self.queuemanager.building_queue:
        #     print("building in BuildingManager.set_building_amounts: ", building)
        #     if building.get_name()
        if self.get_currently_building_name() == "Air purifier":
            self.air_purifier_amount += 1
        elif self.get_currently_building_name() == "House":
            self.house_amount += 1
        elif self.get_currently_building_name() == "Robot factory":
            self.robot_factory_amount += 1
        elif self.get_currently_building_name() == "Water purifier":
            self.water_purifier_amount += 1
        else:
            print("No building to increase!")
        self.set_building_amountStringVars()


    # Sets what building is currently being constructed for display purposes only.
    def set_building_construction(self):
        if self.get_currently_building_name():
            self.building_buildingStringVar.set("Building %s" % self.get_currently_building_name())
        else:
            self.building_buildingStringVar.set("Nothing to build")


    # Controls what happens when double clicking an item in the building list.
    def add_buildings(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        selection_id = int(selection[0])
        self.queuemanager.add_to_building_queue(selection_id)
        self.set_building_queue_turns()
        self.turnmanager.set_turns_left_building_queue()
        self.set_building_construction()


    # This defines what happens when finishing building something.
    def add_built(self):
        self.set_previous_building()
        if self.previous_building:
            self.built_buildingStringVar.set("Built %s" % self.previous_building)
        self.set_building_amounts()
        self.queuemanager.remove_from_building_queue()
        self.set_building_construction()
        self.turnmanager.set_turns_left_building_queue()
        self.set_building_queue_turns()

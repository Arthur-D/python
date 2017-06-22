from tkinter import StringVar



# Building object to derive from for all buildings. Also handles its own turns.
class Building():
    def __init__(self, properties):
        self.name = properties["Name"]
        self.turns = properties["Turn amount"]
        self.cost = properties["Cost"]
        self.level = 1
        self.graphics_id = None


    def get_name(self):
        return self.name

    def get_turns(self):
        return self.turns

    def get_cost(self):
        return self.cost

    def get_level(self):
        return self.level

    def set_graphics_id(self, graphics_id):
        self.graphics_id = graphics_id

    def get_graphics_id(self):
        if self.graphics_id is not None:
            return self.graphics_id


    def decrease_turns(self):
        if self.turns > 0:
            self.turns -= 1
            if self.turns == 0:
                print("Building complete: ", self.name)


    def increase_level(self):
        if self.level < 5:
            self.level += 1
            if self.level == 5:
                print("Max level reached!")



# Class for handling the buildings.
class BuildingManager:
    def __init__(self):
        self.buildings_names = ""
        self.buildings_names_list = []
        self.building_turns = ""
        self.previous_building = ""
        self.finished_buildings = [Building({"Name" : "Headquarters", "Turn amount" : 0, "Cost" : "0"})]
        self.finished_buildings_names = []

        self.buildingsStringVar = StringVar()
        self.building_descriptionStringVar = StringVar()
        self.building_errorStringVar = StringVar()
        self.built_buildingStringVar = StringVar()
        self.building_turnsStringVar = StringVar()
        self.air_purifier_amountStringVar = StringVar()
        self.house_amountStringVar = StringVar()
        self.robot_factory_amountStringVar = StringVar()
        self.water_purifier_amountStringVar = StringVar()

        self.set_building_properties()
        self.set_building_turns()


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_gamelogic(self, gamelogic):
        self.gamelogic = gamelogic


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_statemanager(self, statemanager):
        self.statemanager = statemanager


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


    # Sets what the previous building in the queue were, for showing what has just finished building.
    def set_previous_building(self):
        if self.queuemanager.get_currently_building_name():
            self.previous_building = self.queuemanager.get_currently_building_name()
        else:
            self.previous_building = None


    # Controls what happens when double clicking an item in the building list.
    def add_buildings(self):
        selection_id = self.guimanager.get_buildingsListbox_selection()
        if self.statemanager.energy_resource >= self.get_building_cost(self.buildings_names_list[selection_id]):
            self.resourcemanager.decrease_resources(self.get_building_cost(self.buildings_names_list[selection_id]))
            self.queuemanager.add_to_building_queue(selection_id)
            self.guimanager.set_building_queue_turns()
            self.turnmanager.set_turns_left_building_queue()
            self.guimanager.set_building_construction()
            self.guimanager.set_building_queueScrollbar_visibility()
        else:
            self.guimanager.set_game_statusStringVar("red", "Not enough\nresources to build!")


    # This defines what happens when finishing building something.
    def add_built(self):
        self.set_previous_building()
        if self.previous_building:
            self.built_buildingStringVar.set("Built %s" % self.previous_building)
        self.set_finished_buildings()
        self.guimanager.set_collectionsCombobox_selection(None)
        self.guimanager.set_collectionsScrollbar_visibility()
        self.guimanager.set_finished_buildings_amounts()
        self.queuemanager.remove_from_building_queue()
        self.guimanager.set_building_construction()
        self.turnmanager.set_turns_left_building_queue()
        self.guimanager.set_building_queue_turns()
        self.guimanager.set_building_queueScrollbar_visibility()


    def set_finished_buildings(self):
        if self.queuemanager.get_currently_building_index() != None:
            self.finished_buildings.append(self.queuemanager.building_queue[self.queuemanager.get_currently_building_index()])

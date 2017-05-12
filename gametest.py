from tkinter import *
from tkinter import ttk



def main():
    root = Tk()
    gamelogic = GameLogic()
    queuemanager = QueueManager()
    turnmanager = TurnManager()
    buildingmanager = BuildingManager()

    gamelogic.set_turnmanager(turnmanager)
    gamelogic.set_buildingmanager(buildingmanager)
    queuemanager.set_buildingmanager(buildingmanager)
    queuemanager.set_turnmanager(turnmanager)
    turnmanager.set_buildingmanager(buildingmanager)
    turnmanager.set_queuemanager(queuemanager)
    buildingmanager.set_turnmanager(turnmanager)
    buildingmanager.set_queuemanager(queuemanager)

    app = GUI(root, gamelogic, buildingmanager, queuemanager, turnmanager)
    root.mainloop()


# Class containing the GUI definitions for tkinter and ttk.
class GUI(Frame):
    def __init__(self, parent, gamelogic, buildingmanager, queuemanager, turnmanager):
        # Creates the main frame and background color.
        Frame.__init__(self, parent, background = "#d9d9d9")
        self.parent = parent
        self.style = ttk.Style()
        self.style.theme_use("default")
        #self.style.configure("TButton", padding = (0, 2, 0, 0), font = "TkFixedFont")
        self.style.configure("building_turns.TLabel", font = "TkTextFont 10")

        self.initUI()
        self.gamelogic = gamelogic
        self.buildingmanager = buildingmanager
        self.queuemanager = queuemanager
        self.turnmanager = turnmanager
        
        # List buildings you can build.
        self.buildingsListbox = Listbox(self, height = 13, background = "white", listvariable = self.buildingmanager.buildingsStringVar)
        
        self.building_queueListbox = Listbox(self, height = 5, background = "white", listvariable = self.queuemanager.building_queueStringVar)
        
        # A name entry widget which currently does not work correctly due to miscommunication between GUI and GameLogic.
        self.nameentry = ttk.Entry(self, textvariable = self.gamelogic.playernameStringVar)
        
        # Hidden label to display the name entered in self.nameentry.
        self.saved_nameLabel = ttk.Label(self, textvariable = self.gamelogic.saved_playernameStringVar)
        
        # Hidden label to display if an invalid name is entered in self.nameentry.
        self.error_playernameLabel = ttk.Label(self, foreground = "red", text = "Invalid name!")
        
        self.UI_configuration()


    def initUI(self):
        self.parent.title("Gametest")
        self.pack(fill = BOTH, expand = True)
        self.centerWindow()


    # Creates the window in which the main frame and the rest is displayed. self.parent.geometry takes width, height, and then centers the window by checking for display resolution and then halving it to find the coordinates.
    def centerWindow(self):
        w = 640
        h = 480
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))


    # Communication function between this GUI class and the GameLogic class.
    def add_buildings(self, buildingsListbox):
        self.buildingmanager.add_buildings(self.buildingsListbox)


    def set_building_description(self, buildingsListbox):
        self.buildingmanager.set_building_description(self.buildingsListbox)


    def remove_from_building_queue(self, building_queueListbox):
        self.queuemanager.delete_from_building_queue(self.building_queueListbox)


    # Communication function between this GUI class and the GameLogic class. Does not currently work as intended (the saved name is not displayed).    
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        self.gamelogic.save_playername(self.saved_nameLabel, self.error_playernameLabel)


    # Function with most of the widgets and their configuration.    
    def UI_configuration(self):
        #time_leftMethod = time_left
        
        # Adding columns and padding space.
        column_number = 0
        # while column_number < 10:
        #     self.columnconfigure(column_number, pad = 4)
        #     print("column_number in GUI.UI_configuration: ", column_number)
        #     column_number += 1

        # self.columnconfigure(0, pad = 2)
        # self.columnconfigure(1, pad = 4)
        # self.columnconfigure(2, pad = 4)
        # self.columnconfigure(3, pad = 4)
        # self.columnconfigure(4, pad = 4)
        # self.columnconfigure(5, pad = 4)
        # self.columnconfigure(6, pad = 4)
        # self.columnconfigure(7, pad = 4)
        # self.columnconfigure(8, pad = 0)
        # self.columnconfigure(9, pad = 4)
        # Adding rows and padding space.
        # self.rowconfigure(0, pad = 3)
        # self.rowconfigure(1, pad = 3)
        # self.rowconfigure(2, pad = 20)
        # self.rowconfigure(3, pad = 3)
        # self.rowconfigure(4, pad = 3)
        # self.rowconfigure(5, pad = 3)
        # self.rowconfigure(6, pad = 3)

        
        # Creating UI elements and setting their parameters.
        
        add_buildingsLabel = ttk.Label(self, text = "Add building")
        # Creating main buttons.
        button1 = ttk.Button(self, text = "Save name", command = self.save_playername)
        button2 = ttk.Button(self, text = "Button 2")
        button3 = ttk.Button(self, text = "Build house", command = self.buildingmanager.add_buildings)
        button4 = ttk.Button(self, text = "End turn", command = self.gamelogic.run_simulation)
        quitButton = ttk.Button(self, text = "Quit", command = self.quit)
        
        
        resources = ttk.Labelframe(self, text = "Resources", labelanchor = "nw", width = 150, height = 100)
        buildingsLabelframe = ttk.Labelframe(self, text = "Buildings", labelanchor = "nw", width = 100, height = 200)
        building_descriptionLabel = ttk.Label(self, textvariable = self.buildingmanager.building_descriptionStringVar)
        turns_left_building_queueLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_building_queueStringVar)
        turns_left_current_buildingLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_current_buildingStringVar)
        building_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.building_buildingStringVar)
        built_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.built_buildingStringVar)
        building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", textvariable = self.buildingmanager.building_turnsStringVar)
        building_building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", textvariable = self.buildingmanager.building_building_turnsStringVar, wraplength = 2, padding = 0)

        air_purifier_amountLabel = ttk.Label(buildingsLabelframe, textvariable = self.buildingmanager.air_purifier_amountStringVar)
        house_amountLabel = ttk.Label(buildingsLabelframe, textvariable = self.buildingmanager.house_amountStringVar)
        robot_factory_amountLabel = ttk.Label(buildingsLabelframe, textvariable = self.buildingmanager.robot_factory_amountStringVar)

        turnLabel = ttk.Label(self, textvariable = self.turnmanager.turn_numberStringVar)
        building_queueLabel = ttk.Label(self, text = "Building queue")
        #building_queueStringVar.set(self.building_queue)

        # Binding actions to elements.
        # Double-1 means double left click.
        # self.buildingsListbox.select_set(first="active")
        # self.buildingsListbox.activate(self.buildingsListbox.nearest(y=0))
        self.buildingsListbox.bind("<<ListboxSelect>>", self.set_building_description)
        self.buildingsListbox.bind("<Double-1>", self.add_buildings)
        self.building_queueListbox.bind("<Double-1>", self.remove_from_building_queue)

        # Placement of UI elements on the grid.
        self.grid(sticky = N + S + W + E)

        add_buildingsLabel.grid(row = 0, column = 0, sticky = S)
        self.nameentry.grid(row = 9, column = 0, sticky = W)
        self.nameentry.focus()
        button1.grid(row = 9, column = 1)
        button2.grid(row = 9, column = 2)
        button3.grid(row = 9, column = 3)
        button4.grid(row = 9, column = 4)
        quitButton.grid(row = 9, column = 8, sticky = E)

        self.buildingsListbox.grid(row = 1, column = 0, sticky = W)
        #resources.grid(row = 0, column = 8, sticky = W)
        buildingsLabelframe.grid(row = 1, column = 8, sticky = W)
        built_buildingLabel.grid(row = 2, column = 8, sticky = W)
        building_descriptionLabel.grid(row = 1, column = 2, sticky = NW)
        building_turnsLabel.grid(row = 1, column = 1, sticky = NW)
        building_building_turnsLabel.grid(row = 3, column = 1, sticky = NW)

        air_purifier_amountLabel.grid(row = 1, column = 8, sticky = W)
        house_amountLabel.grid(row=2, column=8, sticky=W)
        robot_factory_amountLabel.grid(row = 3, column = 8, sticky = W)

        turnLabel.grid(row = 0, column = 8, sticky = E)
        self.saved_nameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid_remove()
        building_queueLabel.grid(row = 2, column = 0, sticky = S)
        self.building_queueListbox.grid(row = 3, column = 0, sticky = W)
        building_buildingLabel.grid(row = 4, column = 0, sticky = W)
        # built_buildingLabel.grid(row = 5, column = 0, sticky = W)
        turns_left_building_queueLabel.grid(row = 6, column = 0, sticky = W)
        # turns_left_current_buildingLabel.grid(row = 7, column = 0, sticky = W)
        emptylabel = ttk.Label(self, text = "")
        emptylabel.grid(row = 2, column = 8)



# High level class getting the simulation started.
class GameLogic():
    def __init__(self):
        self.playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    # This defines what happens when clicking End turn.
    def run_simulation(self):
        self.turnmanager.increase_game_turns()
        self.turnmanager.decrease_building_turns()
        self.buildingmanager.set_building_building_turns()


    # Logic for saving playername to labels in GUI.
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        saving_name = str(self.playernameStringVar.get())
        if saving_name != "":
            saved_nameLabel.grid()
            self.saved_playernameStringVar.set(saving_name)
            error_playernameLabel.grid_remove()
        else:
            error_playernameLabel.grid()
            saved_nameLabel.grid_remove()



# Class managing all turns.
class TurnManager():
    def __init__(self):
        self.turn = 0
        self.turns_left_building_queue = 0
        self.turns_left_current_building = 0

        self.turn_numberStringVar = StringVar()
        self.turn_numberStringVar.set("Turn %s" % self.turn)
        self.turns_left_building_queueStringVar = StringVar()
        self.turns_left_current_buildingStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    def decrease_building_turns(self):
        if self.queuemanager.building_queue:
            building = self.queuemanager.building_queue[self.buildingmanager.get_currently_building_index()]
            building.decrease_turns()
            self.set_turns_left_current_building()
            self.set_turns_left_building_queue()
            self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % building.get_turns())
            if building.get_turns() == 0:
                self.buildingmanager.add_built()


    # Logic for displaying how many turns are left to build the whole building queue.
    def set_turns_left_building_queue(self):
        turn_amount = 0
        for index, building in enumerate(self.queuemanager.building_queue):
            if index != self.buildingmanager.get_currently_building_index():
                turn_amount += building.get_turns()
            else:
                turn_amount += self.turns_left_current_building
        self.turns_left_building_queue = turn_amount
        if len(self.queuemanager.building_queue) > 0:
            self.turns_left_building_queueStringVar.set("Turns left for\nbuilding queue: %s" % self.turns_left_building_queue)
        else:
            self.turns_left_building_queueStringVar.set("")
        print("Turns left for building queue: ", self.turns_left_building_queue)


    # Logic for displaying how many turns are left building the foremost building in the queue.
    def set_turns_left_current_building(self):
        if self.queuemanager.building_queue:
            building = self.queuemanager.building_queue[self.buildingmanager.get_currently_building_index()]
            self.turns_left_current_building = building.get_turns()
            self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % building.get_turns())
        else:
            self.turns_left_current_buildingStringVar.set("")


    def increase_game_turns(self):
        if self.turn < 50:
            self.turn += 1
            self.turn_numberStringVar.set("Turn %s" % self.turn)
            print("Turn", self.turn)



class QueueManager():
    def __init__(self):
        self.building_queue = []
        self.building_queueStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_building_queue(self):
        buildings_names = ""
        for building_property in self.building_queue:
            buildings_names += "{%s}\n" % (building_property.get_name())
        self.building_queueStringVar.set(buildings_names)


    def add_to_building_queue(self, selection_id):
        self.building_queue.insert(0, (Building(self.buildingmanager.building_properties[selection_id])))
        self.set_building_queue()


    # Handles removal of a building from building queue after it's been built.
    def remove_from_building_queue(self):
        if self.building_queue:
            self.building_queue.pop()
            self.set_building_queue()
        else:
            print("Building queue empty")


    # Handles deletion of buildings from building queue.
    def delete_from_building_queue(self, building_queueListbox):
        selection = building_queueListbox.curselection()
        if len(selection) == 1:
            selection_id = int(selection[0])
            if self.building_queue:
                self.buildingmanager.set_previous_building()
                self.building_queue.pop(selection_id)
                self.set_building_queue()
        else:
            selection_id = None
            print("No more buildings to remove. Building queue empty.")
        if len(selection) == 1:
            self.buildingmanager.set_building_construction()
        if selection_id == self.buildingmanager.get_currently_building_index() + 1:
            self.turnmanager.set_turns_left_current_building()
        self.turnmanager.set_turns_left_building_queue()
        self.buildingmanager.set_building_building_turns()



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



class BuildingManager():
    def __init__(self):
        self.air_purifier_amount = 0
        self.house_amount = 0
        self.robot_factory_amount = 0

        self.buildings_names = ""
        self.building_turns = ""
        self.previous_building = ""

        self.buildingsStringVar = StringVar()
        self.building_descriptionStringVar = StringVar()
        self.building_buildingStringVar = StringVar()
        self.building_building_turnsStringVar = StringVar()
        self.built_buildingStringVar = StringVar()
        self.building_turnsStringVar = StringVar()
        self.air_purifier_amountStringVar = StringVar()
        self.house_amountStringVar = StringVar()
        self.robot_factory_amountStringVar = StringVar()

        self.set_building_properties()
        self.set_building_amountStringVars()
        self.set_building_turns()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    def set_building_properties(self):
        self.building_properties = [{"Name" : "Air purifier", "Turn amount" : 4}, {"Name" : "House", "Turn amount" : 5}, {"Name" : "Robot factory", "Turn amount" : 7}, {"Name" : "Water purifier", "Turn amount" : 4}]
        self.set_building_names()

        self.air_purifier = Building(properties=self.get_building_properties("Air purifier"))
        self.house = Building(properties=self.get_building_properties("House"))
        self.robot_factory = Building(properties=self.get_building_properties("Robot factory"))
        self.water_purifier = Building(properties=self.get_building_properties("Water purifier"))

        self.building_objects = [self.air_purifier, self.house, self.robot_factory, self.water_purifier]


    def get_building_properties(self, name):
        for building in self.building_properties:
            if building["Name"] == name:
                return building
        return None


    def get_currently_building_object(self):
        print("self.get_building_properties(self.get_currently_building()) in BuildingManager.get_currently_building_object", self.get_building_properties(self.get_currently_building()))


    # Populate the list of possible buildings to build in self.buildings_list.
    def set_building_names(self):
        for building_property in self.building_properties:
            self.buildings_names += "{%s}\n" % (building_property["Name"])
        self.buildingsStringVar.set(self.buildings_names)

        # chars_to_remove = ["{", "'", "}"]
        # self.houses_numberStringVar.set(self.buildings_dict)
        # buildings_names_filtered = ''.join([char for char in self.houses_numberStringVar.get() if char not in chars_to_remove])
        # buildings_names_filtered = buildings_names_filtered.replace(",", "\n")
        # self.houses_numberStringVar.set(buildings_names_filtered)


    def set_building_turns(self):
        for building_property in self.building_properties:
            self.building_turns += "%s\n" % (building_property["Turn amount"])
        self.building_turnsStringVar.set(self.building_turns)


    def set_building_description(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        if selection:
            selection_id = int(selection[0])
            if selection_id == 0:
                self.building_descriptionStringVar.set("Test1")
            elif selection_id == 1:
                self.building_descriptionStringVar.set("Test2")
            else:
                self.building_descriptionStringVar.set("")


    def set_building_amountStringVars(self):
        self.air_purifier_amountStringVar.set("Air purifiers: %s" % self.air_purifier_amount)
        self.house_amountStringVar.set("Houses: %s" % self.house_amount)
        self.robot_factory_amountStringVar.set("Robot factories: %s" % self.robot_factory_amount)


    def set_building_building_turns(self):
        building_building_turns = ""
        for building in self.queuemanager.building_queue:
            building_building_turns += "%s" % building.get_turns()
        self.building_building_turnsStringVar.set(building_building_turns)


    def get_currently_building(self):
        if self.queuemanager.building_queue:
            return self.queuemanager.building_queue[len(self.queuemanager.building_queue) - 1].get_name()
        else:
            return None


    def get_currently_building_index(self):
            return len(self.queuemanager.building_queue) - 1


    def set_previous_building(self):
        if self.get_currently_building():
            self.previous_building = self.get_currently_building()
        else:
            self.previous_building = None


    def set_building_amounts(self):
        # self.building_amounts = [{ self.air_purifier_amountStringVar : "Air purifiers", self.house_amountStringVar : 0, self.robot_factory_amountStringVar : 0 }]
        # for building in self.queuemanager.building_queue:
        #     print("building in BuildingManager.set_building_amounts: ", building)
        #     if building.get_name()
        if self.get_currently_building() == "Air purifier":
            self.air_purifier_amount += 1
        elif self.get_currently_building() == "House":
            self.house_amount += 1
        elif self.get_currently_building() == "Robot factory":
            self.robot_factory_amount += 1
        else:
            print("No building to increase!")
        self.set_building_amountStringVars()


    def set_building_construction(self):
        if self.get_currently_building():
            if self.queuemanager.building_queue:
                self.building_buildingStringVar.set("Building %s" % self.get_currently_building())
            if self.queuemanager.building_queue and self.turnmanager.turns_left_current_building == 1:
                self.building_buildingStringVar.set("Building %s" % self.get_currently_building())
        else:
            self.building_buildingStringVar.set("Nothing to build")


    # Controls what happens when double clicking an item in the building list.
    def add_buildings(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        selection_id = int(selection[0])
        self.queuemanager.add_to_building_queue(selection_id)
        self.set_building_building_turns()
        if len(self.queuemanager.building_queue) == 1:
            self.turnmanager.set_turns_left_current_building()
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
        self.turnmanager.set_turns_left_current_building()
        self.turnmanager.set_turns_left_building_queue()
        self.set_building_building_turns()



if __name__ == "__main__":
    main()

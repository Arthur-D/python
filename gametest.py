from tkinter import *
from tkinter import ttk



# The initializing function. Also contains references to setters in a specific order so as to make the various classes aware of each other.
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
        
        # Listing buildings you can build.
        self.buildingsListbox = Listbox(self, height = 13, background = "white", listvariable = self.buildingmanager.buildingsStringVar)

        # Listing buildings in the building queue.
        self.building_queueListbox = Listbox(self, height = 5, background = "white", selectmode = "browse", listvariable = self.queuemanager.building_queueStringVar)
        
        # A name entry widget which currently does not work correctly due to miscommunication between GUI and GameLogic.
        self.nameentry = ttk.Entry(self, textvariable = self.gamelogic.playernameStringVar)
        
        # Hidden label to display the name entered in self.nameentry.
        self.saved_nameLabel = ttk.Label(self, textvariable = self.gamelogic.saved_playernameStringVar)
        
        # Hidden label to display if an invalid name is entered in self.nameentry.
        self.error_playernameLabel = ttk.Label(self, foreground = "red", text = "Invalid name!")
        
        self.set_UI_configuration()
        self.set_UI_widgets()
        self.set_widgets_on_grid()
        self.set_widget_mouse_bindings()


    # Function for creating the window context.
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


    # Communication function between this class and the BuildingManager class.
    def add_buildings(self, buildingsListbox):
        self.buildingmanager.add_buildings(self.buildingsListbox)


    # Communication function between this class and the BuildingManager class.
    def set_building_description(self, buildingsListbox):
        self.buildingmanager.set_building_description(self.buildingsListbox)


    # Communication function between this class and the QueueManager class.
    def remove_from_building_queue(self, building_queueListbox):
        self.queuemanager.delete_from_building_queue(self.building_queueListbox)


    # Communication function between this class and the QueueManager class.
    def move_in_building_queue(self, building_queueListbox):
        self.queuemanager.move_in_building_queue(self.building_queueListbox)


    # Communication function between this class and the GameLogic class. Does not currently work as intended (the saved name is not displayed).
    def save_playername(self, saved_nameLabel, error_playernameLabel):
        self.gamelogic.save_playername(self.saved_nameLabel, self.error_playernameLabel)


    # Function with widget configuration. Currently unused.
    def set_UI_configuration(self):
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

        
    # Creating UI elements and setting their parameters. Note: some widgets are in the constructor __init__().
    def set_UI_widgets(self):
        # Creating main buttons.
        self.button1 = ttk.Button(self, text = "Save name", command = self.save_playername)
        self.button2 = ttk.Button(self, text = "Button 2")
        self.button3 = ttk.Button(self, text = "Build house", command = self.buildingmanager.add_buildings)
        self.button4 = ttk.Button(self, text = "End turn", command = self.gamelogic.run_simulation)
        self.quitButton = ttk.Button(self, text = "Quit", command = self.quit)

        # Creating labels.
        self.add_buildingsLabel = ttk.Label(self, text = "Add building")
        self.turnLabel = ttk.Label(self, textvariable = self.turnmanager.turn_numberStringVar)
        self.building_queueLabel = ttk.Label(self, text = "Building queue")
        self.building_descriptionLabel = ttk.Label(self, textvariable = self.buildingmanager.building_descriptionStringVar)
        self.turns_left_building_queueLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_building_queueStringVar)
        self.turns_left_current_buildingLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_current_buildingStringVar)
        self.building_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.building_buildingStringVar)
        self.built_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.built_buildingStringVar)
        self.building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", wraplength = 2, pad = "2 1 2 1", textvariable = self.buildingmanager.building_turnsStringVar)
        self.building_building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", wraplength = 2, pad = "2 1 2 1", textvariable = self.buildingmanager.building_building_turnsStringVar)

        self.building_amountsLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.building_amountsStringVar)
        self.air_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.air_purifier_amountStringVar)
        self.house_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.house_amountStringVar)
        self.robot_factory_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.robot_factory_amountStringVar)
        self.water_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.water_purifier_amountStringVar)

        # Creating labelframes.
        self.resources = ttk.Labelframe(self, text = "Resources", labelanchor = "nw", width = 150, height = 100)
        self.buildingsLabelframe = ttk.Labelframe(self, text = "Buildings", labelanchor = "nw", width = 100, height = 200)


    # Placement of UI elements on the grid.
    def set_widgets_on_grid(self):
        self.grid(sticky = N + S + W + E)

        # Row 0:
        self.add_buildingsLabel.grid(row = 0, column = 0, sticky = S)
        self.turnLabel.grid(row = 0, column = 8, sticky = E)
        #resources.grid(row = 0, column = 8, sticky = W)

        # Row 1:
        self.buildingsListbox.grid(row = 1, column = 0, sticky = W)
        self.building_turnsLabel.grid(row = 1, column = 1, sticky = NW)
        self.building_descriptionLabel.grid(row = 1, column = 2, sticky = NW)
        self.buildingsLabelframe.grid(row = 1, column = 8, sticky = W)
        self.air_purifier_amountLabel.grid(row = 1, column = 8, sticky = W)

        # Row 2:
        self.building_queueLabel.grid(row = 2, column = 0, sticky = S)
        self.built_buildingLabel.grid(row = 2, column = 8, sticky = W)
        self.house_amountLabel.grid(row = 2, column = 8, sticky = W)

        # Row 3:
        self.building_queueListbox.grid(row = 3, column = 0, sticky = W)
        self.building_building_turnsLabel.grid(row = 3, column = 1, sticky = NW)
        self.robot_factory_amountLabel.grid(row = 3, column= 8 , sticky = W)

        # Row 4:
        self.building_buildingLabel.grid(row = 4, column = 0, sticky = W)
        self.water_purifier_amountLabel.grid(row = 4, column = 8, sticky = W)

        # Row 5:
        # self.built_buildingLabel.grid(row = 5, column = 0, sticky = W)

        # Row 6:
        self.turns_left_building_queueLabel.grid(row = 6, column = 0, sticky = W)

        # Row 7:
        # self.turns_left_current_buildingLabel.grid(row = 7, column = 0, sticky = W)

        # Row 8:
        self.saved_nameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid_remove()

        # Row 9:
        self.nameentry.grid(row = 9, column = 0, sticky = W)
        self.nameentry.focus()
        self.button1.grid(row = 9, column = 1)
        self.button2.grid(row = 9, column = 2)
        self.button3.grid(row = 9, column = 3)
        self.button4.grid(row = 9, column = 4)
        self.quitButton.grid(row = 9, column = 8, sticky = E)


    # Binding actions to elements.
    # Double-1 means double left click.
    def set_widget_mouse_bindings(self):
        # self.buildingsListbox.select_set(first="active")
        # self.buildingsListbox.activate(self.buildingsListbox.nearest(y=0))
        self.buildingsListbox.bind("<<ListboxSelect>>", self.set_building_description)
        self.buildingsListbox.bind("<Double-1>", self.add_buildings)
        self.building_queueListbox.bind("<Double-1>", self.remove_from_building_queue)
        self.building_queueListbox.bind("<3>", self.move_in_building_queue)



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
        self.buildingmanager.set_building_queue_turns()


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


    # Decreases the amount of turns for the foremost building in the queue if End turn button is pressed.
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
            building = self.buildingmanager.get_currently_building()
            self.turns_left_current_building = building.get_turns()
            self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % self.turns_left_current_building)
        else:
            self.turns_left_current_buildingStringVar.set("")


    # Increments the global turn counter. See GameLogic.run_simulation() for the other things happening when clicking End turn.
    def increase_game_turns(self):
        if self.turn < 100:
            self.turn += 1
            self.turn_numberStringVar.set("Turn %s" % self.turn)
            print("Turn", self.turn)



# Class for managing the various queues in play.
class QueueManager():
    def __init__(self):
        self.building_queue = []
        self.building_queueStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    # Sets the visible names in the building queue for display.
    def set_building_queue(self):
        buildings_names = ""
        for building_property in self.building_queue:
            buildings_names += "{%s}\n" % (building_property.get_name())
        self.building_queueStringVar.set(buildings_names)


    # Inserts a new building into the building queue.
    def add_to_building_queue(self, selection_id):
        self.building_queue.insert(0, (Building(self.buildingmanager.building_properties[selection_id])))
        self.set_building_queue()


    # Handles removal of a building from the visible building queue after it's been built.
    def remove_from_building_queue(self):
        if self.building_queue:
            self.building_queue.pop()
            self.set_building_queue()
        else:
            print("Building queue empty")


    # Handles deletion of buildings from building queue.
    def delete_from_building_queue(self, building_queueListbox):
        selection = building_queueListbox.curselection()
        if self.building_queue and len(selection) == 1:
            selection_id = int(selection[0])
            self.buildingmanager.set_previous_building()
            self.building_queue.pop(selection_id)
            self.set_building_queue()
            self.buildingmanager.set_building_construction()
            print("self.buildingmanager.get_currently_building_index() in QueueManager.delete_from_building_queue(): ", self.buildingmanager.get_currently_building_index())
            print("selection_id in QueueManager.delete_from_building_queue(): ", selection_id)
            if selection_id == self.buildingmanager.get_currently_building_index() + 1:
                self.turnmanager.set_turns_left_current_building()
        else:
            print("No more buildings to remove. Building queue empty.")
        self.turnmanager.set_turns_left_building_queue()
        self.buildingmanager.set_building_queue_turns()


    # Makes it possible to move a building forward in the queue.
    def move_in_building_queue(self, building_queueListbox):
        selection = building_queueListbox.curselection()
        if selection:
            selection_id = int(selection[0])
            building = self.building_queue[selection_id]
            self.building_queue.pop(selection_id)
            self.building_queue.insert(selection_id + 1, building)
            building_queueListbox.selection_clear(selection_id)
            building_queueListbox.selection_set(selection_id + 1)
            self.set_building_queue()
            self.buildingmanager.set_building_queue_turns()



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
        print("self.buildings_names_list in BuildingManager.set_building_names(): ", self.buildings_names_list)
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
        self.set_building_queue_turns()




if __name__ == "__main__":
    main()

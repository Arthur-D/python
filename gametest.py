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
        self.columnconfigure(0, pad = 2)
        self.columnconfigure(1, pad = 4)
        self.columnconfigure(2, pad = 4)
        self.columnconfigure(3, pad = 4)
        self.columnconfigure(4, pad = 4)
        self.columnconfigure(5, pad = 4)
        self.columnconfigure(6, pad = 4)
        self.columnconfigure(7, pad = 4)
        self.columnconfigure(8, pad = 0)
        self.columnconfigure(9, pad = 4)
        # Adding rows and padding space.
        self.rowconfigure(0, pad = 3)
        self.rowconfigure(1, pad = 3)
        self.rowconfigure(2, pad = 20)
        self.rowconfigure(3, pad = 3)
        self.rowconfigure(4, pad = 3)
        self.rowconfigure(5, pad = 3)
        self.rowconfigure(6, pad = 3)

        
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
        #time_leftLabel = Label(self, textvariable = time_leftStringVar)
        turns_left_building_queueLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_building_queueStringVar)
        turns_left_current_buildingLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_current_buildingStringVar)
        building_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.building_buildingStringVar)
        built_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.built_buildingStringVar)

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
        building_descriptionLabel.grid(row = 1, column = 1, sticky = NW)

        air_purifier_amountLabel.grid(row = 1, column = 8, sticky = W)
        house_amountLabel.grid(row=2, column=8, sticky=W)
        robot_factory_amountLabel.grid(row = 3, column = 8, sticky = W)

        turnLabel.grid(row = 0, column = 8, sticky = E)
        self.saved_nameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid_remove()
        building_queueLabel.grid(row = 2, column = 0, sticky = S)
        self.building_queueListbox.grid(row = 3, column = 0, sticky = W)
        #time_leftLabel.grid(row = 2, column = 1, sticky = W)
        building_buildingLabel.grid(row = 4, column = 0, sticky = W)
        # built_buildingLabel.grid(row = 5, column = 0, sticky = W)
        turns_left_building_queueLabel.grid(row = 6, column = 0, sticky = W)
        turns_left_current_buildingLabel.grid(row = 7, column = 0, sticky = W)
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
        self.turnmanager.decrease_building_queue_turns()


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


    # Logic for displaying how many turns are left to build the whole building queue.
    def set_turns_left_building_queue(self):
        turn_amount = 0
        for index, building in enumerate(self.queuemanager.building_queue):
            print("Building index:", index, building)
            if index != self.buildingmanager.get_currently_building_index():
                turn_amount += self.buildingmanager.buildings_dict.get(building)
            else:
                turn_amount += self.turns_left_current_building
        self.turns_left_building_queue = turn_amount
        self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
        print("Turns left: ", self.turns_left_building_queue)


    # Logic for displaying how many turns are left building the foremost building in the queue.
    def set_turns_left_current_building(self):
        print(self.queuemanager.building_queue)
        if self.queuemanager.building_queue:
            # self.turns_left_current_building = self.buildingmanager.building_object[self.buildingmanager.get_currently_building_index()].get_turns()
            self.turns_left_current_building = self.buildingmanager.buildings_dict[self.buildingmanager.get_currently_building()]
        else:
            self.turns_left_current_building = 0
        print("self.turns_left_current_building: ", self.turns_left_current_building)
        self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % self.turns_left_current_building)


    # Method for decreasing the turns in the building queue and current building.
    def decrease_building_queue_turns(self):
        if self.turns_left_building_queue > 1:
            self.turns_left_building_queue -= 1
            self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
            print("Set turns left to", self.turns_left_building_queue)
        else:
            self.turns_left_building_queue = 0
            self.turns_left_building_queueStringVar.set("Queue empty")
            print("Set turns left to 0")
        if self.turns_left_current_building > 1:
            self.turns_left_current_building -= 1
            self.turns_left_current_buildingStringVar.set(
                "Turns left for\ncurrent building: %s" % self.turns_left_current_building)
            print("Turns left for current building: ", self.turns_left_current_building)
        else:
            print(self.queuemanager.building_queue)
            self.buildingmanager.add_built()
            if not self.queuemanager.building_queue:
                self.turns_left_current_building = 0


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


    def add_to_building_queue(self, selection_id):
        self.building_queue.insert(0, "%s" % (self.buildingmanager.buildings_list[selection_id]))
        print("Building queue: ", self.building_queue)
        self.building_queueStringVar.set(self.building_queue)


    # Handles removal of a building from building queue after it's been built.
    def remove_from_building_queue(self):
        if self.building_queue:
            self.building_queue.pop()
            self.building_queueStringVar.set(self.building_queue)
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
                self.building_queueStringVar.set(self.building_queue)
        else:
            selection_id = None
            print("No more buildings to remove. Building queue empty.")
        print("len(selection) in delete_from_building_queue: ", len(selection))
        if len(selection) == 1:
            self.buildingmanager.set_building_construction()
        if selection_id == self.buildingmanager.get_currently_building_index() + 1:
            self.turnmanager.set_turns_left_current_building()
        self.turnmanager.set_turns_left_building_queue()



class Building():
    def __init__(self, name, turns):
        self.name = name
        self.turns = turns


    def get_name(self):
        return self.name


    def get_turns(self):
        return self.turns



class BuildingManager():
    def __init__(self):
        self.air_purifier_amount = 0
        self.house_amount = 0
        self.robot_factory_amount = 0

        self.buildings_names = ""
        self.previous_building = ""
        # Defining which buildings that can be built and how many turns they take to build.
        self.buildings_dict = {
            "Air purifier" : 4,
            "Water purifier" : 4,
            "House" : 5,
            "Robot factory" : 7
            }
        # self.buildings_unsorted_list = [key for key in self.buildings_dict]
        # self.buildings_list = sorted(self.buildings_unsorted_list)

        self.buildingsStringVar = StringVar()
        self.building_descriptionStringVar = StringVar()
        self.building_buildingStringVar = StringVar()
        self.built_buildingStringVar = StringVar()
        self.air_purifier_amountStringVar = StringVar()
        self.house_amountStringVar = StringVar()
        self.robot_factory_amountStringVar = StringVar()

        self.set_building_properties()
        self.set_building_names()
        self.set_building_amountStringVars()
        # self.set_buildings_attributes()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    def set_building_properties(self):
        self.building_properties = [{"Name" : "Air purifier", "Turn amount" : 4}, {"Name" : "House", "Turn amount" : 5}, {"Name" : "Robot factory", "Turn amount" : 7}, {"Name" : "Water purifier", "Turn amount" : 4}]
        self.set_building_names()

        # self.building_object = [self.air_purifier, self.house, self.robot_factory, self.water_purifier]
        # self.buildings_list = sorted(key for key in self.building_properties if ""])
        # print("self.house.get_turns() in BuildingManager.set_buildings_attributes: ", self.house.get_turns())


    def get_building_properties(self, name):
        for building in self.building_properties:
            if building["Name"] == name:
                return building
            return None


    # Populate the list of built buildings with building names in self.buildings_list.
    def set_building_names(self):
        for name in self.building_properties:
            if self.building_properties["Name"] == name:
                self.buildings_names += "{%s}\n" % (name)
        self.buildingsStringVar.set(self.buildings_names)

        # chars_to_remove = ["{", "'", "}"]
        # self.houses_numberStringVar.set(self.buildings_dict)
        # buildings_names_filtered = ''.join([char for char in self.houses_numberStringVar.get() if char not in chars_to_remove])
        # buildings_names_filtered = buildings_names_filtered.replace(",", "\n")
        # self.houses_numberStringVar.set(buildings_names_filtered)


    def set_building_description(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        if selection:
            selection_id = int(selection[0])
            print("selection_id in set_building_description: ", selection_id)
            if selection_id == 0:
                self.building_descriptionStringVar.set("Test1")
            elif selection_id == 1:
                self.building_descriptionStringVar.set("Test2")
            else:
                self.building_descriptionStringVar.set("")
        # pass


    def set_building_amountStringVars(self):
        self.air_purifier_amountStringVar.set("Air purifiers: %s" % self.air_purifier_amount)
        self.house_amountStringVar.set("Houses: %s" % self.house_amount)
        self.robot_factory_amountStringVar.set("Robot factories: %s" % self.robot_factory_amount)


    def get_currently_building(self):
        if self.queuemanager.building_queue:
            # print("self.queuemanager.building_queue[len(self.queuemanager.building_queue) - 1] in get_currently_building: ", self.queuemanager.building_queue[len(self.queuemanager.building_queue) - 1])
            return self.queuemanager.building_queue[len(self.queuemanager.building_queue) - 1]
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
        print("buildingsListbox in BuildingManager.add_buildings: ", buildingsListbox)
        selection = buildingsListbox.curselection()
        print("selection in add_buildings: ", selection)
        selection_id = int(selection[0])
        print("selection_id in add_buildings: ", selection_id)
        self.queuemanager.add_to_building_queue(selection_id)
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



if __name__ == "__main__":
    main()

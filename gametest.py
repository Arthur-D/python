from tkinter import *
from tkinter import ttk




def main():
    root = Tk()
    gamelogic = GameLogic()
    # gamelogic = GameLogic()
    # buildingmanager = BuildingManager(gamelogic)
    queuemanager = QueueManager()
    turnmanager = TurnManager()
    buildingmanager = BuildingManager()

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
        self.turnmanager.set_turns_left_current_building()
        
    def remove_from_building_queue(self, building_queueListbox):
        self.queuemanager.remove_from_building_queue(self.building_queueListbox)
        
    def set_building_description(self, buildingsListbox):
        self.buildingmanager.set_building_description()
        
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

        housesLabel = ttk.Label(buildingsLabelframe, textvariable = self.buildingmanager.houses_numberStringVar)
        air_purifierLabel = ttk.Label(buildingsLabelframe, textvariable = self.buildingmanager.air_purifiers_numberStringVar)
        turnLabel = ttk.Label(self, textvariable = self.gamelogic.turn_numberStringVar)
        building_queueLabel = ttk.Label(self, text = "Building queue")
        #building_queueStringVar.set(self.building_queue)

        # Binding actions to elements.
        # Double-1 means double left click.
        self.buildingsListbox.bind("<Double-1>", self.add_buildings)
        self.buildingsListbox.bind("<1>", self.set_building_description)
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
        building_descriptionLabel.grid(row = 1, column = 1, sticky = NW)
        housesLabel.grid(row = 2, column = 8, sticky = W)
        air_purifierLabel.grid(row = 1, column = 8, sticky = W)
        turnLabel.grid(row = 0, column = 8, sticky = E)
        self.saved_nameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid_remove()
        building_queueLabel.grid(row = 2, column = 0, sticky = S)
        self.building_queueListbox.grid(row = 3, column = 0, sticky = W)
        #time_leftLabel.grid(row = 2, column = 1, sticky = W)
        turns_left_building_queueLabel.grid(row = 4, column = 0, sticky = W)
        turns_left_current_buildingLabel.grid(row = 5, column = 0, sticky = W)
        emptylabel = ttk.Label(self, text = "")
        emptylabel.grid(row = 2, column = 8)




# Class containing the actual game logic.
class GameLogic():
    def __init__(self):
        self.turn = 0

        self.playernameStringVar = StringVar()
        self.saved_playernameStringVar = StringVar()
        self.turn_numberStringVar = StringVar()
        self.turn_numberStringVar.set("Turn %s" % self.turn)



    # def set_buildingmanager(self):
    #     self.buildingmanager = buildingmanager



    # This defines what happens when clicking End turn.
    def run_simulation(self):
        if self.turn < 50:
            self.turn += 1
            self.turn_numberStringVar.set("Turn %s" % self.turn)
            print("Turn", self.turn)
            #print("First in self.building_queue: %s" % self.building_queue[len(self.building_queue)-1], ", index", len(self.building_queue)-1)



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




class TurnManager():
    def __init__(self):
        self.turns_left_building_queue = 0
        self.turns_left_current_building = 0

        self.turns_left_building_queueStringVar = StringVar()
        self.turns_left_current_buildingStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager


    # Logic for displaying how many turns are left to build the whole building queue.
    def set_turns_left_building_queue(self, turn_amount=0):
        self.turns_left_building_queue = turn_amount
        self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
        if self.turns_left_building_queue:
            print("Turns left: ", self.turns_left_building_queue)
        else:
            print("No more turns left.")




    # Logic for displaying how many turns are left building the foremost building in the queue.
    def set_turns_left_current_building(self):
        turn_amount = 0
        print(self.queuemanager.building_queue)
        # self.buildingmanager.currently_building_index = len(self.queuemanager.building_queue) - 1
        if self.queuemanager.building_queue:
            if self.turns_left_current_building <= 1:
                self.turns_left_current_building = self.buildingmanager.buildings_dict[
                    self.queuemanager.building_queue[self.buildingmanager.currently_building_index]]
            for index, building in enumerate(self.queuemanager.building_queue):
                print("Building index:", index, building)
                if index != self.buildingmanager.currently_building_index:
                    turn_amount += self.buildingmanager.buildings_dict.get(building)
                elif len(self.queuemanager.building_queue) == 1:
                    turn_amount += self.buildingmanager.buildings_dict.get(building)
                else:
                    turn_amount += self.turns_left_current_building
        else:
            self.turns_left_current_building = 0
        self.turns_left_current_buildingStringVar.set(
            "Turns left for\ncurrent building: %s" % self.turns_left_current_building)
        self.set_turns_left_building_queue(turn_amount)



    def decrease_queue_turns(self):
        if self.turns_left_current_building > 1:
            self.turns_left_current_building -= 1
            self.turns_left_current_buildingStringVar.set(
                "Turns left for\ncurrent building: %s" % self.turns_left_current_building)
            print("Turns left for current building: ", self.turns_left_current_building)
        else:
            print(self.building_queue)
            self.buildingmanager.add_built(self.buildingmanager.currently_building)
            if not self.queuemanager.building_queue:
                self.turns_left_current_building = 0
        if self.turns_left_building_queue > 1:
            self.turns_left_building_queue -= 1
            self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
            print("Set turns left to", self.turns_left_building_queue)
        else:
            self.turns_left_building_queue = 0
            self.turns_left_building_queueStringVar.set("Queue empty")
            print("Set turns left to 0")




class QueueManager():
    def __init__(self):
        self.building_queue = []
        self.building_queueStringVar = StringVar()


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager



    # Handles removal of buildings from building queue.
    def remove_from_building_queue(self, building_queueListbox):
        turn_amount = 0
        selection = building_queueListbox.curselection()
        if self.building_queue and len(selection) == 1:
            selection_id = int(selection[0])
            left_over_turn_amount = self.turns_left_current_building
            print("selection_id and len(self.building_queue)-1: ", selection_id, len(self.building_queue)-1)
            if selection_id == len(self.building_queue)-1:
                self.turns_left_building_queue -= self.turns_left_current_building
                print("Removed %s turns." % self.turns_left_current_building)
                self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
                self.turns_left_current_building = self.buildingmanager.buildings_dict[self.building_queue[self.buildingmanager.currently_building_index]]
            else:
                self.turns_left_building_queue -= BuildingManager.buildings_dict.get(self.building_queue[selection_id])
                self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
            self.turns_left_building_queueStringVar.set("Turns left: %s" % self.turns_left_building_queue)
            self.building_queue.remove(self.building_queue[selection_id])
            self.building_queueStringVar.set(self.building_queue)
            if len(self.building_queue)-1 > -1:
                self.buildingmanager.currently_building = self.building_queue[len(self.building_queue) - 1]
            else:
                self.turns_left_current_building = 0
            #print("self.turns_left_building_queue -= self.turns_left_current_building: ", self.turns_left_building_queue -= self.turns_left_current_building)
            print("Buildings.buildings_list[selection_id]: ", BuildingManager.buildings_list[selection_id])
            print("selection and selection_id: ", selection, selection_id)
            #self.set_turns_left_building_queue(turn_amount)
        else:
            print("No more buildings to remove.")
            self.turns_left_current_building = 0
            self.building_queueStringVar.set(self.building_queue)
            print("Building queue empty")
        print("self.building_queue empty: ", self.building_queue)
        self.turns_left_current_buildingStringVar.set("Turns left for\ncurrent building: %s" % self.turns_left_current_building)




class BuildingManager():
    def __init__(self):

        self.air_purifiers_number = 0
        self.houses_number = 0
        self.buildings_names = ""
        self.currently_building = ""
        self.buildings_list = sorted(["Air purifier", "Water purifier", "House", "Robot factory"])
        # Defining which buildings that can be built and how many turns they take to build.
        self.buildings_dict = {
            "Air purifier" : 4,
            "Water purifier" : 4,
            "House" : 5,
            "Robot factory" : 7
            }

        self.buildingsStringVar = StringVar()
        self.building_descriptionStringVar = StringVar()

        self.air_purifiers_numberStringVar = StringVar()
        self.houses_numberStringVar = StringVar()

        self.set_buildings()


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_queuemanager(self, queuemanager):
        self.queuemanager = queuemanager
        # FIXME: self.currently_building_index appears to have a value of -1 since it's initialized before the fun starts.'
        self.currently_building_index = len(self.queuemanager.building_queue)-1


    # def set_gamelogic(self):
    #     self.gamelogic = gamelogic



    # Populate the list of built buildings with building names in self.buildings_list.
    def set_buildings(self):
        for name in self.buildings_list:
            self.buildings_names += "{%s}\n" % (name)
        self.buildingsStringVar.set(self.buildings_names)
        self.air_purifiers_numberStringVar.set("Air purifiers: %s" % self.air_purifiers_number)
        self.houses_numberStringVar.set("Houses: %s" % self.houses_number)
        # chars_to_remove = ["{", "'", "}"]
        # self.houses_numberStringVar.set(self.buildings_dict)
        # buildings_names_filtered = ''.join([char for char in self.houses_numberStringVar.get() if char not in chars_to_remove])
        # buildings_names_filtered = buildings_names_filtered.replace(",", "\n")
        # self.houses_numberStringVar.set(buildings_names_filtered)



    def set_building_description(self):
        # selection = buildingsListbox.curselection()
        # selection_id = int(selection[0])

        self.building_descriptionStringVar.set("Test2")



    # Controls what happens when double clicking an item in the building list.
    def add_buildings(self, buildingsListbox):
        selection = buildingsListbox.curselection()
        selection_id = int(selection[0])
        self.queuemanager.building_queue.insert(0, "%s" % (self.buildings_list[selection_id]))
        # self.queuemanager.building_queue.insert(0, "Test")
        print("Building queue: ", self.queuemanager.building_queue)
        self.currently_building = self.queuemanager.building_queue[len(self.queuemanager.building_queue)-1]
        self.queuemanager.building_queueStringVar.set(self.queuemanager.building_queue)



    # This defines what happens when finishing building something.
    def add_built(self, currently_building):
        if self.queuemanager.building_queue:
            self.queuemanager.building_queue.pop()
            self.queuemanager.building_queueStringVar.set(self.queuemanager.building_queue)
            self.queuemanager.turns_left_current_buildingStringVar.set("Built %s" % self.currently_building)
            self.currently_building_index = len(self.queuemanager.building_queue) - 1
        else:
            # self.turnmanager.turns_left_current_building = 0
            self.queuemanager.building_queueStringVar.set(GameLogic.building_queue)
            print("Building queue empty")
        if currently_building == "House":
            self.houses_number += 1
            self.houses_numberStringVar.set("Houses: %s" % self.houses_number)
        elif currently_building == "Air purifier":
            self.air_purifiers_number += 1
            self.air_purifiers_numberStringVar.set("Air purifiers: %s" % self.air_purifiers_number)
        else:
            print("No building to increase!")
        if self.queuemanager.building_queue:
            self.currently_building = self.queuemanager.building_queue[len(GameLogic.building_queue) - 1]
            self.queuemanager.turns_left_current_building = self.buildings_dict[self.queuemanager.building_queue[self.currently_building_index]]
        else:
            self.currently_building = None




if __name__ == "__main__":
    main()

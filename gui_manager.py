from tkinter import *
from tkinter import ttk



# Class containing the GUI definitions for tkinter and ttk.
class GUI(Frame):
    def __init__(self, parent, gamelogic, buildingmanager, queuemanager, turnmanager, savemanager, stringvarmanager):
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
        self.savemanager = savemanager
        self.stringvarmanager = stringvarmanager

        # Listing buildings you can build.
        self.buildingsListbox = Listbox(self, width = 16, height = 13, background = "white", listvariable = self.buildingmanager.buildingsStringVar)

        # Listing buildings in the building queue.
        self.building_queueListbox = Listbox(self, width = 16, height = 5, background = "white", selectmode = "browse", listvariable = self.queuemanager.building_queueStringVar)

        # A name entry widget.
        self.nameentry = ttk.Entry(self, width = 16, textvariable = self.gamelogic.playernameStringVar)
        self.save_name = ttk.Entry(self, width = 16, textvariable = self.gamelogic.save_nameStringVar)

        # Hidden label to display the name entered in self.nameentry.
        self.saved_nameLabel = ttk.Label(self, textvariable = self.gamelogic.saved_playernameStringVar)

        # Hidden label to display if an invalid name is entered in self.nameentry.
        self.error_playernameLabel = ttk.Label(self, foreground = "red", text = "Invalid name!")

        # Creating comboboxes.
        self.saved_gamesCombobox = ttk.Combobox(self, width = 15, state = "readonly")
        self.saved_gamesCombobox.set("Select saved game:")

        self.set_UI_configuration()
        self.set_UI_widgets()
        self.set_widgets_on_grid()
        self.set_widget_mouse_bindings()
        self.set_saved_games(self.saved_gamesCombobox)


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


    def set_saved_games(self, saved_gamesCombobox):
        self.gamelogic.set_saved_games(self.saved_gamesCombobox)


    def select_saved_game(self, saved_gameCombobox):
        self.gamelogic.select_saved_game(self.saved_gamesCombobox)


    def save_game(self):
        self.gamelogic.save_game(self.saved_gamesCombobox)


    def load_game(self):
        self.gamelogic.load_game(self.saved_gamesCombobox)


    # Communication function between this class and the GameLogic class.
    def save_playername(self):
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
        self.button2 = ttk.Button(self, text = "Save game", command = self.save_game)
        self.button3 = ttk.Button(self, text = "Load game", command = self.load_game)
        self.button4 = ttk.Button(self, text = "End turn", command = self.gamelogic.run_simulation)
        self.quitButton = ttk.Button(self, text = "Quit", command = self.quit)

        # Creating labelframes.
        self.resources = ttk.Labelframe(self, text = "Resources", labelanchor = "nw", width = 150, height = 100)
        self.buildingsLabelframe = ttk.Labelframe(self, text = "Buildings", labelanchor = "nw", width = 100, height = 200)

        # Creating labels.
        self.add_buildingsLabel = ttk.Label(self, text = "Add building")
        self.turnLabel = ttk.Label(self, textvariable = self.turnmanager.turn_numberStringVar)
        self.building_queueLabel = ttk.Label(self, text = "Building queue")
        self.building_descriptionLabel = ttk.Label(self, textvariable = self.buildingmanager.building_descriptionStringVar)
        self.turns_left_building_queueLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_building_queueStringVar)
        self.building_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.building_buildingStringVar)
        self.built_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.built_buildingStringVar)
        self.building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", wraplength = 2, pad = "2 1 2 1", textvariable = self.buildingmanager.building_turnsStringVar)
        self.building_building_turnsLabel = ttk.Label(self, style = "building_turns.TLabel", wraplength = 2, pad = "2 1 2 1", textvariable = self.buildingmanager.building_building_turnsStringVar)

        self.building_amountsLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.building_amountsStringVar)
        self.air_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.stringvarmanager.air_purifier_amountStringVar)
        self.house_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.house_amountStringVar)
        self.robot_factory_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.robot_factory_amountStringVar)
        self.water_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.water_purifier_amountStringVar)


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

        # Row 8:
        self.saved_nameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid(row = 8, column = 0, sticky = W)
        self.error_playernameLabel.grid_remove()

        # Row 9:
        self.nameentry.grid(row = 9, column = 0, sticky = W)
        self.nameentry.focus()
        self.save_name.grid(row = 9, column = 2, sticky = W)
        self.button1.grid(row = 9, column = 1)
        self.button2.grid(row = 9, column = 3)
        self.button4.grid(row = 9, column = 6)
        self.quitButton.grid(row = 9, column = 8, sticky = E)

        # Row 10:
        self.saved_gamesCombobox.grid(row = 10, column = 0)
        self.button3.grid(row = 10, column = 1)


    # Binding actions to elements. Double-1 means double left click.
    def set_widget_mouse_bindings(self):
        # self.buildingsListbox.select_set(first="active")
        # self.buildingsListbox.activate(self.buildingsListbox.nearest(y=0))
        self.buildingsListbox.bind("<<ListboxSelect>>", self.set_building_description)
        self.buildingsListbox.bind("<Double-1>", self.add_buildings)
        self.building_queueListbox.bind("<Double-1>", self.remove_from_building_queue)
        self.building_queueListbox.bind("<3>", self.move_in_building_queue)
        self.saved_gamesCombobox.bind("<<ComboboxSelected>>", self.select_saved_game)

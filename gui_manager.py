from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter



# Class containing the GUI definitions for tkinter and ttk.
class GUI(Frame):
    def __init__(self, parent, gamelogic, buildingmanager, queuemanager, turnmanager, resourcemanager, savemanager, statemanager, saveandloadgui):
        # Creates the main frame and background color.
        Frame.__init__(self, parent, background = "#d9d9d9")
        self.parent = parent
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("building_list", font = "TkFixedFont")

        self.initUI()
        self.gamelogic = gamelogic
        self.buildingmanager = buildingmanager
        self.queuemanager = queuemanager
        self.turnmanager = turnmanager
        self.resourcemanager = resourcemanager
        self.savemanager = savemanager
        self.saveandloadgui = saveandloadgui
        self.statemanager = statemanager

        self.building_buildingStringVar = StringVar()
        self.building_building_turnsStringVar = StringVar()
        self.building_amountsStringVar = StringVar()
        self.game_statusStringVar = StringVar()
        self.collection_itemsStringVar = StringVar()

        self.finished_buildings_amounts = {}

        # Listing buildings you can build.
        self.buildingsListbox = Listbox(self, font = "TkFixedFont", width = 16, height = 10, background = "white", listvariable = self.buildingmanager.buildingsStringVar)

        # Listing buildings in the building queue.
        self.building_queueListbox = Listbox(self, font = "TkFixedFont", width = 16, height = 5, background = "white", selectmode = "browse", listvariable = self.queuemanager.building_queueStringVar)
        self.building_queueListbox.configure(self.building_queueListbox.yview_scroll(1, "units"))

        # Listing collection items.
        self.collectionsListbox = Listbox(self, font = "TkFixedFont", width = 16, height = 5, listvariable = self.collection_itemsStringVar)

        # A name entry widget.
        self.nameentry = ttk.Entry(self, width = 16, textvariable = self.gamelogic.playernameStringVar)

        # Hidden label to display the name entered in self.nameentry.
        self.saved_nameLabel = ttk.Label(self,  textvariable = self.gamelogic.saved_playernameStringVar)

        # Hidden label to display if an invalid name is entered in self.nameentry.
        self.error_playernameLabel = ttk.Label(self, foreground = "red", textvariable = self.gamelogic.error_playernameStringVar)

        self.displayCanvas = Canvas(self, width = 960, height = 540, scrollregion = "0 0 1024 1024")
        self.display_x_Scrollbar = Scrollbar(self, orient = HORIZONTAL, command = self.displayCanvas.xview)
        self.display_y_Scrollbar = Scrollbar(self, orient = VERTICAL, command = self.displayCanvas.yview)
        self.displayCanvas.configure(xscrollcommand = self.display_x_Scrollbar.set, yscrollcommand = self.display_y_Scrollbar.set)
        self.displayCanvas.bind("<B1-Motion>", self.displayCanvas.xview)

        self.set_UI_configuration()
        self.set_UI_widgets()
        self.set_widgets_on_grid()
        self.set_widget_mouse_bindings()
        self.fill_displayCanvas()

        self.queuemanager.set_finished_buildings()
        self.set_finished_buildings_amounts()
        self.turnmanager.turn_numberStringVar.set("Turn %s" % self.statemanager.turn_number)
        self.resourcemanager.energy_resourceStringVar.set("Energy: {}".format(self.statemanager.energy_resource))
        # self.set_collectionsCombobox_selection()


    # Function for creating the window context.
    def initUI(self):
        self.parent.title("Gametest")
        self._root().option_add("*tearOff", FALSE)
        self.pack(fill = BOTH, expand = True)
        # self.centerWindow(self.parent, 960, 540)


    # Creates the window in which the main frame and the rest is displayed. self.parent.geometry takes width, height, and then centers the window by checking for display resolution and then halving it to find the coordinates.
    def centerWindow(self, window, w, h):
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))


    # Communication function between this class and the BuildingManager class.
    def add_buildings(self, buildingsListbox):
        self.buildingmanager.add_buildings()


    # Communication function between this class and the BuildingManager class.
    def set_building_description(self, buildingsListbox):
        self.buildingmanager.set_building_description(self.buildingsListbox)


    # Communication function between this class and the QueueManager class.
    def remove_from_building_queue(self, building_queueListbox):
        self.queuemanager.delete_from_building_queue(self.building_queueListbox)


    # Communication function between this class and the QueueManager class.
    def move_in_building_queue(self, building_queueListbox):
        self.queuemanager.move_in_building_queue(self.building_queueListbox)


    def set_building_queueScrollbar_visibility(self):
        if self.building_queueListbox.size() > self.building_queueListbox.cget("height"):
            self.building_queueScrollbar.grid(row=4, column=0, sticky=(NE, S))
        else:
            self.building_queueScrollbar.grid_remove()


    def set_collectionsScrollbar_visibility(self):
        if self.collectionsListbox.size() > self.collectionsListbox.cget("height"):
            self.collectionsScrollbar.grid(row=4, column=9, sticky=(NE, S))
        else:
            self.collectionsScrollbar.grid_remove()


    def get_buildingsListbox_selection(self):
        selection = self.buildingsListbox.curselection()
        return int(selection[0])


    # Communication function between this class and the GameLogic class.
    def save_playername(self):
        self.gamelogic.save_playername(self.saved_nameLabel, self.error_playernameLabel)


    # Sets what building is currently being constructed for display purposes only.
    def set_building_construction(self):
        if self.queuemanager.get_currently_building_name():
            self.building_buildingStringVar.set("Building %s" % self.queuemanager.get_currently_building_name())
        else:
            self.building_buildingStringVar.set("")


    # Similar to set_buildings_list() but is for the buildings that are in the building queue.
    def set_building_queue_turns(self):
        building_queue_turns = ""
        for building in self.queuemanager.building_queue:
            building_queue_turns += "%s" % building.get_turns()
        self.building_building_turnsStringVar.set(building_queue_turns)


    def set_finished_buildings_amounts(self):
        building_amounts = ""
        building_names = [building.get_name() for building in self.queuemanager.finished_buildings]
        for building_name in self.buildingmanager.buildings_names_list:
            self.finished_buildings_amounts[building_name] = building_names.count(building_name)
            if building_name.endswith("y"):
                building_amounts += "{}ies:{:4}\n".format(building_name[:-1], building_names.count(building_name))
            else:
                building_amounts += "{}s:{:4}\n".format(building_name, building_names.count(building_name))
        self.building_amountsStringVar.set(building_amounts.rstrip("\n"))


    def set_game_statusStringVar(self, color, content):
        self.game_statusLabel.grid()
        self.game_statusLabel["foreground"] = color
        self.game_statusStringVar.set(content)
        self.parent.after(5000, lambda: self.game_statusLabel.grid_remove())


    def set_collectionsCombobox_selection(self, collectionsCombobox):
        if self.collectionsCombobox.current() == 0:
            self.queuemanager.set_buildings_collection()
        elif self.collectionsCombobox.current() == 1:
            self.queuemanager.set_robots_collection()
        self.collectionsCombobox.selection_clear()


    def fill_displayCanvas(self):
        image_original_dirt = Image.open("Graphics/dirt_border.png")
        image_resized_dirt = image_original_dirt.resize((128, 64))
        # image_aa_dirt = image_resized_dirt.filter(ImageFilter.SMOOTH)
        image_dirt = ImageTk.PhotoImage(image_resized_dirt)
        self.displayCanvas.create_rectangle(2, 2, 1022, 1022)
        self.image_dirt = image_dirt
        x_loc = 388
        y_loc = 4
        offset_x = 64
        offset_y = 32
        for x in range(8):
            x_loc += offset_x
            y_loc += offset_y
            self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)
        for x in range(7):
            x_loc -= offset_x
            y_loc += offset_y
            self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)

        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image = image_dirt)
        # x_loc = 324
        # y_loc = 36
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image = image_dirt)
        # x_loc = 260
        # y_loc = 68
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)
        # x_loc = 196
        # y_loc = 100
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)
        # x_loc = 132
        # y_loc = 132
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)
        # x_loc = 68
        # y_loc = 164
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)
        # x_loc = 4
        # y_loc = 196
        # for x in range(8):
        #     x_loc += 64
        #     y_loc += 32
        #     self.displayCanvas.create_image(x_loc, y_loc, image=image_dirt)


    # Function with widget configuration. Currently unused.
    def set_UI_configuration(self):
        # Adding columns and padding space.
        column_number = 0
        # while column_number < 10:
        #     self.columnconfigure(column_number, pad = 4)
        #     print("column_number in GUI.UI_configuration: ", column_number)
        #     column_number += 1


    # Creating UI elements and setting their parameters. Note: some widgets are in the constructor __init__().
    def set_UI_widgets(self):
        # Creating menubar.
        self.menubar = Menu(self.parent)
        self.parent["menu"] = self.menubar
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu = self.menu_file, label = "File")
        self.menu_file.add_command(label = "New game", command = self.gamelogic.start_new_game)
        self.menu_file.add_command(label = "Save current", command = self.savemanager.save_game_main_window)
        self.menu_file.add_command(label = "Load/Save as...", command = self.saveandloadgui.set_save_load_window)

        # Creating main buttons.
        # self.resource_robotButton = ttk.Bu
        self.save_playernameButton = ttk.Button(self, text ="Save name", command = self.save_playername)
        self.end_turnButton = ttk.Button(self, text = "End turn", command = self.gamelogic.run_simulation)
        self.quitButton = ttk.Button(self, text = "Quit", command = self.quit)

        # Creating labelframes.
        self.resourcesLabelframe = ttk.Labelframe(self, text = "Resources", labelanchor = "nw", width = 300, height = 32)
        self.buildingsLabelframe = ttk.Labelframe(self, text = "Buildings", labelanchor = "nw", width = 100, height = 200)

        #Creating scrollbars.
        self.building_queueScrollbar = ttk.Scrollbar(self, orient = VERTICAL, command = self.building_queueListbox.yview)
        self.building_queueListbox.configure(yscrollcommand = self.building_queueScrollbar.set)
        self.collectionsScrollbar = ttk.Scrollbar(self, orient = VERTICAL, command = self.collectionsListbox.yview)
        self.collectionsListbox.configure(yscrollcommand = self.collectionsScrollbar.set)

        # Creating comboboxes.
        self.collectionsCombobox = ttk.Combobox(self)
        self.collectionsCombobox["values"] = ("Buildings", "Robots")
        self.collectionsCombobox["state"] = "readonly"
        self.collectionsCombobox.current(1)

        # Creating labels.
        self.game_statusLabel = ttk.Label(self, font = "TkTooltipFont", textvariable = self.game_statusStringVar)
        self.add_buildingsLabel = ttk.Label(self, text = "Add building")
        self.turnLabel = ttk.Label(self, textvariable = self.turnmanager.turn_numberStringVar)
        self.building_queueLabel = ttk.Label(self, text = "Building queue")
        self.building_descriptionLabel = ttk.Label(self, textvariable = self.buildingmanager.building_descriptionStringVar)
        self.turns_left_building_queueLabel = ttk.Label(self, textvariable = self.turnmanager.turns_left_building_queueStringVar)
        self.building_buildingLabel = ttk.Label(self, textvariable = self.building_buildingStringVar)
        self.built_buildingLabel = ttk.Label(self, textvariable = self.buildingmanager.built_buildingStringVar)


        self.building_amountsLabel = ttk.Label(self.buildingsLabelframe, justify = "right", textvariable = self.building_amountsStringVar)
        self.air_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.air_purifier_amountStringVar)
        self.house_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.house_amountStringVar)
        self.robot_factory_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.robot_factory_amountStringVar)
        self.water_purifier_amountLabel = ttk.Label(self.buildingsLabelframe, textvariable = self.buildingmanager.water_purifier_amountStringVar)

        self.energy_resourceLabel = ttk.Label(self.resourcesLabelframe, textvariable = self.resourcemanager.energy_resourceStringVar)


    # Placement of UI elements on the grid.
    def set_widgets_on_grid(self):
        self.grid(sticky = N + S + W + E)

        # Row 0:
        self.resourcesLabelframe.grid(row = 0, column = 0, columnspan = 7, sticky = W)
        self.energy_resourceLabel.grid(row = 0, column = 1, sticky = W)
        self.game_statusLabel.grid(row = 0, column = 2)
        self.saved_nameLabel.grid(row = 0, column = 16, sticky = W)
        self.turnLabel.grid(row = 0, column = 16, sticky = E)

        # Row 1:
        self.add_buildingsLabel.grid(row = 1, column = 0, sticky = S)
        self.built_buildingLabel.grid(row = 1, column = 16, sticky = W)

        # Row 2:
        self.buildingsListbox.grid(row = 2, column = 0, sticky = W)
        self.display_y_Scrollbar.grid(row = 2, column = 15, rowspan = 4, sticky = NS)
        self.building_descriptionLabel.grid(row = 1, column = 3, sticky = NW)
        self.displayCanvas.grid(row = 2, column = 3, rowspan = 4, columnspan = 12)
        self.buildingsLabelframe.grid(row = 2, column = 16, sticky = W)

        # Row 3:
        self.building_queueLabel.grid(row = 3, column = 0, sticky = S)
        self.collectionsCombobox.grid(row = 3, column = 16)

        # Row 4:
        self.building_queueListbox.grid(row = 4, column = 0, sticky = W)
        self.collectionsListbox.grid(row = 4, column = 16, sticky = W)

        # Row 5:
        self.building_buildingLabel.grid(row = 5, column = 0, sticky = W)
        self.display_x_Scrollbar.grid(row = 6, column = 3, columnspan = 13, sticky = EW)

        # Row 6:
        self.turns_left_building_queueLabel.grid(row = 6, column = 0, sticky = W)

        # Row 7:
        self.building_amountsLabel.grid(row = 7, column = 16)

        # Row 8:

        # Row 9:
        self.nameentry.grid(row = 9, column = 0, sticky = W)
        self.nameentry.focus()
        self.save_playernameButton.grid(row = 9, column = 3)
        self.end_turnButton.grid(row = 9, column = 6)
        self.quitButton.grid(row = 9, column = 8, sticky = E)

        # Row 10:
        self.error_playernameLabel.grid(row = 10, column = 2, sticky = W)
        self.error_playernameLabel.grid_remove()


    # Binding actions to elements. Double-1 means double left click.
    def set_widget_mouse_bindings(self):
        # self.buildingsListbox.select_set(first="active")
        # self.buildingsListbox.activate(self.buildingsListbox.nearest(y=0))
        self.buildingsListbox.bind("<<ListboxSelect>>", self.set_building_description)
        self.buildingsListbox.bind("<Double-1>", self.add_buildings)
        self.building_queueListbox.bind("<Double-1>", self.remove_from_building_queue)
        self.building_queueListbox.bind("<3>", self.move_in_building_queue)
        self.collectionsCombobox.bind("<<ComboboxSelected>>", self.set_collectionsCombobox_selection)



class SaveAndLoadGUI(Frame):
    def __init__(self, parent, savemanager):
        self.parent = parent
        self.savemanager = savemanager

        # Creates the main frame and background color.
        Frame.__init__(self, parent, background = "#d9d9d9")
        self.save_statusStringVar = StringVar()


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    # Creates the window in which the main frame and the rest is displayed. self.parent.geometry takes width, height, and then centers the window by checking for display resolution and then halving it to find the coordinates.
    def centerWindow(self, window):
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        w = window.winfo_reqwidth()
        h = window.winfo_reqheight()
        print("w, h in SaveAndLoadGUI.centerWindow(): ", w, h)
        print("window.bbox() in SaveAndLoadGUI.centerWindow(): ", window.bbox())
        x = (sw - w)/2
        y = (sh - h)/2
        # window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        print("window.winfo_geometry() in SaveAndLoadGUI.centerWindow():" , window.winfo_geometry())


    def load_game(self, saved_gamesListbox):
        self.savemanager.load_game()


    def set_save_load_window(self):
        self.save_load_window = Toplevel(self.parent)
        self.save_load_window.title("Load/Save game")
        self.save_load_window.focus()

        self.save_load_window.columnconfigure(1, minsize = 15)

        self.save_gameEntry = ttk.Entry(self.save_load_window, width = 16, textvariable = self.savemanager.save_nameStringVar)

        self.save_gameButton = ttk.Button(self.save_load_window, text = "Save game", width = 10, command = self.savemanager.save_game)
        self.load_gameButton = ttk.Button(self.save_load_window, text = "Load game", command = self.savemanager.load_game)
        self.delete_saveButton = ttk.Button(self.save_load_window, text = "Delete save", command = self.savemanager.delete_game)
        self.confirmButton = ttk.Button(self.save_load_window, text = "Confirm", command = self.savemanager.confirm)
        self.abortButton = ttk.Button(self.save_load_window, text = "Abort", command = self.savemanager.abort)

        self.saved_gamesLabel = Label(self.save_load_window, text = "Saved games")
        self.game_infoLabel = Label(self.save_load_window, text = "Game info")
        self.save_statusLabel = Label(self.save_load_window, wraplength = 120, textvariable = self.save_statusStringVar)
        self.saved_game_infoLabel = Label(self.save_load_window, width = 16, textvariable = self.savemanager.saved_game_infoStringVar)

        self.saved_gamesListbox = Listbox(self.save_load_window, width = 16, height = 6, listvariable = self.savemanager.saved_gamesStringVar)
        self.saved_gamesListbox.bind("<<ListboxSelect>>", self.savemanager.set_save_name_from_selection)
        self.saved_gamesListbox.bind("<Double-1>", self.load_game)
        self.saved_gamesScrollbar = ttk.Scrollbar(self.save_load_window, orient = VERTICAL, command = self.saved_gamesListbox.yview)
        self.saved_gamesListbox.configure(yscrollcommand = self.saved_gamesScrollbar.set)

        self.saved_gamesLabel.grid(row = 0, column = 0)
        self.game_infoLabel.grid(row = 0, column = 2)
        self.saved_gamesListbox.grid(row = 1, column = 0, rowspan = 6)
        self.saved_game_infoLabel.grid(row = 1, column = 2, rowspan = 2, sticky = N)
        self.save_gameEntry.grid(row = 4, column = 3, sticky = S)
        self.save_gameButton.grid(row = 3, column = 3, sticky = N)
        self.load_gameButton.grid(row = 1, column = 3, sticky = N)
        self.delete_saveButton.grid(row = 2, column = 3, sticky = N)

        self.savemanager.set_saved_games()
        self.centerWindow(self.save_load_window)


    def close_save_load_window(self):
        self.save_load_window.destroy()


    def get_selection_saved_game(self):
        selection = self.saved_gamesListbox.curselection()
        if selection:
            selection_id = int(selection[0])
            return selection_id


    def set_selection_saved_game(self, selection):
        if len(self.savemanager.saved_games) > 0:
            self.saved_gamesListbox.selection_set(selection)


    def show_confirm_and_abortButton(self):
        self.abortButton.grid(row = 4, column = 2)
        self.confirmButton.grid(row = 3, column = 2)


    def set_saved_gamesScrollbar_visibility(self):
        if self.saved_gamesListbox.size() > self.saved_gamesListbox.cget("height"):
            self.saved_gamesScrollbar.grid(row = 1, column = 1, rowspan = 4, sticky = (NW, S))
        else:
            self.saved_gamesScrollbar.grid_remove()


    def remove_save_statusLabel(self):
        if self.save_load_window.winfo_exists() == 1:
            self.save_statusLabel.grid_remove()


    def set_save_statusStringVar(self, color, content):
        if self.save_load_window.winfo_exists() == 1:
            self.save_statusLabel.grid(row = 3, column = 2, rowspan = 2)
            self.save_statusLabel["foreground"] = color
            self.save_statusStringVar.set(content)
            self.parent.after(5000, lambda: self.remove_save_statusLabel())

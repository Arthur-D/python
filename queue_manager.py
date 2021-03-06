from tkinter import StringVar
from building_manager import Building
from robot_manager import Robot



# Class for managing the various queues in play.
class QueueManager():
    def __init__(self):
        self.building_queue = []
        self.building_queueStringVar = StringVar()
        self.finished_robots = []


    def set_buildingmanager(self, buildingmanager):
        self.buildingmanager = buildingmanager


    def set_guimanager(self, guimanager):
        self.guimanager = guimanager


    def set_resourcemanager(self, resourcemanager):
        self.resourcemanager = resourcemanager


    def set_robotmanager(self, robotmanager):
        self.robotmanager = robotmanager


    def set_turnmanager(self, turnmanager):
        self.turnmanager = turnmanager


    def set_building_queue(self, saved_queue):
        self.building_queue = saved_queue


    # Sets the visible names in the building queue for display.
    def set_building_queue_names(self):
        buildings_names = ""
        for building in self.building_queue:
            # First and last two brackets are denoting it as a literal, while the middle bracket ones are the .format representations of strings. :15 pads the first one to the left by 15 characters.
            buildings_names += ("{{{:15}{}}}\n").format(building.get_name(), building.get_turns())
        self.building_queueStringVar.set(buildings_names)


    # Inserts a new building into the building queue.
    def add_to_building_queue(self, selection_id):
        self.building_queue.insert(0, (Building(self.buildingmanager.building_properties[selection_id])))
        self.set_building_queue_names()


    # Handles removal of a building from the visible building queue after it's been built.
    def remove_from_building_queue(self):
        if self.building_queue:
            self.building_queue.pop()
            self.set_building_queue_names()
        else:
            print("Building queue empty")


    # Handles deletion of buildings from building queue.
    def delete_from_building_queue(self, building_queueListbox):
        selection = building_queueListbox.curselection()
        if self.building_queue and len(selection) == 1:
            selection_id = int(selection[0])
            self.buildingmanager.set_previous_building()
            print("self.building_queue[selection_id].get_name() in QueueManager.delete_from_building_queue: ", self.building_queue[selection_id].get_name())
            self.resourcemanager.increase_resources(self.buildingmanager.get_building_cost(self.building_queue[selection_id].get_name()))
            self.building_queue.pop(selection_id)
            self.set_building_queue_names()
            self.guimanager.set_building_construction()
        else:
            print("No more buildings to remove. Building queue empty.")
        self.turnmanager.set_turns_left_building_queue()
        self.guimanager.set_building_queueScrollbar_visibility()


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
            self.set_building_queue_names()
            self.guimanager.building_queueListbox.see(selection_id + 1)
            self.guimanager.set_building_queue_turns()
            self.guimanager.set_building_construction()


    # Returns the foremost building instance in the building queue.
    def get_currently_building(self):
        if self.building_queue:
            return self.building_queue[self.get_currently_building_index()]
        else:
            return None


    # For getting the index of the foremost building in the queue.
    def get_currently_building_index(self):
        if self.building_queue:
            return len(self.building_queue) - 1


    # For getting the name of the foremost building in the queue.
    def get_currently_building_name(self):
        if self.building_queue:
            return self.building_queue[len(self.building_queue) - 1].get_name()


    def set_buildings_collection(self):
        buildings = ""
        if len(self.finished_buildings) > 0:
            for building in self.finished_buildings:
                buildings += "{{{:15}{}}}\n".format(building.get_name(), building.get_level())
            self.guimanager.collection_itemsStringVar.set(buildings)


    def set_finished_robots(self):
        self.finished_robots.append()


    def set_robots_collection(self):
        robots = ""
        for robot in self.finished_robots:
            robots += "{{{:15}{}}}\n".format(robot.get_name(), robot.get_level())
        self.guimanager.collection_itemsStringVar.set(robots)

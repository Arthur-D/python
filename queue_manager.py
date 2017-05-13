from tkinter import StringVar
from building_manager import Building



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

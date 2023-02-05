# 12/12/2022
from random import choice
from Item_info import basis_items
from math import ceil
from copy import copy

class Inventory:
    def __init__(self, inventory_limit = 20):
        # Items
        self.stored_items = []
        self.inventory = []

        # information
        self.inventory_limit = inventory_limit
        self.used_item_ids = []

    def generate_items(self, number= 4):
        items = []
        for _ in range(number):
            item = copy(choice(basis_items))
            items.append(item)
        self.inventory = items
        self.organize_inventories(True)
        

    def can_use_inventory(self):
        return len(self.inventory) > 0

    def generate_id(self):
        if len(self.used_item_ids) == 0:
            self.used_item_ids.append(0)
        ids = self.used_item_ids
        ids.sort()

        id = ids[-1] + 1
        self.used_item_ids.append(id)
        return id
    
    def organize_inventories(self, t_inventory_f_storage):
        # chooses what item collection to organise
        if t_inventory_f_storage:
            self.inventory = self.new_organizer(self.inventory)
        else:
            self.stored_items = self.new_organizer(self.stored_items)

    def new_organizer(self, inventory):
        "Organizes all items within a inventory using"
        # creates a list of items inside of the inventory to organize
        item_combo = []
        for item in inventory:
            quantity = item.quantity
            item_object = item
            found_item = False

            if len(item_combo) == 0:
                item_combo.append([item_object, quantity])

            for item_list in item_combo:
                if item_object.id == item_list[0].id:
                    item_list[1] += quantity
                    found_item = True

            if found_item == False:
                item_combo.append([item_object, quantity])
        
        # goes through all of the items in the items lists
        items = []
        for item_object, item_quantity in item_combo:
            number_of_objects = ceil(item_quantity / item.max_quantity)
            for _ in range(number_of_objects):
                object_clone = copy(item_object)
                object_clone.quantity = 0
                item_quantity = object_clone.change_quantity(item_quantity)
                items.append(object_clone)

        return items
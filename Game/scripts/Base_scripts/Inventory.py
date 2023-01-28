# 12/12/2022

class Inventory:
    def __init__(self, inventory_limit = 20):
        # Items
        self.stored_items = []
        self.inventory = []

        # information
        self.inventory_limit = inventory_limit
        self.used_item_ids = []

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
            self.inventory = self.organizer(self.inventory)
        else:
            self.stored_items = self.organizer(self.stored_items)

    def organizer(self, inventory):
        # separates items based if their filled
        filled_items = []
        non_filled = []
        for item in inventory:
            if item.is_full:
                filled_items.append(item)
            else:
                non_filled.append(item)
        # Goes through all of the items that aren't filled
        move_to_filled = []  # this is where the index of filled items will go to for removal
        for item in non_filled:
            item_name = item.name
            matching = []

            if not index in move_to_filled:  # skips items that are already in the move list
                for same_items in non_filled:  # creates a list of matching items by name
                    # filters
                    name_check = same_items.name == item_name  # has the same name
                    not_same_check = not same_items == item  # not the same as the main item
                    index_not_check = not non_filled.index(same_items) in move_to_filled  # not in the move list
                    not_dead = same_items.quantity != 0  # isn't zero

                    if name_check and not_same_check and index_not_check and not_dead:
                        matching.append(same_items)

                if len(matching) != 0:

                    # goes through matched items
                    for sub_item in matching:
                        if item.quantity != 0:
                            amount_have = item.quantity
                            leftovers = sub_item.change_quantity(amount_have)
                            if sub_item.is_full:  # checks to see if an item is now full and place it into filled list
                                index = non_filled.index(sub_item)
                                filled_items.append(sub_item)
                                move_to_filled.append(index)
                            item.change_quantity(-amount_have + leftovers)
                if item.quantity != 0:
                    index = non_filled.index(item)
                    filled_items.append(item)
                    move_to_filled.append(index)
        
        # removes the items that have been placed in the move list
        move_to_filled.sort(reverse=True)
        for index in move_to_filled:
            non_filled.pop(index)

        return filled_items
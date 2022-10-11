#10/8/22
# test item test
# this test is to create a 
# funtion where items in a list will automaticly fill items.

from random import randint


class Test_item:
    def __init__(self, name, quantity, limit):
        self.name = name
        self.quantity = quantity
        self.limit = limit
        if self.quantity > self.limit:
            self.quantity = self.limit
        elif self.quantity == 0:
            del self
    
    @property
    def stats(self):
        return self.name, self.quantity, self.limit, "thats it"

    @property
    def is_full(self):
        return self.quantity >= self.limit

    @property
    def empty_space(self):
        return self.limit - self.quantity

    def change_quantity(self, number):
        quantity = self.quantity
        quantity += number

        if quantity > self.limit:  # if the new quantity is more than 
            left_over = quantity - self.limit  # something like 30 - 20 = 10 left overs
            quantity = self.limit
        elif quantity <= 0:  # if the new quantity is below quantity  
            left_over = quantity * -1  # something like -4 * -1
            quantity = 0
        else:
            left_over = 0
        self.quantity = quantity
        return left_over

def create_items(number = 10):
    inventory = []
    for _ in range(number):
        item_base = items.get(randint(1, 4))
        item = Test_item(item_base[0], randint(1, item_base[1]), item_base[1])
        inventory.append(item)
    return inventory

def new_organizer(inventory):
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
        if not index in move_to_filled:
            for same_items in non_filled:
                print(same_items.stats)
                name_check = same_items.name == item_name
                not_same_check = not same_items == item
                index_not_check = not non_filled.index(same_items) in move_to_filled
                not_dead = same_items.quantity != 0 
                print("\n")

                if name_check and not_same_check and index_not_check and not_dead:
                    matching.append(same_items)

            # goes through matched items
            if len(matching) != 0:
                for sub_item in matching:
                    if item.quantity != 0:
                        amount_have = item.quantity

                        leftovers = sub_item.change_quantity(amount_have)
                        if sub_item.is_full:
                            index = non_filled.index(sub_item)
                            filled_items.append(sub_item)
                            move_to_filled.append(index)
                        item.change_quantity(-amount_have + leftovers)

            print(f"quantity {item.stats}")
            if item.quantity != 0:
                index = non_filled.index(item)
                filled_items.append(item)
                move_to_filled.append(index)
    
    move_to_filled.sort(reverse=True)
    print(move_to_filled)
    for index in move_to_filled:
        non_filled.pop(index)

    for item in non_filled:
        if item.quantity != 0:
            index = non_filled.index(item)
            non_filled.pop(index)

    print(f"\nFull or ish: {[item.stats for item in filled_items]}\nNeeds items: {[item.stats for item in non_filled]}\n")
    


items = {
    1 : ("potion", 20),
    2 : ("revive", 20),
    3 : ("sword", 1),
    4 : ("shield", 1)
}

inventory = create_items(50)
print(inventory)
del inventory[1]
print(inventory)

new_organizer(inventory)

# restart this <><



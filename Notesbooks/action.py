# This is to test if I can creaet dynamic dictonaries in python.
"""class player:
    def __init__(self, name, _list) -> None:
        pass
        self.name = name
        self.list = _list

class Action_test_1:
    def __init__(self) -> None:
        self.chars = [player("sadfklj", [1, 2, 4, 5, 6]), player("iou", [8, 0, 3, 5, 213])]
        self.current_place = 0

        self.actions = {
            "list": self.grab_list()
        }

    @property
    def update_actions(self):
        # update list
        print("updating")
        self.actions["list"]= self.grab_list()

    @property
    def current_player(self):
        return self.chars[self.current_place]

    def grab_list(self):
        return self.current_player.list

    def run_test(self):
        run = True
        while run:
            print(self.current_place)
            action = input("Action")
            if action == "next":
                self.current_place += 1
                if self.current_place + 1 > len(self.chars):
                    self.current_place = 0
                self.update_actions
            elif action == "info":
                print(self.current_player.name, self.current_player.list)
            elif action == "list":
                print(self.actions.get("list"))
            elif action == "quit":
                run = False
            else:
                print("!")
a = Action_test_1()
a.run_test()"""

a = {
    "a" : {
        "aa" : 3,
        "bb" : 4
    },
    "b" : 2
}
print(a["a"]["aa"])

# Notes
# dictonaries connot be dynamicly changed due to everything in the dictonarry being set and cannot be changed without updating it.
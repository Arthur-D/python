


class Robot:
    def __init__(self):
        self.name = properties["Name"]
        self.turns = properties["Turn amount"]
        self.cost = properties["Cost"]
        self.level = 1

    def get_name(self):
        return self.name

    def get_turns(self):
        return self.turns

    def get_cost(self):
        return self.cost

    def get_level(self):
        return self.level

    def decrease_turns(self):
        if self.turns > 0:
            self.turns -= 1
            if self.turns == 0:
                print(self.name, " robot complete")

    def increase_level(self):
        if self.level < 5:
            self.level += 1
            if self.level == 5:
                print("Max level reached!")
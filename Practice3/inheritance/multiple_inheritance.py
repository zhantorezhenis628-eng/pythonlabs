class Father:
    def skill(self):
        print("Gardening")

class Mother:
    def talent(self):
        print("Painting")

class Child(Father, Mother):
    pass

child = Child()
child.skill()
child.talent()

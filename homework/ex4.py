def print_info(**kwargs):
    """Print any named arguments"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="London")




def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
print_info(name="A", age=25, city="S")





class Person:
    def __init__(self, name):
        self.name = name
class Employee(Person):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary
e = Employee("Alice", 5000)
print(e.name, e.salary)



class Bird:
    def fly(self):
        print("Birds can fly")
class Penguin(Bird):
    def fly(self):
        print("Penguins can not fly")
b = Bird()
p = Penguin()
b.fly()
p.fly()
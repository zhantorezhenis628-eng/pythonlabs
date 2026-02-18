class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def display(self):
        print(f"Name: {self.name}, Grade: {self.grade}")

student1 = Student("John", 90)
student1.display()

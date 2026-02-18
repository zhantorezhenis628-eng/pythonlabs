class Employee:
    company_name = "TechCorp"   # Class variable

    def __init__(self, name):
        self.name = name        # Instance variable

emp1 = Employee("John")
emp2 = Employee("Alice")

print(emp1.company_name)
print(emp2.company_name)

Employee.company_name = "NewTech"

print(emp1.company_name)
print(emp2.company_name)

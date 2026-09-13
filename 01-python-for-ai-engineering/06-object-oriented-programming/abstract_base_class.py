from abc import ABC, abstractmethod


class Employee(ABC):
    """Abstract base class — cannot be instantiated directly."""

    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    @abstractmethod
    def calculate_salary(self):
        """Every subclass MUST implement this."""
        pass

    @abstractmethod
    def role_description(self):
        """Another required method."""
        pass

    @property
    @abstractmethod
    def department(self):
        """Abstract property — subclasses must define this too."""
        pass

    # Concrete method — shared by all subclasses, no need to override
    def summary(self):
        return (f"{self.name} | {self.department} | "
                f"{self.role_description()} | "
                f"Salary: ${self.calculate_salary():.2f}")


class Developer(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def role_description(self):
        return "Writes and maintains code"

    @property
    def department(self):
        return "Engineering"


class Manager(Employee):
    def __init__(self, name, base_salary, team_size):
        super().__init__(name, base_salary)
        self.team_size = team_size

    def calculate_salary(self):
        return self.base_salary + (self.team_size * 500)

    def role_description(self):
        return "Manages a team"

    @property
    def department(self):
        return "Management"


# ---- Demonstration ----

if __name__ == "__main__":
    # 1. Cannot instantiate the abstract base class
    try:
        e = Employee("Test", 50000)
    except TypeError as err:
        print(f"Error creating Employee: {err}\n")

    # 2. Concrete subclasses work fine
    dev = Developer("Alice", 70000, 5000)
    mgr = Manager("Bob", 90000, 4)

    print(dev.summary())
    print(mgr.summary())

    # 3. isinstance/issubclass work meaningfully
    print(f"\nIs dev an Employee? {isinstance(dev, Employee)}")
    print(f"Is Developer a subclass of Employee? {issubclass(Developer, Employee)}")

    # 4. Polymorphism — treat all employees uniformly
    print("\n--- All Employees ---")
    employees = [dev, mgr]
    total_payroll = sum(emp.calculate_salary() for emp in employees)
    for emp in employees:
        print(emp.summary())
    print(f"Total payroll: ${total_payroll:.2f}")

    # 5. What happens if a subclass forgets an abstract method
    class Intern(Employee):
        def calculate_salary(self):
            return self.base_salary

        # forgot role_description and department!

    try:
        i = Intern("Charlie", 20000)
    except TypeError as err:
        print(f"\nError creating Intern: {err}")
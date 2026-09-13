class Circle:
    def __init__(self, radius):
        self._radius = radius  # "private" backing variable

    @property
    def radius(self):          # getter — accessed like an attribute: c.radius
        return self._radius

    @radius.setter
    def radius(self, value):   # setter — c.radius = 5
        if value < 0:
            raise ValueError("radius can't be negative")
        self._radius = value

    @property
    def area(self):            # computed, read-only property
        return 3.14159 * self._radius ** 2


c = Circle(5)
print(c.radius)   # 5   (no parentheses — looks like plain attribute access)
print(c.area)     # 78.53975

c.radius = 10     # goes through the setter, validated
print(c.area)     # 314.159

c.radius = -1     # raises ValueError
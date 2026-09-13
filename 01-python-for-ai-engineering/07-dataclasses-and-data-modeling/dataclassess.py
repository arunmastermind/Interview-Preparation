from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    active: bool = True

u1 = User("Arun", 30)
u2 = User("Arun", 30)

print(u1)           # User(name='Arun', age=30, active=True)  — auto __repr__
print(u1 == u2)     # True — auto __eq__ (compares fields)
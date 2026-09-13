class JSONMixin:
    def to_json(self):
        return str(self.__dict__)  # simple stand-in for json.dumps

class ComparableMixin:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class User(JSONMixin, ComparableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

u1 = User("Arun", 30)
u2 = User("Arun", 30)

print(u1.to_json())   # {'name': 'Arun', 'age': 30}
print(u1 == u2)        # True — from ComparableMixin
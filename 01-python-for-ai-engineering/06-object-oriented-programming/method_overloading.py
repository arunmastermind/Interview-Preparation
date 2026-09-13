class A():
    def a(self):
        print("A -> a")

    def a(self,x):
        print("A -> a(x)")
    
    def a(self,x,y):
        print("A -> a(x,y)")

l = A()
# l.a() #Error: missing 2 required positional arguments: 'x' and 'y'
# l.a(10) #Error: missing 1 required positional argument: 'y'
l.a(10,20)

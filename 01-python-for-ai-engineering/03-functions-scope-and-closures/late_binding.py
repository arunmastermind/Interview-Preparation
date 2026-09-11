a = range(3)
b = [1,2,3,4]

x = [lambda: i for i in a]
y = [lambda: i for i in b]

p = list(f() for f in x)
q = list(f() for f in y)

print(a)
print(b)
print("-"*20)
print(x)
print(y)
print("-"*20)
print(p) #[2, 2, 2]
print(q) #[4, 4, 4, 4]

print("-"*20)

#solution

x = [lambda i=i: i for i in a]
y = [lambda i=i: i for i in b]

p = list(f() for f in x)
q = list(f() for f in y)

print("-"*20)
print(p) #[0,1,2]
print(q) #[1,2,3,4]
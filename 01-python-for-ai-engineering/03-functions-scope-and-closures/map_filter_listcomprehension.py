a = [1,2,3]
print(a)
print("-"*50)

b = list(map(lambda x:x+1, a))
c = list(filter(lambda x: x>1, a))
print(b)
print(c)
print("-"*50)

# list compehension 
x= [p for p in a]
print(x)

y = [p for p in a if p>1]
print(y)
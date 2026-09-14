import sys

items = []
alias = items
print(sys.getrefcount(items))

del alias
print(sys.getrefcount(items))
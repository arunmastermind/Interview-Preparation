import copy

print("=== 1. ORIGINAL LIST ===")
# A nested list: a list containing another list
original = [[1, 2, 3], [4, 5, 6]]
print(f"Original: {original}\n")


print("=== 2. ASSIGNMENT (assigned) ===")
# Assignment does NOT copy data. It just creates a new variable name
# pointing to the exact same object in memory.
assigned = original

# Modifying an element via 'assigned' affects 'original'
assigned[0][0] = 99
print(f"Assigned modified: {assigned}")
print(f"Original after assignment change: {original}")
# Notice that original[0][0] changed to 99 because they point to the same list.
# Reset original for next demonstration:
original = [[1, 2, 3], [4, 5, 6]]
print("-" * 50)


print("=== 3. SHALLOW COPY (shallow) ===")
# Creates a new outer list, but the inner lists are shared (references).
shallow = copy.copy(original)

# Test 1: Modifying a top-level element (adding a new inner list)
shallow.append([7, 8, 9])
print(f"Shallow (added item): {shallow}")
print(f"Original (unaffected at top-level): {original}")

# Test 2: Modifying a nested (inner) element
shallow[0][0] = 99  # Modifying inside the shared inner list
print(f"Shallow modified inner: {shallow}")
print(f"Original after inner change: {original}")
# Notice: Original's inner list ALSO changed because inner elements are shared!
# Reset original:
original = [[1, 2, 3], [4, 5, 6]]
print("-" * 50)


print("=== 4. DEEP COPY (deep) ===")
# Recursively duplicates everything: a brand new outer list AND brand new inner lists.
deep = copy.deepcopy(original)

# Modifying the inner element of the deep copy
deep[0][0] = 99

print(f"Deep copy modified: {deep}")
print(f"Original after deep copy change: {original}")
# Notice: Original remains completely untouched! The deep copy is 100% independent.
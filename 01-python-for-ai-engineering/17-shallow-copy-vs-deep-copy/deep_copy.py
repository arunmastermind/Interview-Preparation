import copy

original = {"tags": ["rag", "llm"]}
deep = copy.deepcopy(original)

deep["tags"].append("agent")
print(original["tags"])  # unchanged
print(deep["tags"])
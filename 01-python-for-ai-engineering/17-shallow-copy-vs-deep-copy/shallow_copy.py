import copy

original = {"tags": ["rag", "llm"]}
shallow = copy.copy(original)

shallow["tags"].append("agent")
print(original["tags"])  # also changed
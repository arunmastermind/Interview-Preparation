def read_documents(documents):
    for document in documents:
        cleaned = document.strip().lower()
        if cleaned:
            yield cleaned

for document in read_documents([" RAG ", "", " LLM "]):
    print(document)

print("-"*10, " Lazy evaluation ", "-"*10)

def lazy_eval():
    print("Starting lazy evaluation")
    yield 1
    print("Still lazy")
    yield 2
    print("Still lazy")
    yield 3
    print("Done")

# Lazy evaluation - only runs when next() is called
for value in lazy_eval():
    print(value)

print("-"*10, " Generator expression ", "-"*10)

gen_exp = (x * 1 for x in range(5))

print(next(gen_exp))
print(next(gen_exp))
print(next(gen_exp))
print(next(gen_exp))
print(next(gen_exp))
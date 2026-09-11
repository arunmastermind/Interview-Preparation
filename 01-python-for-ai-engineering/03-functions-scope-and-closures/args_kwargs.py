# def log_event(event, *tags, **metadata):
#     print("event:", event)
#     print("tags:", tags)
#     print("metadata:", metadata)

# log_event("llm_request", "production", "rag", latency_ms=120, model="gpt")

# def val(*a):
#     print(a)
#     print(type(a))

# val("A", "B")

def log(event, *tags, level="INFO", **metadata):
    print(event, tags, level, metadata)

log("request", "rag", "production", level="DEBUG", latency=120)
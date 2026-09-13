from functools import wraps

def trimmer(func):    
    @wraps(func)
    def wrapper(text):
        return func(text.strip())
    return wrapper


@trimmer
def test(text):
    return text

print(test(" Arun "))

print("-"*10, " Multiple decorators ", "-"*10)
def lower_case(func):
    @wraps(func)
    def wrapper(text):
        return func(text.lower())
    return wrapper

@lower_case
@trimmer
def test(text):
    return text

print(test(" Arun "))
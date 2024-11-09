def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()  # Call the original function
        print("After the function runs")
    return wrapper



@my_decorator
def say_hello():
    print("Hello!")

say_hello()



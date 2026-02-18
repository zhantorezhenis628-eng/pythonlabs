def display_info(*args, **kwargs):
    """
    Print all positional and keyword arguments.
    """
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

display_info(1, 2, 3, name="Alice", age=25)

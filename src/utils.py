import threading


def threaded(fun):
    """A decorator that runs a function on a thread."""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fun, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper

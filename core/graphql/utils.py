def login_required(func):
    def wrapper(*args, **kwargs):
        info = args[2]
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to perform this action.")
        return func(*args, **kwargs)

    return wrapper


def validate_rate(rate):
    try:
        rate = int(rate)
    except ValueError:
        raise Exception("Rate must mu number value.")
    if rate < 1 or rate > 10:
        raise Exception("Rate value must be between 1 and 10")

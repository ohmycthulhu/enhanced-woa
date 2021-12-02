def expect_error(func, message_error, message_success):
    try:
        func()
        print(message_error)
    except:
        print(message_success)
        return True

    return False


def expect_no_error(func, message_error, message_success):
    try:
        func()
        print(message_success)
        return True
    except:
        print(message_error)
        raise
        return False

    return True


def expect_value(expected, actual):
    if expected != actual:
        print(f"{actual} does not match expected {expected}")
        return False
    return True


def expect_different(expected, actual):
    if expected == actual:
        print(f"{actual} expected to not match {expected}")
        return False
    return True


def expect_not_none(actual):
    if actual is None:
        print(f"Value expected to not be None")
        return False
    return True


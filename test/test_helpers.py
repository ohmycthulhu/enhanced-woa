def expect_error(func, message_error, message_success):
    try:
        func()
        print(message_error)
        return False
    except:
        print(message_success)
        return True


def expect_no_error(func, message_error, message_success):
    try:
        func()
        print(message_success)
        return True
    except:
        print(message_error)
        return False


def expect_value(expected, actual):
    if expected != actual:
        print(f"{actual} does not match expected {expected}")
    return actual == expected


def expect_different(expected, actual):
    if expected == actual:
        print(f"{actual} expected to not match {expected}")
    return actual != expected


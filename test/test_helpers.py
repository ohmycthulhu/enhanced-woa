import os.path


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
    except:
        print(message_error)
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


def expect_file_exists(actual, remove_file=True):
    if not os.path.exists(actual):
        print(f'Could not find expected file - {actual}')
        return False
    if remove_file:
        os.remove(actual)
    return True

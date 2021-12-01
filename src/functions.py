import numpy as np


def ackley_function(a, b, c, xs):
    p_1 = -b * np.mean([x ** 2 for x in xs])
    p_2 = np.mean([np.cos(c * x) for x in xs])

    return -a * np.exp(p_1) - np.exp(p_2) + a + np.e


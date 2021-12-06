import numpy as np


def ackley_function(a, b, c, xs):
    p_1 = -b * np.mean([x ** 2 for x in xs])
    p_2 = np.mean([np.cos(c * x) for x in xs])

    return -a * np.exp(p_1) - np.exp(p_2) + a + np.e


def rastrigin_function(xs):
    d = len(xs)
    return 10 * d + sum([x**2 - 10 * np.cos(2 * np.pi * x) for x in xs])


def rosenbrok_function(xs):
    return sum([
        (100 * (xs[i + 1] - xs[i]**2)**2) + (xs[i] - 1)**2
        for i in range(len(xs) - 1)
    ])


def schwefel_function(xs):
    d = len(xs)
    return 418.9829 * d - sum([x * np.sin(np.sqrt(np.abs(x))) for x in xs])


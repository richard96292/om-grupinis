import math
from inspect import signature
from random import uniform

from output import output_data


# https://www.sfu.ca/~ssurjano/grlee12.html
def gramacy_lee(x: float) -> float:
    return (math.sin(10 * math.pi * x) / (2 * x)) + ((x - 1) ** 4)


# https://www.sfu.ca/~ssurjano/camel6.html
def six_hump_camel(x1: float, x2: float) -> float:
    part_one = (4 - 2.1 * x1 ** 2 + (x1 ** 4 / 3)) * x1 ** 2
    part_two = x1 * x2
    part_three = (-4 + 4 * x2 ** 2) * x2 ** 2
    return part_one + part_two + part_three


def acceptance_criterion(cur_fval: float, prev_fval: float, temperature: float) -> bool:
    delta_fval = cur_fval - prev_fval
    if delta_fval < 0:
        return True
    else:
        r = uniform(0, 1)
        if r < math.exp(-delta_fval / temperature):
            return True
        else:
            return False


def generate_new_point(X: list[float], bounds: [list[list]]) -> list[float]:
    X_new = []
    for i, x in enumerate(X):
        while True:
            x_new = x + uniform(-0.2, 0.2)
            if x_new >= bounds[i][0] and x_new <= bounds[i][1]:
                X_new.append(x_new)
                break

    return X_new


# The probability of convergence is not 1. Sometimes it won't find the global minimum.
def simulated_annealing(
        f, bounds: list[list[float]], temp_max: float, verbose: bool = False
) -> dict:
    data = {"minimum": [], "iterations": 0, "points": [], "temperatures": []}

    var_count = len(signature(f).parameters)
    if var_count != len(bounds):
        print("Variable count doesn't match the bound count.")

    temp = temp_max

    X = [uniform(bounds[i][0], bounds[i][1]) for i in range(0, var_count)]
    E = f(*X)
    data["points"].append(X)

    if verbose:
        print(f"Initial temperature: {temp}")
        print(f"Initial solution: {X}")
        print(f"Energy of initial solution: {E}")

    i = 0
    while temp > 0.0000000001:  # Why this many zeros? Don't ask questions.
        i = i + 1

        X_new = generate_new_point(X, bounds)
        E_new = f(*X_new)

        if acceptance_criterion(E_new, E, temp):
            X = X_new
            E = E_new

        data["points"].append(X)
        data["temperatures"].append(temp)
        data["iterations"] = len(data["points"])
        data["minimum"] = [X, f(*X)]

        temp = temp * 0.95

    if verbose:
        print(f(*X))
    return data


def main():
    output_data(simulated_annealing, gramacy_lee, six_hump_camel)


if __name__ == "__main__":
    main()

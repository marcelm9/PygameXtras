"""idea: given a structure, check if an input follows the given structure"""

def check(test, schema):
    pass

s = {
    "a": {
        "b": int,
        "c": float,
        "d": [int, float]
    }
}

t = {
    "a": {
        "b": 10,
        "c": 3.1417,
        "d": [20, 50.10]
    }
}

print(check(t, s))
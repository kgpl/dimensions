import sys
sys.path.insert(0, r"../src")
from dimensions import measurement

Measurement = measurement.Measurement

def test_initialize():
    mass = Measurement("Weight")
    print(type(mass), flush=True)

test_initialize()
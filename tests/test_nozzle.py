import pytest
from combustion_chamber_rpa import *
from nozzle_conical import *

combustion_pressure = 20e5
of_ratio = 1
area_ratio = 3.5
efficiency = 0.97
thrust = 7500
ambient_pressure = 1e5

@pytest.fixture
def nozzle():
    combustion_chamber = CombustionChamberRpa()
    combustion_chamber.read_rpa_data("resources/n2o_ethanol_95.txt")
    combustion_chamber.recalculate_combustion_conditions(of_ratio, combustion_pressure)

    nozzle = NozzleConical(area_ratio, efficiency, 30, 15)
    nozzle.set_combustion_conditions(combustion_chamber.get_combustion_conditions())
    nozzle.recalculate(thrust, ambient_pressure)
    return nozzle


def test_pressure_ratio(nozzle):
    assert pytest.approx(nozzle.pressure_ratio, None, 1e-4) == 0.047411


def test_exhaust_velocity(nozzle):
    assert pytest.approx(nozzle.exhaust_velocity, None, 1e-1) == 1478.2


def test_exhaust_velocity(nozzle):
    assert pytest.approx(nozzle.exit_pressure, None, 1e-1) == nozzle.pressure_ratio * nozzle.combustion_pressure


def test_throat_diameter(nozzle):
    assert pytest.approx(nozzle.throat_diameter, None, 1e-4) == 0.0593

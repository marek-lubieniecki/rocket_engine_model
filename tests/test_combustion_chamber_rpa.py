
import pytest
from combustion_chamber_rpa import *
from utility import *

combustion_pressure = 20e5
of_ratio = 1
mass_flow = 1
throat_area = area_from_diameter(0.05)

@pytest.fixture
def combustion_chamber_rpa():
    combustion_chamber = CombustionChamberRpa()
    combustion_chamber.read_rpa_data("resources/n2o_ethanol_95.txt")
    combustion_chamber.recalculate_combustion_conditions(of_ratio, combustion_pressure)
    combustion_chamber.calculate_diameter(mass_flow)
    combustion_chamber.calculate_length(throat_area)
    return combustion_chamber


def test_read_rpa_data(combustion_chamber_rpa):
    assert combustion_chamber_rpa.combustion_pressures[0] == 20e5


def test_ideal_temperature_interpolation(combustion_chamber_rpa):
    assert combustion_chamber_rpa.get_ideal_combustion_temperature(of_ratio, combustion_pressure) == 1122.2712


def test_real_temperature_interpolation(combustion_chamber_rpa):
    assert combustion_chamber_rpa.get_real_combustion_temperature(of_ratio, combustion_pressure) == 1122.2712*0.95


def test_molecular_weight_interpolation(combustion_chamber_rpa):
    assert combustion_chamber_rpa.get_molecular_mass(of_ratio, combustion_pressure) == 18.4047/1e3


def test_gamma_interpolation(combustion_chamber_rpa):
    assert combustion_chamber_rpa.get_gamma(of_ratio, combustion_pressure) == 1.2571


def test_k_interpolation(combustion_chamber_rpa):
    assert combustion_chamber_rpa.get_k(of_ratio, combustion_pressure) == 1.1485


def test_density_calculation(combustion_chamber_rpa):
    assert pytest.approx(combustion_chamber_rpa.density, None, 1e-4) == 4.1526


def test_speed_of_sound_calculation(combustion_chamber_rpa):
    assert pytest.approx(combustion_chamber_rpa.speed_sound, None, 1e-4) == 778.1015


def test_diameter_calculation(combustion_chamber_rpa):
    assert pytest.approx(combustion_chamber_rpa.diameter, None, 1e-4) == 0.06277


def test_volume_calculation(combustion_chamber_rpa):
    assert pytest.approx(combustion_chamber_rpa.volume, None, 1e-4) == 0.001963495


def test_length_calculation(combustion_chamber_rpa):
    assert pytest.approx(combustion_chamber_rpa.length, None, 1e-4) == 0.6344






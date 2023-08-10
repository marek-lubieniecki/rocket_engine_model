from utility import *


class CombustionChamber:

    def __init__(self, mach_number, characteristic_length, efficiency):
        self.mach_number = mach_number
        self.characteristic_length = characteristic_length
        self.efficiency = efficiency

        self.length = 0
        self.diameter = 0
        self.cross_section_area = 0
        self.volume = 0

        self.of_ratio = 0
        self.combustion_pressure = 0
        self.ideal_temperature = 0
        self.real_temperature = 0
        self.molecular_mass = 0
        self.gamma = 0
        self.k = 0

        self.density = 0
        self.speed_sound = 0
        self.velocity = 0

        self.temperature_interpolator = None
        self.molecular_mass_interpolator = None
        self.gamma_interpolator = None
        self.k_interpolator = None

    def calculate_dimensions(self, mass_flow, throat_area):
        self.calculate_diameter(mass_flow)
        self.calculate_length(throat_area)

    def calculate_length(self, throat_area):
        self.volume = throat_area * self.characteristic_length
        self.length = self.volume / self.cross_section_area

    def calculate_diameter(self, mass_flow):
        self.recalculate_combustion_conditions(self.of_ratio, self.combustion_pressure)
        self.density = gas_density(self.combustion_pressure, self.real_temperature, self.molecular_mass)
        self.speed_sound = sound_speed(self.gamma, self.molecular_mass, self.real_temperature)
        self.velocity = self.speed_sound * self.mach_number
        self.cross_section_area = mass_flow/(self.velocity*self.density)
        self.diameter = diameter_from_area(self.cross_section_area)

    def recalculate_combustion_conditions(self, of_ratio, combustion_pressure):
        self.of_ratio = of_ratio
        self.combustion_pressure = combustion_pressure
        self.ideal_temperature = self.get_ideal_combustion_temperature(of_ratio, combustion_pressure)
        self.real_temperature = self.get_real_combustion_temperature(of_ratio, combustion_pressure)
        self.molecular_mass = self.get_molecular_mass(of_ratio, combustion_pressure)
        self.gamma = self.get_gamma(of_ratio, combustion_pressure)
        self.k = self.get_k(of_ratio, combustion_pressure)

    def get_ideal_combustion_temperature(self, of_ratio, combustion_pressure):
        return self.temperature_interpolator((of_ratio, combustion_pressure)).item()

    def get_real_combustion_temperature(self, of_ratio, combustion_pressure):
        return self.efficiency * self.temperature_interpolator((of_ratio, combustion_pressure)).item()

    def get_molecular_mass(self, of_ratio, combustion_pressure):
        return self.molecular_mass_interpolator((of_ratio, combustion_pressure)).item()

    def get_gamma(self, of_ratio, combustion_pressure):
        return self.gamma_interpolator((of_ratio, combustion_pressure)).item()

    def get_k(self, of_ratio, combustion_pressure):
        return self.k_interpolator((of_ratio, combustion_pressure)).item()

    def get_combustion_conditions(self):
        return CombustionChamberConditions(self.combustion_pressure, self.real_temperature, self.molecular_mass,
                                           self.gamma, self.mach_number)

    def print_combustion_properties(self):
        print("Combustion pressure: ", self.combustion_pressure)
        print("Combustion temperature: ", self.combustion_temperature)
        print("Heat capacity ratio: ", self.heat_capacity_ratio)
        print("Mean molecular weight: ", self.gas.mean_molecular_weight)
        print("Individual gas constant: ", self.individual_gas_constant)

class CombustionChamberConditions():
    def __init__(self, pressure, temperature, molecular_mass, gamma, mach):
        self.pressure = pressure
        self.temperature = temperature
        self.molecular_mass = molecular_mass
        self.gamma = gamma
        self.mach = mach
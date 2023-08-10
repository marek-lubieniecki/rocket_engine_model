from combustion_chamber import *
import cantera as ct
import numpy as np


class CombustionChamberCantera(CombustionChamber):
    def __init__(self,fuel, oxidiser, mach_number=0.15, characteristic_length=1, c_star_efficiency=0.95):
        super().__init__(mach_number, characteristic_length, c_star_efficiency)

        self.fuel = fuel
        self.oxidiser = oxidiser
        self.gas = ct.Solution('gri30.xml')

        self.equivalence_ratio = 1
        self.stoichiometric_of_ratio = 1

        self.heat_capacity_cv = 0
        self.heat_capacity_cp = 0
        self.heat_capacity_ratio = 1

        self.individual_gas_constant = 1
        self.universal_gas_constant = 8.31446261815324
        self.initial_temperature = 300
        self.gas.TP = self.initial_temperature, ct.one_atm * self.combustion_pressure / 1e5

    def calculate_combustion_chamber_properties(self):
        # https: // kyleniemeyer.github.io / rocket - propulsion / thermochemistry / cea_cantera.html?fbclid = IwAR2Lg2Eqt5xj2m4KEsQyCwRydEPPwLQ4ERNfOT - 6
        # GLoTrX1gVFyaJTuIi58
        self.gas = ct.Solution('gri30.xml')
        nsp = self.gas.n_species
        iFu = self.gas.species_index(self.fuel)  # index of Fuel
        iOx = self.gas.species_index(self.oxidiser)  # index of Oxidize
        phi = self.oxidiser_fuel_ratio

        y = np.zeros(nsp)
        y[iFu] = 1.0  # we want mass fractions
        y[iOx] = phi

        self.gas.TP = 300.0, ct.one_atm * self.combustion_pressure/1e5
        self.gas.Y = y
        self.gas.equilibrate('HP', solver="gibbs")

        self.temperature = self.c_star_efficiency * self.gas.T
        self.molecular_mass = self.gas.mean_molecular_weight
        self.heat_capacity_cp = self.gas.cp
        self.heat_capacity_cv = self.gas.cv
        self.heat_capacity_ratio = self.gas.cp / self.gas.cv
        self.individual_gas_constant = self.universal_gas_constant/(self.gas.mean_molecular_weight/1e3)

    # def calculate_stoichiometric_of_ratio(self):
    #    self.gas.set_equivalence_ratio(1, self.fuel, self.oxidiser)
    #   fuel = self.gas["C3H8"].Y[0]
    #   oxidiser = self.gas["O2"].Y[0]
    #   self.stoichiometric_of_ratio = oxidiser/fuel
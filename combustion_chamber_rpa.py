import numpy as np
import scipy.interpolate as interp
from combustion_chamber import *


class CombustionChamberRpa(CombustionChamber):
    def __init__(self,  mach_number=0.1, characteristic_length=1, efficiency=0.95):
        super().__init__(mach_number, characteristic_length, efficiency)
        self.filepath = None
        self.file = None

        self.of_ratios = None
        self.combustion_pressures = None
        self.temperature_values = None
        self.molecular_mass_values = None
        self.gamma_values = None
        self.k_values = None

    def read_rpa_data(self, filepath):
        self.filepath = filepath
        self.file = open(self.filepath, "r")
        lines = self.file.readlines();
        self.of_ratios = []
        self.combustion_pressures = []

        i = 0
        j = 0
        for line_no, line in enumerate(lines):
            if line_no >= 3:
                split_line = line.split()
                of_ratio = float(split_line[0])
                combustion_pressure = float(split_line[1])*1e5

                if self.of_ratios.count(of_ratio) == 0:
                    i = i + 1
                    self.of_ratios.append(float(of_ratio))

                if self.combustion_pressures.count(combustion_pressure) == 0:
                    j = j+1
                    self.combustion_pressures.append(float(combustion_pressure))

            self.temperature_values = np.zeros((i, j))
            self.molecular_mass_values = np.zeros((i, j))
            self.gamma_values = np.zeros((i, j))
            self.k_values = np.zeros((i, j))

        for line_no, line in enumerate(lines):
            if line_no >= 3:
                split_line = line.split()
                of_ratio = float(split_line[0])
                combustion_pressure = float(split_line[1])*1e5

                i = self.of_ratios.index(of_ratio)
                j = self.combustion_pressures.index(combustion_pressure)

                self.temperature_values[i, j] = float(split_line[5])
                self.molecular_mass_values[i, j] = float(split_line[6])/1e3
                self.gamma_values[i, j] = float(split_line[7])
                self.k_values[i, j] =  float(split_line[8])

        x = np.array(self.of_ratios)
        y = np.array(self.combustion_pressures)

        self.temperature_interpolator = interp.RegularGridInterpolator((x, y), self.temperature_values)
        self.molecular_mass_interpolator = interp.RegularGridInterpolator((x, y), self.molecular_mass_values)
        self.gamma_interpolator = interp.RegularGridInterpolator((x, y), self.gamma_values)
        self.k_interpolator = interp.RegularGridInterpolator((x, y), self.k_values)

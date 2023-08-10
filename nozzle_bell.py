from nozzle import *


class NozzleBell(Nozzle):
    def __init__(self, area_ratio, efficiency, conv_angle, div_inlet_angle, div_outlet_angle, length_fraction):
        super().__init__(area_ratio, efficiency)


    def set_length_fraction(self, length_fraction):
        self.length_fraction = length_fraction
        self.calculate_angles()

    def calculate_angles(self):

        if self.expansion_ratio > 50:
            expansion_ratio = 50
        elif self.expansion_ratio < 5:
            expansion_ratio = 5
        else:
            expansion_ratio = self.expansion_ratio

        self.initial_angle = self.initial_angle_function(expansion_ratio)
        self.outlet_angle = self.outlet_angle_function(expansion_ratio)
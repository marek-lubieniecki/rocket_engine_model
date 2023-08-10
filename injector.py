from utility import *
import math


class Injector:

    def __init__(self, oxidiser, fuel, total_mass_flow, oxidiser_fuel_ratio, pressure_drop, discharge_coefficient ):

        self.oxidiser = oxidiser
        self.fuel = fuel
        self.pressure_drop = pressure_drop
        self.total_mass_flow = total_mass_flow
        self.oxidiser_fuel_ratio = oxidiser_fuel_ratio
        self.discharge_coefficient = discharge_coefficient
        self.real_of_ratio = 0

        self.oxidiser_hole_number = 0
        self.fuel_hole_number = 0
        self.oxidiser_hole_diameter = 0.002  # 2mm holes like in SF-1000
        self.hole_area = area_from_diameter(self.hole_diameter)

        self.fuel_total_area = 0
        self.oxidiser_total_area = 0

        self.oxidiser_mass_flow = 0
        self.fuel_mass_flow = 0
        self.update_injector()

    def calculate_mass_flows(self):
        self.oxidiser_mass_flow = self.oxidiser_fuel_ratio * self.total_mass_flow / (1 + self.oxidiser_fuel_ratio)
        self.fuel_mass_flow = self.total_mass_flow - self.oxidiser_mass_flow

    def calculate_fuel_hole_number(self):
        self.fuel_total_area = self.fuel_mass_flow / (self.discharge_coefficient * math.sqrt(2* self.fuel.density * self.pressure_drop))
        self.fuel_hole_number = math.floor(self.fuel_total_area/self.hole_area)
        self.fuel_real_area = self.fuel_hole_number * self.hole_area

    def calculate_oxidiser_hole_number(self):
        self.oxidiser_total_area = self.oxidiser_mass_flow / (self.discharge_coefficient * math.sqrt(2* self.oxidiser.density * self.pressure_drop))
        self.oxidiser_hole_number = round(self.oxidiser_total_area / self.hole_area)
        self.oxidiser_real_area = self.oxidiser_hole_number * self.hole_area

    def calculate_real_mass_flows(self):
        self.real_oxidiser_mass_flow = self.discharge_coefficient * self.oxidiser_real_area * math.sqrt(2*self.oxidiser.density * self.pressure_drop)
        self.real_fuel_mass_flow = self.discharge_coefficient * self.fuel_real_area * math.sqrt(2*self.fuel.density * self.pressure_drop)
        self.real_of_ratio = self.real_oxidiser_mass_flow / self.real_fuel_mass_flow

    def update_injector(self):
        self.calculate_mass_flows()
        self.calculate_fuel_hole_number()
        self.calculate_oxidiser_hole_number()
        self.calculate_real_mass_flows()

    def print_info(self):
        print("Total mass flow: " + str(self.total_mass_flow))
        print("Oxidiser mass flow: " + str(self.oxidiser_mass_flow))
        print("Fuel mass flow: " + str(self.fuel_mass_flow))
        print("Oxidiser hole number: " + str(self.oxidiser_hole_number))
        print("Fuel hole number: " + str(self.fuel_hole_number))
        print("Real OF ratio: " + str(self.real_of_ratio))
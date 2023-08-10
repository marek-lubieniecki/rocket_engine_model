import cantera as ct
import numpy as np
from injector import *
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


class Engine:

    def __init__(self, oxidiser, fuel, combustion_pressure,  oxidiser_fuel_ratio, injector, combustion_chamber, nozzle):

        self.oxidiser = oxidiser
        self.fuel = fuel
        self.combustion_pressure = combustion_pressure
        self.oxidiser_fuel_ratio = oxidiser_fuel_ratio
        self.injector = injector
        self.combustion_chamber = combustion_chamber
        self.nozzle = nozzle

        self.specific_impulse = 0

        self.vacuum_exit_velocity = 0
        self.vacuum_specific_impulse = 0

        self.mass_flow = 0
        self.oxidiser_mass_flow = 0
        self.fuel_mass_flow = 0

    def calculate(self, thrust, ambient_pressure):
        self.combustion_chamber.recalculate_combustion_conditions(self.oxidiser_fuel_ratio, self.combustion_pressure)
        self.nozzle.set_combustion_conditions(self.combustion_chamber.get_combustion_conditions())
        self.nozzle.recalculate(thrust, ambient_pressure)
        self.combustion_chamber.calculate_dimensions(self.nozzle.mass_flow, self.nozzle.throat_area)
        self.nozzle.calculate_profile(self.combustion_chamber.diameter, self.combustion_chamber.length)
        self.nozzle.calculate_isp(ambient_pressure)
        self.nozzle.calculate_axial_flow_properties()

    def draw(self):
        self.nozzle.draw()

       # policz średnicę komory spalania
       # policz długość komory spalania
       # policz kształt zbieżnej części dyszy
       # policz kształt rozbieżnej części dyszy
       # policz średnicę wzdłuż całego silnika
       # policz prędkość i temperatury wzdłuż całego silnika
       # policz współczynnik wymiany ciepła wzdłuż całego silnika od wewnątrz
       # policz współczynnik wymiany ciepła wzdłuż kanału chłodzącego
       # policz rozkład temperatur
       # policz wtryskiwacz


    def set_oxidiser_fuel_ratio(self, of_ratio):
        self.oxidiser_fuel_ratio = of_ratio
        self.equivalence_ratio = of_ratio / self.stoichiometric_of_ratio

    def calculate_current_thrust(self, ambient_pressure):
        return self.nozzle.mass_flow * self.nozzle.exhaust_velocity + self.nozzle.exit_area * (self.nozzle.exit_pressure - ambient_pressure)

    def print_info(self):
        print('Mass flow:', self.nozzle.mass_flow)
        print('Throat diameter: ', self.nozzle.throat_diameter)
        print('Exit diameter: ', self.nozzle.exit_diameter)
        print('Exit pressure: ', self.nozzle.exit_pressure)
        print('Chamber diameter: ', self.combustion_chamber.diameter)
        print('Chamber length: ', self.combustion_chamber.length)
        print('ISP: ', self.nozzle.isp)

    def calculate_total_length(self):
        self.calculate_combustion_chamber_dimensions()
        self.calculate_nozzle_length()
        self.total_length = self.cc_length + self.nozzle_total_length


    def draw_engine_contour(self):
        cc_axial_start = 0
        cc_axial_end = self.cc_length
        throat_axial = cc_axial_end + self.nozzle_converging_length
        exit_axial = throat_axial + self.nozzle_diverging_length_conical

        axial_coordinates = np.array([cc_axial_start, cc_axial_end, throat_axial, exit_axial])
        radial_coordinates = np.array([self.cc_diameter/2, self.cc_diameter/2, self.throat_diameter/2, self.exit_diameter/2])

        plt.plot(axial_coordinates, radial_coordinates, color='blue', linewidth=2)
        plt.plot(axial_coordinates, -radial_coordinates, color='blue', linewidth=2)
        plt.grid(b=True, which='major')
        plt.grid(b=True, which='minor')
        plt.minorticks_on()
        plt.ylim(-0.1, 0.1)
        plt.xlim(0, 1)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')
        plt.show()




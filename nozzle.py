import math
from abc import abstractmethod

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from utility import *


class Nozzle:

    def __init__(self, area_ratio, efficiency):

        self.cc_conditions = None

        self.area_ratio = area_ratio
        self.efficiency = efficiency

        self.combustion_temperature = 0
        self.combustion_pressure = 0
        self.molecular_mass = 0
        self.heat_capacity_ratio = 0
        self.individual_gas_constant = 0

        self.throat_area = 0
        self.throat_diameter = 0
        self.throat_radius = 0
        self.throat_temperature = 0
        self.throat_pressure = 0

        self.exit_area = 0
        self.exit_diameter = 0
        self.exit_radius = 0
        self.exit_pressure = 0

        self.isp = 0

        self.profile_interpolator = None

        #self.initial_angle_array = np.genfromtxt("nozzle_initial_angle.csv")
        #self.outlet_angle_array = np.genfromtxt("nozzle_outlet_angle.csv")

        #self.initial_angle_function = interp1d(self.initial_angle_array[:, 1], self.initial_angle_array[:, 2])
        #self.outlet_angle_function = interp1d(self.initial_angle_array[:, 1], self.outlet_angle_array[:, 2])

        self.pressure_ratio = 0
        self.atmospheric_pressure_ratio = 0
        self.atmospheric_area_ratio = 0
        self.mass_flow = 0
        self.exhaust_velocity = 0

        self.xs = None
        self.ys = None
        self.throat_x = 0
        self.nozzle_start_x = 0
        self.nozzle_end_x =0

        self.axials = []
        self.radials = []
        self.temperatures = []
        self.pressures = []
        self.machs = []
        self.velocities= []

        self.backward_x = []
        self.backward_mach = []
        self.backward_temperature = []
        self.backward_pressure = []

        self.forward_x = []
        self.forward_mach = []
        self.forward_temperature = []
        self.forward_pressure = []

    def set_combustion_conditions(self, cc_conditions):
        self.cc_conditions = cc_conditions
        self.combustion_temperature = cc_conditions.temperature
        self.combustion_pressure = cc_conditions.pressure
        self.molecular_mass = cc_conditions.molecular_mass
        self.heat_capacity_ratio = cc_conditions.gamma
        self.individual_gas_constant = 8.314/self.molecular_mass

    def recalculate(self, thrust, atmospheric_pressure):
        #calculate pressure ratio
        self.calculate_pressure_ratio()
        self.exhaust_velocity = self.calculate_exhaust_velocity(self.pressure_ratio)
        self.calculate_areas_and_mass_flow(thrust, atmospheric_pressure)

    def calculate_pressure_ratio(self):
        self.pressure_ratio = fsolve(ratios, np.array(0.0001), args=(self.area_ratio, self.heat_capacity_ratio)).item()
        self.exit_pressure = self.pressure_ratio * self.combustion_pressure

    def calculate_exhaust_velocity(self, pressure_ratio):
        A = self.heat_capacity_ratio/(self.heat_capacity_ratio-1)
        B = 1 - math.pow(pressure_ratio, (self.heat_capacity_ratio-1)/self.heat_capacity_ratio)
        exhaust_velocity = math.sqrt(2*A*self.individual_gas_constant*self.combustion_temperature*B)
        return exhaust_velocity

    def calculate_areas_and_mass_flow(self, thrust, ambient_pressure):
        self.exit_area = 0
        self.calculate_mass_flow(thrust, ambient_pressure)
        iteration_number = 1
        mass_flow_tolerance = 0.01  # kg/s
        mass_flow_unbalance = True
        while mass_flow_unbalance:
            old_mass_flow = self.mass_flow
            self.calculate_nozzle_areas()
            self.calculate_mass_flow(thrust, ambient_pressure)
            mass_flow_difference = self.mass_flow - old_mass_flow
            mass_flow_unbalance = (abs(mass_flow_difference) > mass_flow_tolerance)
            print("Iteration number: ", iteration_number, " Previous mass flow: ", old_mass_flow,
                  " Current mass flow: ", self.mass_flow, " Mass flow difference: ", mass_flow_difference)
            print("Iteration number: ", iteration_number, " Throat diameter: ", self.throat_diameter * 1e3,
                  " Exit diameter : ", self.exit_diameter * 1e3)
            iteration_number = iteration_number + 1

    def calculate_mass_flow(self, thrust, ambient_pressure):
        self.mass_flow = (thrust - self.exit_area * (self.exit_pressure - ambient_pressure)) / self.exhaust_velocity
        self.mass_flow = self.mass_flow / self.efficiency

    def calculate_nozzle_areas(self):
        throat_pressure = self.combustion_pressure * math.pow((2 / (self.heat_capacity_ratio + 1)), (
                    self.heat_capacity_ratio / (self.heat_capacity_ratio - 1)))
        throat_temperature = self.combustion_temperature * (2 / (self.heat_capacity_ratio + 1))
        throat_density = throat_pressure / (self.individual_gas_constant * throat_temperature)
        throat_velocity = math.sqrt(self.heat_capacity_ratio * self.individual_gas_constant * throat_temperature)

        self.throat_pressure = throat_pressure
        self.throat_temperature = throat_temperature
        self.throat_density = throat_density
        self.throat_velocity= throat_velocity
        self.throat_area = self.mass_flow / (throat_velocity * throat_density)
        self.throat_diameter = diameter_from_area(self.throat_area)
        self.exit_area = self.throat_area * self.area_ratio
        self.exit_diameter = diameter_from_area(self.exit_area)

    @abstractmethod
    def calculate_profile(self, cc_diameter, cc_length):
        pass

    def draw(self):
        plt.figure(1)
        plt.plot(self.xs*1e3, self.ys*1e3, linewidth=2.0)
        plt.plot(self.xs*1e3, -self.ys*1e3, linewidth=2.0)
        plt.grid()
        plt.axis('equal')

        plt.figure(2)
        plt.plot(self.axials, self.machs, linewidth=2.0)
        plt.grid()

        plt.figure(3)
        plt.plot(self.axials, self.pressures, linewidth=2.0)
        plt.grid()

        plt.figure(4)
        plt.plot(self.axials, self.temperatures, linewidth=2.0)
        plt.grid()

        plt.figure(5)
        plt.plot(self.axials, self.velocities, linewidth=2.0)
        plt.grid()

        plt.show()


    def get_radius(self, axial_position):
        return self.profile_interpolator(axial_position)

    def calculate_atmospheric_nozzle_properties(self, atmospheric_pressure):
        self.atmospheric_pressure_ratio = atmospheric_pressure/self.combustion_pressure
        self.atmospheric_area_ratio = self.calculate_area_ratio(atmospheric_pressure)

    def set_area_ratio(self, area_ratio):
        self.area__ratio = area_ratio
        self.calculate_exit_area()

    def set_throat_area(self, throat_area):
        self.throat_area = throat_area
        self.throat_diameter = diameter_from_area(self.throat_area)
        self.throat_radius = self.throat_radius/2

    def calculate_exit_area(self):
        self.exit_area = self.throat_area * self.area_ratio
        self.exit_diameter = diameter_from_area(self.exit_area)
        self.exit_radius = self.exit_diameter/2

    def calculate_area_ratio(self, atmospheric_pressure):
        self.pressure_ratio = atmospheric_pressure/self.combustion_pressure
        A = 2 * self.heat_capacity_ratio / (self.heat_capacity_ratio-1)
        B = math.pow(self.pressure_ratio, (2/self.heat_capacity_ratio))
        C = 1 - math.pow(self.pressure_ratio, (self.heat_capacity_ratio-1)/self.heat_capacity_ratio)
        area_ratio = v_function(self.heat_capacity_ratio) / math.sqrt(A*B*C)
        return area_ratio

    def calculate_current_thrust(self, ambient_pressure):
        return self.mass_flow * self.exhaust_velocity + self.exit_area * (self.exit_pressure - ambient_pressure)

    def calculate_isp(self, ambient_pressure):
        self.isp = self.calculate_current_thrust(ambient_pressure)/(self.mass_flow * 9.81)

    def calculate_axial_flow_properties(self):

        # combustion chamber


        step = 0.001
        # nozzle backward
        backward_length = self.throat_x - self.nozzle_start_x
        steps_no_backward = math.ceil(backward_length/step)

        for i in range(steps_no_backward):
            x = self.throat_x - (i)/(steps_no_backward) * backward_length
            y = self.profile_interpolator(x).item()
            area = area_from_diameter(y*2)
            area_ratio = area/self.throat_area

            mach = fsolve(mach_area_ratio, np.array([0.1]), args=(1.0, area_ratio, self.heat_capacity_ratio))
            temperature = temperature_mach(1.0, mach, self.throat_temperature,
                                           self.heat_capacity_ratio)
            pressure = pressure_mach(1.0, mach, self.throat_pressure,
                                     self.heat_capacity_ratio)

            self.backward_x.append(x)
            self.backward_mach.append(mach)
            self.backward_temperature.append(temperature)
            self.backward_pressure.append(pressure)

        self.backward_x.reverse()
        self.backward_mach.reverse()
        self.backward_temperature.reverse()
        self.backward_pressure.reverse()
        # nozzle forward
        forward_length = self.nozzle_end_x - self.throat_x

        steps_no_forward = math.ceil(forward_length / step)

        for j in range(steps_no_forward):
            x = self.throat_x + (j) / (steps_no_forward) * forward_length
            y = self.profile_interpolator(x)
            area = area_from_diameter(y * 2)
            area_ratio = area / self.throat_area

            mach = fsolve(mach_area_ratio, np.array(2), args=(1.0, area_ratio, self.heat_capacity_ratio))
            temperature = temperature_mach(1.0, mach, self.throat_temperature,
                                           self.heat_capacity_ratio)
            pressure = pressure_mach(1.0, mach, self.throat_pressure,
                                     self.heat_capacity_ratio)

            self.forward_x.append(x)
            self.forward_mach.append(mach)
            self.forward_temperature.append(temperature)
            self.forward_pressure.append(pressure)

        self.axials = [0,  self.nozzle_start_x]
        self.axials.extend(self.backward_x)
        self.axials.extend(self.forward_x)

        self.machs = [self.backward_mach[0], self.backward_mach[0]]
        self.machs.extend(self.backward_mach)
        self.machs.extend(self.forward_mach)

        self.temperatures = [self.backward_temperature[0], self.backward_temperature[0]]
        self.temperatures.extend(self.backward_temperature)
        self.temperatures.extend(self.forward_temperature)

        self.pressures = [self.backward_pressure[0], self.backward_pressure[0]]
        self.pressures.extend(self.backward_pressure)
        self.pressures.extend(self.forward_pressure)

        for pos_no in range(len(self.axials)):
            a = sound_speed(self.heat_capacity_ratio, self.molecular_mass, self.temperatures[pos_no])
            self.velocities.append(a*self.machs[pos_no])


def v_function(specific_heat_ratio):
    value = math.sqrt(specific_heat_ratio) * \
            math.pow((2/(specific_heat_ratio+1)), ((specific_heat_ratio+1)/(2*(specific_heat_ratio-1))))
    return value


def ratios(pressure_ratio, area_ratio, kappa):
    A = 2 * kappa / (kappa - 1)
    B = math.pow(pressure_ratio, (2 / kappa))
    C = 1 - math.pow(pressure_ratio, (kappa - 1) / kappa)
    value = area_ratio - v_function(kappa) / math.sqrt(A * B * C)

    return value


def mach_area_ratio(m2, m1, A, gamma):
    B = (gamma - 1)/2
    C = (gamma+1)/(2*(gamma-1))
    value = m1/m2 * math.pow((1+B*m2*m2)/(1+B*m1*m1), C) - A

    return value

def pressure_mach(m1, m2, p1, gamma):
    A = (gamma -1)/2
    B = gamma/(gamma-1)
    C = math.pow((1+A*m2*m2)/(1+A*m1*m1), B)
    return p1/C

def temperature_mach(m1, m2, t1, gamma):
    A = (gamma -1)/2

    return t1 * (1+A*m1*m1)/(1+A*m2*m2)


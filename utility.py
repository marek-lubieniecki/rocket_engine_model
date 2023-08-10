import math
import csv


def area_from_diameter(diameter):
    return diameter * diameter * math.pi / 4


def diameter_from_area(area):
    return math.sqrt(4 * area/math.pi)


def vector_norm(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1] * vector[1])


def gravitational_acceleration(altitude):

    GM = 3.986004419e14
    mean_earth_radius = 6371e3
    distance = mean_earth_radius + altitude

    return GM / (distance * distance)


def sound_speed(kappa, m, t):
    return math.sqrt(kappa * 8.314/m * t)


def gas_density(p, t, m):
    return p/(8.314/m * t)
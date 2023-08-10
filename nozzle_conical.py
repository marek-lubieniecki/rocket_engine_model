import scipy.interpolate as interp

from nozzle import *


class NozzleConical(Nozzle):
    def __init__(self, area_ratio, efficiency, outlet_angle, inlet_angle):
        super().__init__(area_ratio, efficiency)

        self.inlet_angle = inlet_angle
        self.outlet_angle = outlet_angle

        self.inlet_angle_rad = math.radians(inlet_angle)
        self.outlet_angle_rad = math.radians(outlet_angle)

        self.converging_filet_ratio = 0.25
        self.diverging_filet_ratio = 0.5

        self.converging_filet_radius = 0
        self.diverging_filet_radius = 0

    def calculate_profile(self, cc_diameter, cc_length):
        self.converging_filet_radius = cc_diameter * self.converging_filet_ratio
        self.diverging_filet_radius = self.throat_diameter * self.diverging_filet_ratio

        D_c = cc_diameter
        D_t = self.throat_diameter
        r_a = self.converging_filet_radius
        r_u = self.diverging_filet_radius
        beta = self.inlet_angle_rad
        alpha = self.outlet_angle_rad

        # srodek pierwszego okregu
        x0_a = 0;  # koniec
        y0_a = D_c / 2 - r_a

        # punkt przeciecia okregu z prosta
        x_1 = x0_a + r_a * math.sin(beta)
        y_1 = y0_a + r_a * math.cos(beta)

        # rownanie prostej zbieznej
        a_zb = - math.tan(beta)
        b_zb = y_1 - a_zb * x_1

        # wyznaczenie zbieznej dlugosci

        y0_u = D_t / 2 + r_u
        y_2 = y0_u - r_u * math.cos(beta)
        x_2 = (y_2 - b_zb) / a_zb
        x0_u = x_2 + r_u * math.sin(beta)

        # 3 punkt przeciecia okręgu z prostą
        x_3 = x0_u + r_u * math.sin(alpha)
        y_3 = y0_u - r_u * math.cos(alpha)

        # rownanie prostej rozbieznej
        a_rb = math.tan(alpha)
        b_rb = y_3 - a_rb * x_3

        # plaszczyzna wylotowa
        y_4 = self.exit_diameter/2
        x_4 = (y_4 - b_rb)/a_rb

        xs = [-cc_length, 0]
        ys = [D_c/2, D_c/2]

        for i in range(20):
            angle = i/20 * beta
            xs.append(x0_a + r_a * math.sin(angle))
            ys.append(y0_a + r_a * math.cos(angle))

        xs.extend([x_1, x_2])
        ys.extend([y_1, y_2])

        for i in range(30):
            angle = -beta + i/30 * (beta+alpha)
            xs.append(x0_u + r_u * math.sin(angle))
            ys.append(y0_u - r_u * math.cos(angle))

        xs.extend([x_3, x_4])
        ys.extend([y_3, y_4])

        self.xs = cc_length + np.array(xs)
        self.ys = np.array(ys)

        self.throat_x = x0_u + cc_length
        self.nozzle_start_x = cc_length
        self.nozzle_end_x = self.xs[-1]

        self.profile_interpolator = interp.interp1d(self.xs, self.ys)

        # def calculate_nozzle_length(self, cc_diameter):
    #
    #    self.nozzle_converging_length = (self.cc_diameter - self.throat_diameter)/(2 * math.tan(converging_angle))
    #    self.nozzle_diverging_length_conical = (self.exit_diameter - self.throat_diameter)/(2 * math.tan(diverging_angle))
    #    self.nozzle_diverging_length = self.conical_length_fraction * self.nozzle_diverging_length_conical
    #    self.nozzle_total_length = self.nozzle_converging_length + self.nozzle_diverging_length


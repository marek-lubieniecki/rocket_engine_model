class Requirements:
    def __init__(self, total_impulse, thrust, ambient_pressure):
        self.total_impulse = total_impulse
        self.thrust = thrust
        self.thrust_time = 0
        self.ambient_pressure = ambient_pressure

        self.calculate_thrust_time()

    def calculate_thrust_time(self):
        self.thrust_time = self.total_impulse/self.thrust

    def calculate_thrust(self):
        self.thrust = self.total_impulse/self.thrust_time

    def set_total_impulse(self, total_impulse):
        self.total_impulse = total_impulse
        self.calculate_thrust_time()

    def set_thrust(self, thrust):
        self.thrust = thrust
        self.calculate_thrust_time()

    def set_thrust_time(self, time):
        self.thrust_time = time
        self.calculate_thrust()
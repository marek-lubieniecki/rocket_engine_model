class PropulsionSystem:
    def __init__(self, requirements, engine, oxidiser_tank, fuel_tank, pressurising_tank):
        self.requirements = requirements
        self.engine = engine
        self.oxidiser_tank = oxidiser_tank
        self.fuel_tank = fuel_tank
        self.pressurising_tank = pressurising_tank

        self.propellant_mass = 0
        self.oxidiser_mass = 0
        self.fuel_mass = 0

        self.total_mass = 0

    def calculate_engine(self):
        self.engine.calculate(self.requirements.thrust, self.requirements.ambient_pressure)


    def calculate_propellant_mass(self):
        self.propellant_mass = self.engine.mass_flow * self.requirements.thrust_time
        self.fuel_mass = self.propellant_mass/(self.engine.oxidiser_fuel_ratio+1)
        self.oxidiser_mass = self.propellant_mass - self.fuel_mass

    def calculate_tank_mass(self):
        self.oxidiser_tank.propellant_mass = self.oxidiser_mass
        self.fuel_tank.propellant_mass = self.fuel_mass

        self.oxidiser_tank.update_mass_and_volume()
        self.fuel_tank.update_mass_and_volume()

    def calculate_pressurising_system_mass(self):
        pass

    def calculate_total_mass(self):
        pass

    def print_info(self):
        print("Propellant mass: ", self.propellant_mass, "Oxidiser mass: ", self.oxidiser_mass, "Fuel mass: ", self.fuel_mass)
        self.engine.print_info()
        #.oxidiser_tank.print_info()
        #self.fuel_tank.print_info()
        #self.engine.draw_engine_contour()
from CoolProp.CoolProp import PropsSI


cantera_coolprop_dict = {
    "O2": "Oxygen",
    "N2O": "NitrousOxide",
    "C1H4": "Methane",
    "C3H8": "Propane",
    "N2": "Nitrogen",
    "C2H5OH": "Ethanol"
}


species_molecular_mass_dict = {
    "O2": 0.032,
    "C3H8": 0.0441,
    "N2": 0.028,
    "N2O": 0.044,
    "C2H5OH": 0.04608
}


class Propellant:

    def __init__(self, name, pressure, temperature):
        self.name = name
        self.coolprop_name = cantera_coolprop_dict[self.name]
        self.pressure = pressure

        if temperature == 'cryogenic':
            self.temperature = PropsSI("T", "P", 1e5, "Q", 0, self.coolprop_name)
            self.density = PropsSI("D", "P", self.pressure, "T", self.temperature, self.coolprop_name)

        elif temperature == 'self_pressurised':
            self.temperature = PropsSI("T", "P", self.pressure, "Q", 0, self.coolprop_name)
            self.density = PropsSI("D", "T", self.temperature, "Q", 0, self.coolprop_name)
        else:
            self.temperature = temperature
            self.density = PropsSI("D", "P", self.pressure, "T", self.temperature, self.coolprop_name)

        self.molecular_mass = species_molecular_mass_dict[self.name]
        self.gas_constant = 8.314 / self.molecular_mass

    def print_info(self):
        print(self.coolprop_name)
        print(self.pressure)
        print(self.temperature)
        print(self.density)


class Gas(Propellant):

    def __init__(self, name, pressure, temperature, heat_capacity_ratio):
        super().__init__(name, pressure, temperature)
        self.heat_capacity_ratio = heat_capacity_ratio



class Material:

    def __init__(self, name, density, tensile_strength):
        self.name = name
        self.density = density
        self.tensile_strength = tensile_strength








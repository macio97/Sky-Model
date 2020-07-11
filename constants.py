# Libraries
from math import pi
import numpy as np
from properties import look


# Constants
h = 6.62607004e-34                                  # Planck's constant
c = 299792458                                       # speed of light (m/s)
T = 5778                                            # sun's Temperature (k)
k = 1.38064852e-23                                  # Boltzmann constant
n = 1.0002926                                       # IOR of air
N = 2.504e25                                        # number density of air (molecules/m^3)
Do = 2.687e20                                       # Dobson unit (molecules/m^2)
rayleigh_scale = 8000                               # Rayleigh scale height (m)
mie_scale = 1200                                    # Mie scale height (m)
mie_G = 0.76                                        # aerosols anisotropy
sqr_G = mie_G * mie_G                               # quared mie_G
ozone_max = 300 * Do / 15e3                         # maximum number density of ozone molecules (m^-3)
earth_sun = 149.6e9                                 # average distance Earth-Sun (m)
sun_radius = 695500e3                               # radius of Sun (m)
earth_radius = 6360e3                               # radius of Earth (m)
atmosphere_radius = 6420e3                          # radius of atmosphere (m)
max_luminous_efficacy = 683                         # maximum luminous efficacy

# wavelengths
num_wavelengths = 21                                # number of wavelengths
min_wavelength = 380
max_wavelength = 780
wavelengths_step = (max_wavelength - min_wavelength) / (num_wavelengths - 1)
lam = np.arange(min_wavelength, max_wavelength + 1, wavelengths_step) * 10**-9

# illuminants
illuminant_D65 = np.array([[3.2404542, -1.5371385, -0.4985314],
                           [-0.9692660, 1.8760108, 0.0415560],
                           [0.0556434, -0.2040259, 1.0572252]])
illuminant_E = np.array([[2.3706743, -0.9000405, -0.4706338],
                         [-0.5138850, 1.4253036, 0.0885814],
                         [0.0052982, -0.0146949, 1.0093968]])

# CIE color matching functions from 380 to 780nm in 20nm intervals
cmf = np.loadtxt('data/cie_xyz.csv', usecols=(1,2,3))
# blackbody radiation
sun = (2 * pi * h * c * c) / (lam**5 * (np.exp((h * c) / (k * T * lam)) - 1)) * 10**-9
# irradiance on top of atmosphere (W/m^2)
irradiance = sun * ((sun_radius * sun_radius) / (earth_sun * earth_sun))
# Rayleigh scattering coefficient (m^-1)
rayleigh_coeff = ((8 * pi**3) * (n * n - 1)**2) / (3 * N * lam**4)
# Mie scattering coefficient (m^-1)
mie_coeff = 2e-5
# Ozone cross section (cm^2/molecule)
ozone_cross = np.loadtxt('data/ozone_cross_section.csv', usecols=(1))
# Ozone absorption coefficient (m^-1)
ozone_coeff = ozone_cross * 10**-4 * ozone_max

def read_filmic_look(path):
	nums = []
	with open(path) as filmic_file:
		for line in filmic_file:
			nums.append(float(line))
	return nums

# filmic contrast
filmic_look = read_filmic_look("looks/" + look + ".txt")
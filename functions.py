# Libraries
import numpy as np
from constants import atmosphere_radius, cmf, earth_radius, filmic_look, illuminant_D65, mie_G, mie_scale, rayleigh_scale, sqr_G, wavelengths_step
from math import cos, exp, pi, sin, sqrt

# Functions


def density_rayleigh(height):
    return exp(-height / rayleigh_scale)


def density_mie(height):
    return exp(-height / mie_scale)


def density_ozone(height):
    if height < 10e3 or height >= 40e3:
        return 0
    elif height >= 10e3 and height < 25e3:
        return 1 / 15e3 * height - 2 / 3
    else:
        return -(1 / 15e3 * height - 8 / 3)


def phase_rayleigh(mu):
    return 3 / (16 * pi) * (1 + mu * mu)


def phase_mie(mu):
    return (3 * (1 - sqr_G) * (1 + mu * mu)) / (8 * pi * (2 + sqr_G) * ((1 + sqr_G - 2 * mie_G * mu)**1.5))


def geographical_to_direction(lat, lon):
    return np.array([cos(lat) * cos(lon), cos(lat) * sin(lon), sin(lat)])


def atmosphere_intersection(pos, dir):
    b = -2 * np.dot(dir, -pos)
    c = np.sum(pos * pos) - atmosphere_radius * atmosphere_radius
    t = (-b + sqrt(b * b - 4 * c)) / 2
    return pos + dir * t


def surface_intersection(pos, dir):
    if dir[2] >= 0:
        return False
    b = -2 * np.dot(dir, -pos)
    c = np.sum(pos * pos) - earth_radius * earth_radius
    t = b * b - 4 * c
    if t >= 0:
        return True
    else:
        return False


def spec_to_xyz(spectrum):
    # integral
    sum = np.sum(spectrum[:, np.newaxis] * cmf, axis=0)
    return sum * wavelengths_step


def xyz_to_rgb(xyz, exposure):
    # XYZ to sRGB linear
    sRGB_linear = np.dot(illuminant_D65, xyz)

    # apply exposure
    sRGB_exp = sRGB_linear * 2**exposure

    # avoid negative values
    sRGB_1 = np.maximum(1e-5, sRGB_exp)

    # apply filmic log encoding
    sRGB_log = (np.log2(sRGB_1 / 0.18) + 10) / 16.5

    # clamp sRGB between 0 and 1
    sRGB_2 = np.clip(sRGB_log, 1e-5, 1)

    # apply look contrast
    index = np.array(sRGB_2 * 4095, np.int)

    return np.array([filmic_look[i] for i in index])

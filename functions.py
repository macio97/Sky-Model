# Libraries
import numpy as np
from constants import atmosphere_radius, cmf, earth_radius, filmic_look, illuminant_D65, max_luminous_efficacy, mie_G, mie_scale, rayleigh_scale, sqr_G, wavelengths_step
from math import cos, exp, pi, sin, sqrt, pow


# Functions
def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max

def density_rayleigh(height):
    return exp(-height / rayleigh_scale)

def density_mie(height):
    return exp(-height / mie_scale)

def density_ozone(height):
    if height < 10000 or height >= 40000:
        return 0
    elif height >= 10000 and height < 25000:
        return 1 / 15000 * height - 2 / 3
    else:
        return -(1 / 15000 * height - 8 / 3)

def phase_rayleigh(mu):
    return 3 / (16 * pi) * (1 + mu * mu)

def phase_mie(mu):
    return (3 * (1 - sqr_G) * (1 + mu * mu)) / (8 * pi * (2 + sqr_G) * pow((1 + sqr_G - 2 * mie_G * mu), 1.5))

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
    t = np.dot(dir, -pos) / np.sum(dir * dir)
    D = pos[0] * pos[0] - 2 * -pos[0] * dir[0] * t + pow(dir[0] * t, 2) + pos[1] * pos[1] - 2 * (-pos[1]) * dir[1] * t + pow(dir[1] * t, 2) + pos[2] * pos[2] - 2 * (-pos[2]) * dir[2] * t + pow(dir[2] * t, 2)
    if D <= (earth_radius * earth_radius):
        return True
    else:
        return False

def spec_to_xyz(spectrum):
    # xyz tristimulus values
    return (np.sum(spectrum[:, np.newaxis] * cmf, axis=0)) * wavelengths_step * max_luminous_efficacy

def xyz_to_rgb(xyz, exposure):
    # XYZ to sRGB linear
    # the multiply by 120000 is a hack to get a brighter image
    sRGB_linear = np.dot(illuminant_D65, xyz) * 120000

    # apply exposure
    sRGB_exp = sRGB_linear * pow(2, exposure)

    # avoid infinite values
    sRGB_1 = np.where(sRGB_exp <= 0, 1e-5, sRGB_exp)

    # apply filmic log encoding
    sRGB_log = (np.log2(sRGB_1 / 0.18) + 10) / 16.5

    # avoid negative values
    sRGB_2 = np.where(sRGB_log <= 0, 1e-5, sRGB_log)

    # apply look contrast
    index = np.array(sRGB_2 * 4095, np.int)
    
    return np.array([filmic_look[i] for i in index])
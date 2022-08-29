import colorsys
import numpy as np

def spectrum(n : int):
    hsv = [(h, 1, 1) for h in np.linspace(0, 240/360, n)]
    rgb = np.array([(*colorsys.hsv_to_rgb(*tup), 1) for tup in hsv])
    return rgb
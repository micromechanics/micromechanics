"""
Tip Area Models
===============

This example compares projected contact area for a perfect Berkovich tip, an
ISO-style calibrated area function, and a spherical tip.
"""

import matplotlib.pyplot as plt
import numpy as np

from micromechanics.indentation import Tip

contact_depth = np.linspace(0.01, 0.8, 120)
perfect = Tip("perfect")
iso = Tip(shape=[24.5, 420.0, -30.0])
sphere = Tip(shape=[3.0, 70.3, "sphere"])

area_perfect = perfect.areaFunction(contact_depth.copy())
area_iso = iso.areaFunction(contact_depth.copy())
area_sphere = sphere.areaFunction(contact_depth.copy())

fig, ax = plt.subplots()
ax.plot(contact_depth, area_perfect, label="perfect Berkovich")
ax.plot(contact_depth, area_iso, label="ISO area function")
ax.plot(contact_depth, area_sphere, label="spherical cap")
ax.set_xlabel(r"contact depth [$\mathrm{\mu m}$]")
ax.set_ylabel(r"projected contact area [$\mathrm{\mu m^2}$]")
ax.legend()

###############################################################################
# The inverse area function maps a measured contact area back to contact depth.

known_area = perfect.areaFunction(np.array([0.35]))[0]
recovered_depth = perfect.areaFunctionInverse(known_area)
print(f"Recovered depth for the perfect tip: {recovered_depth:.3f} um")

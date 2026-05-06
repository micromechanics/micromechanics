"""
Interpolated Tip Area Function
==============================

This example uses a tabulated contact-depth/contact-area calibration curve as
an interpolated tip area function and compares it with analytical references.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from micromechanics.indentation import Tip

###############################################################################
# Some calibrations are available as measured points rather than polynomial
# prefactors. Here we create such a table by perturbing the perfect Berkovich
# area with a shallow-depth rounding term.

calibration_depth = np.linspace(0.02, 0.8, 18)
perfect_reference = Tip("perfect")
measured_area = perfect_reference.areaFunction(calibration_depth.copy())
measured_area *= 1.0 + 0.18*np.exp(-calibration_depth/0.16)

###############################################################################
# ``Tip`` accepts an interpolation function for ``Ac = f(hc)``. The interpolation
# can then be used anywhere a regular tip area function is expected.

interpolated_area = interp1d(calibration_depth, measured_area, fill_value="extrapolate")
interpolated_tip = Tip(interpFunction=interpolated_area)
spherical_tip = Tip(shape=[3.0, 70.3, "sphere"])

###############################################################################
# Compare the interpolated calibration with the perfect Berkovich and spherical
# references. Differences at shallow depth are especially important because
# small contact-depth errors strongly affect hardness.

contact_depth = np.linspace(0.02, 0.8, 120)
area_interpolated = interpolated_tip.areaFunction(contact_depth.copy())
area_perfect = perfect_reference.areaFunction(contact_depth.copy())
area_sphere = spherical_tip.areaFunction(contact_depth.copy())

fig, ax = plt.subplots()
ax.plot(calibration_depth, measured_area, "o", label="calibration points")
ax.plot(contact_depth, area_interpolated, label="interpolated tip")
ax.plot(contact_depth, area_perfect, "--", label="perfect Berkovich")
ax.plot(contact_depth, area_sphere, ":", label="spherical tip")
ax.set_xlabel(r"contact depth [$\mathrm{\mu m}$]")
ax.set_ylabel(r"projected contact area [$\mathrm{\mu m^2}$]")
ax.legend()

###############################################################################
# The representation confirms that this tip is driven by an interpolation
# function instead of polynomial prefactors.

print(interpolated_tip)

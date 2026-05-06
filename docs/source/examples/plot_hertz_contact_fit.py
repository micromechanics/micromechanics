"""
Hertz Contact Fit
=================

This example creates an ideal elastic loading segment for a spherical
indenter, adds a small displacement offset, and fits the first part of the
curve with the Hertz contact equation.
"""

import matplotlib.pyplot as plt
import numpy as np

from micromechanics.indentation import Indentation
from micromechanics.indentation.hertz import hertzEquation

indentation = Indentation("")
indentation.output["verbose"] = 2

true_h0 = 0.018
true_reduced_modulus = 9500.0
depth = np.linspace(0.0, 0.18, 80)
force = hertzEquation(depth.copy(), true_h0, true_reduced_modulus)

indentation.h = depth.copy()
indentation.p = force.copy()

fit_h0, fit_reduced_modulus = indentation.hertzFit(forceRange=(0.02, 6.0), correctH=False, plot=False)

fit_depth = np.linspace(depth.min(), depth.max(), 200)
fit_force = hertzEquation(fit_depth.copy(), fit_h0, fit_reduced_modulus)

fig, ax = plt.subplots()
ax.plot(depth, force, "o", label="synthetic loading segment")
ax.plot(fit_depth, fit_force, "-", label="Hertz fit")
ax.axvline(fit_h0, color="k", linestyle="dashed", label="fitted contact")
ax.set_xlabel(r"depth [$\mathrm{\mu m}$]")
ax.set_ylabel(r"force [$\mathrm{mN}$]")
ax.legend()

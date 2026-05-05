"""
Micromechanics installation
===========================

This example runs the quick check from the installation instructions using the
default indentation data bundled with micromechanics.
"""

from micromechanics.indentation import Indentation

indentation = Indentation()
indentation.plotAll()

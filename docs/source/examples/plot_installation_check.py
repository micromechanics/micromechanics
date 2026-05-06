"""
Micromechanics installation
===========================

This example runs the quick check from the installation instructions using the
default indentation data bundled with micromechanics.
"""

from micromechanics.indentation import Indentation

###############################################################################
# Calling ``Indentation()`` without a file name loads the small example data set
# bundled with the package. This is the quickest check that imports, data files,
# and plotting are all available in the current environment.

indentation = Indentation()
indentation.plotAll()

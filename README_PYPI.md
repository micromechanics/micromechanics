[![Linting](https://github.com/micromechanics/micromechanics/actions/workflows/pylint.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/pylint.yml)
[![Documentation](https://github.com/micromechanics/micromechanics/actions/workflows/docs.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/docs.yml)
[![pypi.org](https://github.com/micromechanics/micromechanics/actions/workflows/pypi.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/pypi.yml)

# Micromechanics library for experimental micromechanics

This library allows to read datafiles from different nanoindenters and allows to analyse it by evaluating the hardness and Young's modulus using the Oliver-Pharr method. It also includes functions for frame stiffness and area function calibration as well as a number of plotting functions. Additionally the library allows to read SEM images and optimize them

The library can read:
- xls files from the vendors MTS, Agilent, Keysight, which produced the XP and G200 indenters
- hap files from the Fischer-Scope
- zip-files which include all the files of the Micromaterials NanoXtreme
- some common format which is based on the NeXus common data format
- Tif images from Zeiss and FEI/ThermoFischer


Install by
``` bash
pip install micromechanics
```

Run test using the default data
``` python
from micromechanics.indentation import Indentation
i = Indentation()
i.plotAll()
```

Alternatively, for Tif images
``` python
from micromechanics.tif import Tif
```

More information as well as tutorials can be found at: [Read the docs](https://micromechanics.github.io/micromechanics/)

If you want to contribute to the development, we develop at [github](https://github.com/micromechanics/micromechanics)


# Contributors
- Steffen Brinckmann
- Velislava Yonkova
- Ruomeng (Nicole) Chen

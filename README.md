[![Linting](https://github.com/micromechanics/micromechanics/actions/workflows/pylint.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/pylint.yml)
[![Documentation](https://github.com/micromechanics/micromechanics/actions/workflows/docs.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/docs.yml)
[![pypi.org](https://github.com/micromechanics/micromechanics/actions/workflows/pypi.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/pypi.yml)
[![Tests](https://github.com/micromechanics/micromechanics/actions/workflows/tests.yml/badge.svg)](https://github.com/micromechanics/micromechanics/actions/workflows/tests.yml)

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


# Information for developers
Test the code: linting, documentation and then the tests from project main directory
``` bash
pylint micromechanics
make -C docs html
python tests/testVerification.py
python tests/testAllFiles.py
python tests/testAgilent_xls.py
python tests/testMicromaterials_hdf5.py
python tests/testFischerScope_hdf5.py
```
These tests are also executed as github action once pushed.

or the short form to run all the tests
``` bash
python -m unittest tests/test*
```

#TODO_P3 turn all tests into one github action

Then upload/create-pull-request to github, via
``` bash
./commit.py 'my message'
```

## How to find bugs that occurred in a past commit
Steps:
- Git history in nice ASCII  => save in file in distant folder; along with notes
- go to point in history (do not change the present)
- find diff: always old^ new
- run your tests
- undo your changes since checkout
- go back to present

``` bash
git log --oneline --graph
git checkout bf0b634
git diff e7eac50^ fed7119  #(old^ new)
# test
git reset --hard
git checkout main
```

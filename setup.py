#!/usr/bin/env python
from setuptools import setup
import commit

if __name__ == '__main__':
    setup(name='micromechanics',
          version=commit.get_version()[1:]
    )

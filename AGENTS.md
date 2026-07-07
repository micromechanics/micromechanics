# Repository Guidelines

## Project Structure & Module Organization

This is a Python package for nanoindentation and SEM image analysis. Core package code lives in `micromechanics/`. The `micromechanics/indentation/` package contains indentation file readers, calibration, plotting, and analysis routines; `micromechanics/tif/` handles TIF image support and includes bundled font assets. Tests are in `tests/` and use example instrument data from `examples/`. Documentation sources are in `docs/source/`, with images in `docs/source/img/`.

## Documentation Expectations

`README.md` is a concise project entry point for purpose, installation, basic use, development commands, and issue tracking. It is deliberately not the full user manual; detailed user documentation and tutorials live  on Read the Docs.

## Build, Test, and Development Commands

Create a development environment from the repository root:

```bash
python -m pip install -r requirements-devel.txt
python -m pip install -e .
```

Run the CI-style test suite:

```bash
python -m unittest tests/test*
```
Pay attention that no '**ERROR**' is in the output.

Run individual regression tests while iterating, for example:

```bash
python tests/testAgilent_xls.py
python tests/testVerification.py
```

Lint package modules with the same tool used by CI:

```bash
pylint $(git ls-files 'micromechanics/*/*.py')
```

Run static type checks:

```bash
python -m mypy micromechanics
```

Build the Sphinx documentation:

```bash
make -C docs html
```

## Coding Style & Naming Conventions

Follow the existing Python style in the package. The project uses Pylint configuration from `.pylintrc`, including two-space indentation (`indent-string='  '`) and a 200-character maximum line length. Use descriptive module, function, and variable names that match nearby code. Keep public APIs stable where possible, since tests and examples exercise vendor-specific file formats.

## Testing Guidelines

Tests use Python `unittest`; development dependencies also include `pytest` and coverage tools. Name new tests `tests/test*.py` so they are picked up by `python -m unittest tests/test*`. Prefer focused regression tests using the smallest relevant file from `examples/`. When changing parsers or calibration behavior, run both the related vendor test and `tests/testAllFiles.py`.

To measure coverage, include both the test suite and executable examples:

```bash
python -m coverage erase
MPLBACKEND=Agg python -m coverage run -m unittest tests/test*
for f in docs/source/examples/plot_*.py; do MPLBACKEND=Agg python -m coverage run --append "$f"; done
```

Use `MPLBACKEND=Agg` for example coverage runs so matplotlib examples render without opening interactive windows that must be closed manually. Inspect coverage with:

```bash
python -m coverage report -m
python -m coverage html
```

DO NOT run tests, convergence, unless explicitly tasked by the user.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries such as `Add information and output of relative standard error` or `Simplify indentation plotting`. Keep commit messages specific to the behavior changed. For releases, `./commit.py 'message' [level]` regenerates `requirements.txt`, commits, tags, and pushes; use it only when intentionally creating a version tag.

Pull requests should describe the changed behavior, list tests run, and mention affected instrument formats or documentation pages. Include screenshots only for plotting or documentation visual changes.

## Agent-Specific Instructions

Do not modify files in `examples/` unless the change is required for a parser or regression fixture. Treat binary example data and generated documentation output as inputs, not routine edit targets.
For `micromechanics/indentation/*` mixin methods, prefer local `# type: ignore[misc]` on methods whose `self` type is intentionally broader than the mixin class. Do not introduce parallel `_State` or protocol classes just to satisfy mypy; rely on tests to catch mismatches between `Indentation` and its mixins.

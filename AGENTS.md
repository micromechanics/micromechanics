# Repository Guidelines

## Project Structure & Module Organization

This is a Python package for nanoindentation and SEM image analysis. Core package code lives in `micromechanics/`. The `micromechanics/indentation/` package contains indentation file readers, calibration, plotting, and analysis routines; `micromechanics/tif/` handles TIF image support and includes bundled font assets. Tests are in `tests/` and use example instrument data from `examples/`. Documentation sources are in `docs/source/`, with images in `docs/source/img/`.

## Documentation Expectations

`README.md` is a concise project entry point for purpose, installation, basic use, development commands, and issue tracking. It is deliberately not the full user manual; detailed user documentation and tutorials live on Read the Docs.

## Build, Test, and Development Commands

```bash
python -m pip install -r requirements-devel.txt
python -m pip install -e .
python -m unittest tests/test*
python tests/testAgilent_xls.py
python tests/testVerification.py
pylint $(git ls-files 'micromechanics/*/*.py')
python -m mypy micromechanics
make -C docs html
```

Pay attention that no '**ERROR**' is in test output.

## Coding Style

The project uses Pylint configuration from `.pylintrc`, including two-space indentation (`indent-string='  '`) and a 200-character maximum line length.

## Testing Guidelines

Tests use Python `unittest`; development dependencies also include `pytest` and coverage tools. Name tests `tests/test*.py`. When changing parsers or calibration behavior, run both the related vendor test and `tests/testAllFiles.py`.

For coverage, use `MPLBACKEND=Agg` so matplotlib examples do not open interactive windows. Inspect coverage with `python -m coverage report -m` or `python -m coverage html`.

## Commit & Pull Request Guidelines

Use short, imperative commit summaries. For releases, `./commit.py 'message' [level]` regenerates `requirements.txt`, commits, tags, and pushes; use it only when intentionally creating a version tag.

Pull requests should describe changed behavior, tests run, and affected instrument formats or documentation pages. Include screenshots only for plotting or documentation visual changes.

## Agent-Specific Instructions

For `micromechanics/indentation/*` mixin methods, prefer local `# type: ignore[misc]` on methods whose `self` type is intentionally broader than the mixin class. Do not introduce parallel `_State` or protocol classes just to satisfy mypy; rely on tests to catch mismatches between `Indentation` and its mixins.

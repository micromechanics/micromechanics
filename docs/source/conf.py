# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import ast
import os, sys, datetime
import re
from pathlib import Path

repositoryRoot = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repositoryRoot))
sys.path.insert(0, str(repositoryRoot / 'micromechanics' / 'tif'))

# -- Project information -----------------------------------------------------

project = 'micromechanics'
copyright = u'2022-{}, PASTA-ELN team'.format(datetime.datetime.now().year)
author = u'Micromechanics team'

# The full version, including alpha/beta/rc tags
version = "1.3.3"
release = version

# -- General configuration ---------------------------------------------------
# The master toctree document.
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.napoleon', 'sphinx_gallery.gen_gallery']

sphinx_gallery_conf = {
  'examples_dirs': 'examples',
  'gallery_dirs': 'auto_examples',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# define a hard line break for HTML
rst_prolog = """
.. |br| raw:: html

   <br />
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['img']
html_css_files = ['custom.css']

def _definition_source() -> str:
    definitionFile = Path(__file__).resolve().parents[2] / 'micromechanics' / 'indentation' / 'definitions.py'
    return definitionFile.read_text(encoding='utf-8')


def _extract_dict_block(source: str, name: str) -> str:
    assignment = re.search(r'^'+re.escape(name)+r'\s*:[^=]+=\s*{', source, re.MULTILINE)
    if assignment is None:
        raise ValueError('Could not find dictionary '+name+' in definitions.py')
    start = source.find('{', assignment.start())
    depth = 0
    inString = ''
    escaped = False
    for idx, character in enumerate(source[start:], start=start):
        if escaped:
            escaped = False
            continue
        if character == '\\':
            escaped = True
            continue
        if inString:
            if character == inString:
                inString = ''
            continue
        if character in ('"', "'"):
            inString = character
            continue
        if character == '{':
            depth += 1
        elif character == '}':
            depth -= 1
            if depth == 0:
                return source[start:idx+1]
    raise ValueError('Could not find end of dictionary '+name+' in definitions.py')


def _flat_dict_rows(block: str) -> list[tuple[str, str, str]]:
    rows = []
    lastRow = -1
    for line in block.splitlines()[1:-1]:
        entry = re.match(r"\s*'([^']+)'\s*:\s*(.+?)\s*,?\s*(?:#\s*(.*))?$", line)
        if entry:
            key, value, description = entry.groups()
            rows.append((key, value.strip(), '' if description is None else description.strip()))
            lastRow = len(rows)-1
            continue
        continuation = re.match(r'\s*#\s*(.*)$', line)
        if continuation and lastRow >= 0:
            key, value, description = rows[lastRow]
            rows[lastRow] = (key, value, (description+' '+continuation.group(1).strip()).strip())
    return rows


def _vendor_dict_rows(block: str) -> tuple[list[str], list[list[str]]]:
    vendorRows = []
    columns = []
    for line in block.splitlines()[1:-1]:
        entry = re.match(r'\s*Vendor\.([A-Za-z0-9_]+)\s*:\s*(\{.*\})\s*,?\s*(?:#\s*(.*))?$', line)
        if entry is None:
            continue
        vendor, valuesSource, description = entry.groups()
        values = ast.literal_eval(valuesSource)
        for key in values:
            if key not in columns:
                columns.append(key)
        vendorRows.append((vendor, values, '' if description is None else description.strip()))
    headers = ['Vendor'] + columns + ['Description']
    rows = [[vendor] + [str(values.get(column, '')) for column in columns] + [description] for vendor, values, description in vendorRows]
    return headers, rows


def _rst_table(headers: list[str], rows: list[list[str]], widths: str = '') -> list[str]:
    table = ['.. list-table::', '   :header-rows: 1']
    if widths:
        table.append('   :widths: '+widths)
    table += ['', '   * - '+'\n     - '.join(headers)]
    for row in rows:
        table.append('   * - '+'\n     - '.join(row))
    table.append('')
    return table


def _defaults_section(title: str, rows: list[tuple[str, str, str]]) -> list[str]:
    return [title, '-'*len(title), ''] + _rst_table(['Key', 'Default', 'Description'], [list(row) for row in rows], '25 25 50')


def generate_indentation_default_tables(app) -> None:
    source = _definition_source()
    generatedDir = Path(app.srcdir) / 'generated'
    generatedDir.mkdir(exist_ok=True)
    outputFile = generatedDir / 'indentation_defaults.rst'

    modelRows = _flat_dict_rows(_extract_dict_block(source, '_DefaultModel'))
    outputRows = _flat_dict_rows(_extract_dict_block(source, '_DefaultOutput'))
    surfaceRows = _flat_dict_rows(_extract_dict_block(source, '_DefaultSurface'))
    vendorHeaders, vendorRows = _vendor_dict_rows(_extract_dict_block(source, '_DefaultVendorDependent'))

    lines = [
        '.. This file is generated from micromechanics/indentation/definitions.py by docs/source/conf.py.',
        '.. Do not edit it manually.',
        '',
    ]
    lines += _defaults_section('Default Model', modelRows)
    lines += ['Vendor Dependent Defaults', '--------------------------', '']
    lines += _rst_table(vendorHeaders, vendorRows)
    lines += _defaults_section('Default Output', outputRows)
    lines += _defaults_section('Default Surface', surfaceRows)
    outputFile.write_text('\n'.join(lines), encoding='utf-8')


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip

def setup(app):
    generate_indentation_default_tables(app)
    app.connect("autodoc-skip-member", skip)

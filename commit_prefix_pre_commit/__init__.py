# numpydoc ignore=GL08

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("conventional-pre-commit")
except PackageNotFoundError:
    # package is not installed
    pass

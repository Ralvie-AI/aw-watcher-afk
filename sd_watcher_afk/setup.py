from pathlib import Path
import os

from setuptools import setup, Extension
from Cython.Build import cythonize

BASE = Path(__file__).resolve().parent
os.chdir(BASE)

extensions = [
    Extension("windows", ["windows.py"]),
    Extension("config", ["config.py"]),
    Extension("afk", ["afk.py"]),   
]


setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",           
        },
        
    )
)
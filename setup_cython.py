from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "cy_recommender.recommender",
        ["cy_recommender/recommender.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="cy_recommender",
    ext_modules=cythonize(extensions, language_level=3),
)

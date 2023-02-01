"""Setup script for AtomicEmbeddings."""
from setuptools import find_packages, setup

VERSION = "0.1"
DESCRIPTION = "Atomic Embeddings"
LONG_DESCRIPTION = """A package for visualising
 and analysing atomic embedding vectors."""

# Setting up
setup(
    name="AtomicEmbeddings",
    version=VERSION,
    author="Anthony O. Onwuli",
    author_email="anthony.onwuli16@imperial.ac.uk",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={"AtomicEmbeddings": ["data/*.json", "data/*.csv"]},
    test_suite="AtomicEmbeddings.tests.test",
    install_requires=[
        "numpy",
        "scipy",
        "pymatgen",
        "seaborn",
        "matplotlib",
        "scikit-learn",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
)

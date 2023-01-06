[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub issues](https://img.shields.io/github/issues-raw/WMD-Group/Atomic_Embeddings)](https://github.com/WMD-group/Atomic_Embeddings/issues)
[![CI Status](https://github.com/WMD-group/Atomic_Embeddings/actions/workflows/ci.yml/badge.svg)](https://github.com/WMD-group/Atomic_Embeddings/actions/workflows/ci.yml)


Atomic_Embeddings
====

The **Atomic Embeddings** package provides high-level tools for analysing elemental 
embeddings data. This primarily involves visualising the correlation between 
embedding schemes using different statistical measures.

Motivation
--------

Machine learning approaches for materials informatics have become increasingly 
widespread. Some of these involve the use of deep learning 
techniques where the representation of the elements is learned 
rather than specified by the user of the model. While an important goal of 
machine learning training is to minimise the chosen error function to make more 
accurate predictions, it is also important for us material scientists to be able 
to interpret these models. As such, we aim to evaluate and compare different atomic embedding
schemes in a consistent framework. 

Getting started
--------
Atomic_Embeddings's main feature, the Embedding class is accessible by 
importing the class.

Installation
--------
The package can be installed by cloning the repository:

```
git clone https://github.com/WMD-group/Atomic_Embeddings.git
cd Atomic_Embeddings
pip install .
```
Usage
--------
For simple usage, you can instantiate an Embedding object using one of the embeddings in the data directory. For this example, let's use the magpie elemental representation.

```python
# Import the class
>>> from AtomicEmbeddings.core import Embedding

# Load the magpie data
>>> magpie = Embedding.load_data('magpie')
```

We can access some of the properties of the `Embedding` class. For example, we can find the dimensions of the elemental representation and the list of elements for which an embedding exists.
```python
# Print out some of the properties of the Atomic_Embeddings class
>>> print(f'The magpie representation has embeddings of dimension {magpie.dim}') 
>>> print(magpie.element_list) # prints out all the elements considered for this representation
The magpie representation has embeddings of dimension 21
['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk']
```

TO-DO
--------

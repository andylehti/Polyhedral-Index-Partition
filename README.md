[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/andylehti/Polyhedral-Index-Partition/blob/main/Polyhedral_Index_Partition.ipynb)

# The Polyhedral Index Partition (PIP) and the Discovery of Pascal's Dimensions: Enabling Computational Retrieval and Reversibility in High-Index Partition Arrays


Listen to the paper: [here](https://youtu.be/iScC_nTA0EI)

---

Author: **Andrew Lehti**

Disciplines: Cognitive Psychology, Linguistics, Mathematics, and their Histories

DOI: [10.6084/m9.figshare.27642783](https://doi.org/10.6084/m9.figshare.27642783)

## Abstract

The Polyhedral Index Partition (PIP) framework introduces an innovative approach to calculating integer partitions by leveraging the mathematical structures of Pascal's Triangle, specifically through the concepts of Pascal's Dimensions and Pascal's Laterals. This repository contains the Python implementation of PIP, which offers significant performance improvements over traditional partition enumeration methods.

---

## Getting Started

### Prerequisites

- Python 3.8 or later
- `mpmath` library for arbitrary-precision arithmetic

Install `mpmath` using:

```bash
pip install mpmath
```

### Cloning the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/andylehti/Polyhedral-Index-Partition.git
```

---

## Usage

Run the Python script to compute partitions and their indices:

### Example: Partition Calculation

```python
n = 55234587678685685685663467263573
p = 7
a = partition(n, p)
print("Partition:", a)
```

### Example: Reverse Mapping

```python
r = getInverse(*a)
print("Index:", r)
```

For more examples, see the [notebook](https://colab.research.google.com/github/andylehti/Polyhedral-Index-Partition/blob/main/Polyhedral_Index_Partition.ipynb).

---

## References

1. **Pascal, B.** (1654). *Traité du triangle arithmétique*.
2. **Stanley, R. P.** (1999). *Enumerative Combinatorics*.
3. **Sloane, N. J. A.** (2003). *The On-Line Encyclopedia of Integer Sequences*.

---

**Polyhedral Index Partition © Andrew Lehti, 2024**

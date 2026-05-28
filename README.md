# 🧬 synth-dynamics: Coarse-Grained Protein Dynamics

[![PyPI version](https://img.shields.io/pypi/v/synth-dynamics.svg)](https://pypi.org/project/synth-dynamics/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/synth-dynamics.svg)](https://pypi.org/project/synth-dynamics/)
[![Tests](https://github.com/elkins/synth-dynamics/actions/workflows/test.yml/badge.svg)](https://github.com/elkins/synth-dynamics/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`synth-dynamics` is a fast, coarse-grained engine for generating time-resolved structural ensembles using Elastic Network Models (ENM) and Langevin dynamics.

---

### 🧪 For Structural Biologists
*   **Ensemble Generation:** Rapidly sample the conformational landscape of a protein to simulate disordered states or flexible loops.
*   **Integration:** Works seamlessly with `MDAnalysis` and `biotite` for trajectory processing.

### 🤖 For Machine Learning Geeks
*   **Dynamic Data:** Generate synthetic molecular trajectories to train time-series models (LSTMs, Transformers) or dynamic GNNs.
*   **High Performance:** Optimized for throughput, allowing the generation of millisecond-scale ensembles in seconds.

---

## 📦 Installation

```bash
pip install synth-dynamics
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

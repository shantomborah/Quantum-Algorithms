# Quantum-Algorithms
Implementation of a collection of quantum algorithms using qiskit. In partial fulfilment of BITS F421T Thesis. A Qiskit installation is required to run the code. For details on installation of Qiskit, refer to <https://qiskit.org/documentation/install.html>. Contents of the repository are described below.
## Standard Algorithms
Collection of detailed notes on standard quantum algorithms simulated in Qiskit. Recommend NbViewer for viewing:
<https://nbviewer.jupyter.org/github/Arkonaire/Quantum-Algorithms/tree/master/Standard%20Algorithms/>
## HHL Algorithm
An implementation of the HHL Algorithm for the simple case described in [1].
1) hhl_simulation.py: Simplistic Simulation of HHL Algorithm.
2) hhl_components.py: Generalized Circuit for HHL. Yields good results in limited cases due to less number of qubits involved in classical simulations.
## QAOA Algorithm
Implementation of the Max-Cut Solution using QAOA
1) qaoa_components.py: Variational Circuit for QAOA.
2) qaoa_maxcut.py: Simulation of the max cut problem using QAOA.
## Schumacher Compression
An implementation of Schumacher's Block Coding Scheme.
1) compressor.py: Schumacher Compression for a simple case (Both with and w/o noise)
## Quantum Error Correction
3 Qubit and 5 Qubit error correcting codes.
1) three_qubit_code.py: Quantum Circuit for the 3 Qubit Code.
2) five_qubit_code.py: Quantum Circuit for the 5 Qubit Code.
3) three_qubit_simulation.py: Simulation of the 3 Qubit Code.
4) five_qubit_simulation.py: Simulation of the 5 Qubit Code.
5) noise.py: Qiskit noise models for the simulations

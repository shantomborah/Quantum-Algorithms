# Quantum-Algorithms
Implementation of a collection of quantum algorithms using qiskit. In partial fulfilment of BITS F421T Thesis. A Qiskit installation is required to run the code. For details on installation of Qiskit, refer to <https://qiskit.org/documentation/install.html>. Contents of the repository are described below.
## Standard Algorithms
Collection of detailed notes on standard quantum algorithms simulated in Qiskit. Recommend NbViewer for viewing:
<https://nbviewer.jupyter.org/github/Arkonaire/Quantum-Algorithms/tree/master/Standard%20Algorithms/>
## HHL Algorithm
An implementation of the HHL Algorithm for the simple case described in [2].
* __hhl_simulation.py:__ Simplistic Simulation of HHL Algorithm.
* __hhl_components.py:__ Generalized Circuit for HHL. Yields good results in limited cases due to less number of qubits involved in classical simulations.
## QAOA Algorithm
Implementation of the Max-Cut Solution using QAOA
* __qaoa_components.py:__ Variational Circuit for QAOA.
* __qaoa_maxcut.py:__ Simulation of the max cut problem using QAOA.
## Schumacher Compression
An implementation of Schumacher's Block Coding Scheme.
* __compressor.py:__ Schumacher Compression for a simple case (Both with and w/o noise)
## Quantum Error Correction
3 Qubit and 5 Qubit error correcting codes.
* __three_qubit_code.py:__ Quantum Circuit for the 3 Qubit Code.
* __five_qubit_code.py:__ Quantum Circuit for the 5 Qubit Code.
* __three_qubit_simulation.py:__ Simulation of the 3 Qubit Code.
* __five_qubit_simulation.py:__ Simulation of the 5 Qubit Code.
* __noise.py:__ Qiskit noise models for the simulations
## References
Note: References for the Jupyter Notebooks in Standard Algorithms may be found within the respective Notebooks.
1. Hector Abraham et al. _Qiskit: An Open-source Framework for Quantum Computing_. 2019. doi: 10.5281/zenodo.2562110.
2. Yudong Cao et al. "Quantum circuit design for solving linear systems of equations". In: _Molecular Physics_ 110.15-16 (2012), pp. 1675-1680.
3. David Deutsch. "Quantum theory, the Church-Turing principle and the universal quantum computer". In: _Proceedings of the Royal Society of London. A. Mathematical and Physical Sciences_ 400.1818 (1985), pp. 97-117.
4. David Deutsch and Richard Jozsa. "Rapid solution of problems by quantum computation". In: _Proceedings of the Royal Society of London. Series A: Mathematical and Physical Sciences_ 439.1907 (1992), pp. 553-558.
5. Edward Farhi, Jeffrey Goldstone, and Sam Gutmann. "A quantum approximate optimization algorithm". In: _arXiv preprint arXiv:1411.4028_ (2014).
6. Laszlo Gyongyosi, Sandor Imre, and Hung Viet Nguyen. "A survey on quantum channel capacities". In: _IEEE Communications Surveys & Tutorials_ 20.2 (2018), pp. 1149-1205.
7. Alexander S Holevo. "The capacity of the quantum channel with general signal states". In: _IEEE Transactions on Information Theory_ 44.1 (1998), pp. 269-273.
8. Seth Lloyd. "Quantum algorithm for solving linear systems of equations". In: _APS_ 2010 (2010), pp. D4-002.
9. Michael A. Nielsen and Isaac L. Chuang. _Quantum Computation and Quantum Information: 10th Anniversary Edition_. 10th. USA: Cambridge University Press, 2011. ISBN: 1107002176.
10. John Preskill. "Lecture notes for physics 229: Quantum information and computation". In: _California Institute of Technology_ 16 (1998).
11. Benjamin Schumacher. "Quantum coding". In: _Physical Review A_ 51.4 (1995), p. 2738.
12. Claude E Shannon. "A mathematical theory of communication". In: _The Bell system technical journal_ 27.3 (1948), pp. 379-423.
13. Peter W Shor. "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer". In: _SIAM review_ 41.2 (1999), pp. 303-332.31
14. Peter W Shor. "Scheme for reducing decoherence in quantum computer memory". In: _Physical review A_ 52.4 (1995), R2493.
15. Graeme Smith. "Quantum channel capacities". In: _2010 IEEE Information Theory Work-shop_. IEEE. 2010, pp. 1-5.
16. John Von Neumann. _Mathematical foundations of quantum mechanics: New edition_. Princeton university press, 2018.
17. Mark M. Wilde. _Quantum Information Theory_. 1st. USA: Cambridge University Press, 2013. ISBN: 1107034256.

import random
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import state_fidelity
from qiskit.quantum_info import Statevector, DensityMatrix, Operator


class Compressor:

    def __init__(self, ensemble, block_size):

        # Initialize parameters
        self.ensemble = ensemble
        self.n = block_size
        self.m = block_size
        self.theta = ParameterVector('theta', length=block_size)
        self.phi = ParameterVector('phi', length=block_size)

        # Initialize density matrix properties
        self.rho = np.zeros((2, 2))
        self.s0 = np.array([0, 0])
        self.s1 = np.array([0, 0])
        self.entropy = 1
        self.initialize_density_matrix()
        self.noise = ParameterVector('noise', length=self.m)

        # Build subcircuits
        self.ns_ckt = QuantumCircuit(self.n, name='$Noise$')
        self.source = QuantumCircuit(self.n, name='$Src$')
        self.tx_ckt = QuantumCircuit(self.n, name='$Tx$')
        self.rx_ckt = QuantumCircuit(self.n, name='$Rx$')
        self.initialize_subcircuits()

    def initialize_density_matrix(self):

        # Evaluate density matrix and list of states
        for key in self.ensemble.keys():
            theta = key[0]
            phi = key[1]
            state = np.array([np.cos(theta/2), np.sin(theta/2) * np.exp(phi*complex(1, 0))])
            self.rho = self.rho + self.ensemble[key] * np.outer(state, state)

        # Evaluate spectrum
        self.rho: np.ndarray
        v, w = np.linalg.eig(self.rho)
        s0 = Statevector(w[:, 0])
        s1 = Statevector(w[:, 1])
        self.rho = DensityMatrix(self.rho)

        # Evaluate entropy and typical basis
        if state_fidelity(s0, self.rho) > state_fidelity(s1, self.rho):
            self.s0 = s0
            self.s1 = s1
        else:
            self.s0 = s1
            self.s1 = s0
        self.entropy = -np.real(sum([p * np.log2(p) for p in v]))
        self.m = int(np.ceil(self.entropy * self.n))

    def initialize_subcircuits(self):

        # Build source
        self.source.reset(range(self.n))
        for i in range(self.n):
            self.source.ry(self.theta[i], i)
            self.source.rz(self.phi[i], i)

        # Build typical basis change operator
        U = Operator(np.column_stack((self.s0.data, self.s1.data))).adjoint()
        for i in range(self.n):
            self.tx_ckt.unitary(U, [i], label='$Basis$')

        # Build permutation operator
        data = list(range(2 ** self.n))
        data = [("{0:0" + str(self.n) + "b}").format(i) for i in data]
        data = sorted(data, key=lambda x: x.count('1'))
        data = [int(x, 2) for x in data]
        V = np.zeros((2 ** self.n, 2 ** self.n))
        for i in range(2 ** self.n):
            V[i, data[i]] = 1
        self.tx_ckt.unitary(V, list(range(self.n)), label='$Perm$')

        # Build bit flip noisy channel
        for i in range(self.m):
            self.ns_ckt.u3(self.noise[i], 0, self.noise[i], i)

        # Build receiver
        self.rx_ckt.reset(range(self.m, self.n))
        self.rx_ckt.append(self.tx_ckt.to_gate().inverse(), list(range(self.n)))

    def simulate(self, num_shots=1, bit_flip_prob=0.0):

        # Get backend and circuit
        simulator = Aer.get_backend('statevector_simulator')
        circ = self.source + self.tx_ckt + self.ns_ckt + self.rx_ckt
        fid_list = []

        for i in range(num_shots):

            # Acquire parameters
            states = random.choices(list(self.ensemble.keys()), self.ensemble.values(), k=self.n)
            noise = random.choices([0, np.pi], [1-bit_flip_prob, bit_flip_prob], k=self.m)
            theta = [p[0] for p in states]
            phi = [p[1] for p in states]
            circ1 = self.source.bind_parameters({self.theta: theta, self.phi: phi})
            circ2 = circ.bind_parameters({self.theta: theta, self.phi: phi, self.noise: noise})

            # Simulate
            ini_state = execute(circ1, simulator).result().get_statevector()
            fin_state = execute(circ2, simulator).result().get_statevector()
            fid_list.append(state_fidelity(ini_state, fin_state))

        # Return results
        return fid_list

    def visualize(self):

        # Draw components
        self.source.draw('mpl', reverse_bits=True).suptitle('Source Circuit')
        self.tx_ckt.draw('mpl', reverse_bits=True).suptitle('Tx Circuit')
        self.rx_ckt.draw('mpl', reverse_bits=True).suptitle('Rx Circuit')
        (self.source + self.tx_ckt + self.ns_ckt + self.rx_ckt).draw('mpl', reverse_bits=True).suptitle('Full Circuit')
        plt.show()


if __name__ == '__main__':
    ensemble = {(0, 0): 0.5, (np.pi/2, 0): 0.5}
    com = Compressor(ensemble, 3)
    com.visualize()
    fid1 = com.simulate(num_shots=100)
    fid2 = com.simulate(num_shots=100, bit_flip_prob=0.1)
    print('Noiseless System Fidelity: ', np.mean(fid1))
    print('Noisy (p = 0.1) System Fidelity: ', np.mean(fid2))

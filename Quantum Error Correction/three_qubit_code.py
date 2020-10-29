import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit.quantum_info import Operator
from qiskit.circuit.library.standard_gates import XGate


class ThreeQubitCode:

    def __init__(self):

        # Initialize Registers
        self.code = QuantumRegister(3, name="code")
        self.syndrm = QuantumRegister(2, name="syndrome")

        # Build Circuit Components
        self.encoder_ckt = self.build_encoder()
        self.syndrome_ckt = self.build_syndrome()
        self.correction_ckt = self.build_correction()

        # Build Noisy Channel
        self.noise_ckt = QuantumCircuit(self.code, self.syndrm)
        self.noise_ckt.unitary(Operator(np.eye(2)), [self.code[0]], label='noise')
        self.noise_ckt.unitary(Operator(np.eye(2)), [self.code[1]], label='noise')
        self.noise_ckt.unitary(Operator(np.eye(2)), [self.code[2]], label='noise')

        # Compose Full Circuit
        circ = QuantumCircuit(self.code, self.syndrm)
        circ.barrier()
        self.circuit = self.encoder_ckt + circ + self.noise_ckt + circ + self.syndrome_ckt + circ + self.correction_ckt

    def build_encoder(self):

        # Build Encoder Circuit
        circ = QuantumCircuit(self.code, self.syndrm, name="Encoder Circuit")
        circ.cx(self.code[0], self.code[1])
        circ.cx(self.code[0], self.code[2])
        return circ

    def build_syndrome(self):

        # Build Syndrome Circuit
        circ = QuantumCircuit(self.code, self.syndrm, name="Syndrome Circuit")
        circ.h(self.syndrm)
        circ.barrier()
        circ.cz(self.syndrm[1], self.code[2])
        circ.cz(self.syndrm[1], self.code[1])
        circ.cz(self.syndrm[0], self.code[1])
        circ.cz(self.syndrm[0], self.code[0])
        circ.barrier()
        circ.h(self.syndrm)
        return circ

    def build_correction(self):

        # Build Correction Circuit
        circ = QuantumCircuit(self.code, self.syndrm)
        circ.append(XGate().control(2, ctrl_state=2), [self.syndrm[0], self.syndrm[1], self.code[2]])
        circ.append(XGate().control(2, ctrl_state=3), [self.syndrm[0], self.syndrm[1], self.code[1]])
        circ.append(XGate().control(2, ctrl_state=1), [self.syndrm[0], self.syndrm[1], self.code[0]])
        return circ

    def visualize(self):

        # Draw Circuits
        self.encoder_ckt.draw('mpl', reverse_bits=True).suptitle('Encoder Circuit', fontsize=16)
        self.syndrome_ckt.draw('mpl', reverse_bits=True).suptitle('Syndrome Circuit', fontsize=16)
        self.correction_ckt.draw('mpl', reverse_bits=True).suptitle('Error Correction', fontsize=16)
        self.circuit.draw('mpl', reverse_bits=True).suptitle('Three Qubit Error Correction', fontsize=16)
        plt.show()

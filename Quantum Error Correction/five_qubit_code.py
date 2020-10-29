import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit.quantum_info import Operator
from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate


class FiveQubitCode:

    def __init__(self):
        # Initialize Registers
        self.code = QuantumRegister(5, name="code")
        self.syndrm = QuantumRegister(4, name="syndrome")

        # Build Circuit Components
        self.encoder_ckt = self.build_encoder()
        self.syndrome_ckt = self.build_syndrome()
        self.correction_ckt = self.build_correction()
        self.decoder_ckt = self.encoder_ckt.mirror()

        # Build Noisy Channel
        self.noise_ckt = QuantumCircuit(self.code, self.syndrm)
        for i in range(5):
            self.noise_ckt.unitary(Operator(np.eye(2)), [self.code[i]], label='noise')

        # Compose Full Circuit
        circ = QuantumCircuit(self.code, self.syndrm)
        circ.barrier()
        self.circuit = self.encoder_ckt + circ + self.noise_ckt + circ + self.syndrome_ckt
        self.circuit = self.circuit + circ + self.correction_ckt + circ + self.decoder_ckt

    def build_encoder(self):
        # Build Encoder Circuit
        circ = QuantumCircuit(self.code, self.syndrm, name="Encoder Circuit")
        circ.z(self.code[4])
        circ.h(self.code[4])
        circ.z(self.code[4])
        circ.cx(self.code[4], self.code[3])
        circ.h(self.code[4])
        circ.h(self.code[3])
        circ.cx(self.code[4], self.code[2])
        circ.cx(self.code[3], self.code[2])
        circ.h(self.code[2])
        circ.cx(self.code[4], self.code[1])
        circ.cx(self.code[2], self.code[1])
        circ.h(self.code[1])
        circ.h(self.code[4])
        circ.cx(self.code[4], self.code[0])
        circ.cx(self.code[3], self.code[0])
        circ.cx(self.code[2], self.code[0])
        circ.h(self.code[3])
        circ.h(self.code[4])
        return circ

    def build_syndrome(self):
        # Build Syndrome Circuit
        circ = QuantumCircuit(self.code, self.syndrm, name="Syndrome Circuit")
        circ.h(self.syndrm)
        circ.barrier()
        circ.cz(self.syndrm[0], self.code[4])
        circ.cx(self.syndrm[0], self.code[3])
        circ.cx(self.syndrm[0], self.code[2])
        circ.cz(self.syndrm[0], self.code[1])
        circ.cx(self.syndrm[1], self.code[4])
        circ.cx(self.syndrm[1], self.code[3])
        circ.cz(self.syndrm[1], self.code[2])
        circ.cz(self.syndrm[1], self.code[0])
        circ.cx(self.syndrm[2], self.code[4])
        circ.cz(self.syndrm[2], self.code[3])
        circ.cz(self.syndrm[2], self.code[1])
        circ.cx(self.syndrm[2], self.code[0])
        circ.cz(self.syndrm[3], self.code[4])
        circ.cz(self.syndrm[3], self.code[2])
        circ.cx(self.syndrm[3], self.code[1])
        circ.cx(self.syndrm[3], self.code[0])
        circ.barrier()
        circ.h(self.syndrm)
        return circ

    def build_correction(self):
        # Build Correction Circuit
        circ = QuantumCircuit(self.code, self.syndrm)
        circ.append(XGate().control(4, ctrl_state='0010'), [self.syndrm[i] for i in range(4)] + [self.code[0]])
        circ.append(YGate().control(4, ctrl_state='1110'), [self.syndrm[i] for i in range(4)] + [self.code[0]])
        circ.append(ZGate().control(4, ctrl_state='1100'), [self.syndrm[i] for i in range(4)] + [self.code[0]])
        circ.append(XGate().control(4, ctrl_state='0101'), [self.syndrm[i] for i in range(4)] + [self.code[1]])
        circ.append(YGate().control(4, ctrl_state='1101'), [self.syndrm[i] for i in range(4)] + [self.code[1]])
        circ.append(ZGate().control(4, ctrl_state='1000'), [self.syndrm[i] for i in range(4)] + [self.code[1]])
        circ.append(XGate().control(4, ctrl_state='1010'), [self.syndrm[i] for i in range(4)] + [self.code[2]])
        circ.append(YGate().control(4, ctrl_state='1011'), [self.syndrm[i] for i in range(4)] + [self.code[2]])
        circ.append(ZGate().control(4, ctrl_state='0001'), [self.syndrm[i] for i in range(4)] + [self.code[2]])
        circ.append(XGate().control(4, ctrl_state='0100'), [self.syndrm[i] for i in range(4)] + [self.code[3]])
        circ.append(YGate().control(4, ctrl_state='0111'), [self.syndrm[i] for i in range(4)] + [self.code[3]])
        circ.append(ZGate().control(4, ctrl_state='0011'), [self.syndrm[i] for i in range(4)] + [self.code[3]])
        circ.append(XGate().control(4, ctrl_state='1001'), [self.syndrm[i] for i in range(4)] + [self.code[4]])
        circ.append(YGate().control(4, ctrl_state='1111'), [self.syndrm[i] for i in range(4)] + [self.code[4]])
        circ.append(ZGate().control(4, ctrl_state='0110'), [self.syndrm[i] for i in range(4)] + [self.code[4]])
        return circ

    def visualize(self):
        # Draw Circuits
        self.encoder_ckt.draw('mpl', reverse_bits=True).suptitle('Encoder Circuit', fontsize=16)
        self.syndrome_ckt.draw('mpl', reverse_bits=True).suptitle('Syndrome Circuit', fontsize=16)
        self.correction_ckt.draw('mpl', reverse_bits=True).suptitle('Error Correction', fontsize=16)
        self.decoder_ckt.draw('mpl', reverse_bits=True).suptitle('Decoder Circuit', fontsize=16)
        self.circuit.draw('mpl', reverse_bits=True, style={'fontsize': 4}) \
            .suptitle('Five Qubit Error Correction', fontsize=16)
        plt.show()

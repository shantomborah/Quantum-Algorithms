"""Performance Analysis of 5 Qubit Code under Depolarizing Error"""

import noise
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit import Aer, execute
from qiskit.visualization import plot_histogram, plot_bloch_vector
from five_qubit_code import FiveQubitCode

# Parameters
error_prob = 0.05
theta = np.pi / 3
phi = np.pi / 4

# Initialize error correcting circuit, backend and noise model
qasm = Aer.get_backend('qasm_simulator')
noise_depol = noise.depolarizing_noise(error_prob)
qecc = FiveQubitCode()

# Visualize parameters
print(noise_depol)
qecc.visualize()

# Define test circuit and input state
output = ClassicalRegister(5)
circ = QuantumCircuit(qecc.code, qecc.syndrm, output)
circ.ry(theta, qecc.code[4])
circ.rz(phi, qecc.code[4])
plot_bloch_vector([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)], title="Input State")
plt.show()

# Define final measurement circuit
meas = QuantumCircuit(qecc.code, qecc.syndrm, output)
meas.measure(qecc.code, output)

# QASM simulation w/o error correction
job = execute(circ + qecc.encoder_ckt + qecc.noise_ckt + qecc.decoder_ckt + meas,
              backend=qasm, noise_model=noise_depol, basis_gates=noise_depol.basis_gates)
counts_noisy = job.result().get_counts()

# QASM simulation with error correction
job = execute(circ + qecc.circuit + meas, backend=qasm, noise_model=noise_depol,
              basis_gates=noise_depol.basis_gates)
counts_corrected = job.result().get_counts()

# Plot QASM simulation data
plot_histogram([counts_noisy, counts_corrected],
               title='5-Qubit Error Correction  - Depolarizing Noise $(P_{error} = ' + str(error_prob) + ')$',
               legend=['w/o code', 'with code'], figsize=(12, 9), bar_labels=False)
plt.subplots_adjust(left=0.15, right=0.72, top=0.9, bottom=0.20)
plt.show()

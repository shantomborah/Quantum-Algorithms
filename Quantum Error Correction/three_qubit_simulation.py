"""Performance Analysis of 3 Qubit Code under Bit Flip Error"""

import noise
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit import Aer, execute
from qiskit.quantum_info import partial_trace, state_fidelity
from qiskit.quantum_info import DensityMatrix, Kraus
from qiskit.visualization import plot_histogram, plot_bloch_vector
from three_qubit_code import ThreeQubitCode

# Parameters
error_prob = 0.05
theta = np.pi/3
phi = np.pi/4

# Initialize error correcting circuit, backend and noise model
qasm = Aer.get_backend('qasm_simulator')
svsm = Aer.get_backend('statevector_simulator')
unit = Aer.get_backend('unitary_simulator')
noise_model = noise.bit_flip_noise(error_prob)
qecc = ThreeQubitCode()

# Visualize parameters
print(noise_model)
qecc.visualize()

# Define test circuit and input state
output = ClassicalRegister(3)
circ = QuantumCircuit(qecc.code, qecc.syndrm, output)
circ.ry(theta, qecc.code[0])
circ.rz(phi, qecc.code[0])
plot_bloch_vector([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)], title="Input State")
plt.show()

# Define final measurement circuit
meas = QuantumCircuit(qecc.code, qecc.syndrm, output)
meas.measure(qecc.code, output)

# QASM simulation w/o error correction
job = execute(circ + qecc.encoder_ckt + qecc.noise_ckt + meas, backend=qasm, noise_model=noise_model,
              basis_gates=noise_model.basis_gates)
counts_noisy = job.result().get_counts()

# QASM simulation with error correction
job = execute(circ + qecc.circuit + meas, backend=qasm, noise_model=noise_model,
              basis_gates=noise_model.basis_gates)
counts_corrected = job.result().get_counts()

# Plot QASM simulation data
plot_histogram([counts_noisy, counts_corrected],
               title='3-Qubit Error Correction $(P_{error} = ' + str(error_prob) + ')$',
               legend=['w/o code', 'with code'], figsize=(12, 9), bar_labels=False)
plt.subplots_adjust(left=0.15, right=0.72, top=0.9, bottom=0.15)
plt.show()

# Initialize fidelity simulation objects
job = execute(circ + qecc.encoder_ckt, backend=svsm)
init_state = DensityMatrix(job.result().get_statevector())
job = execute(qecc.syndrome_ckt, backend=unit)
syndrome_op = Kraus(job.result().get_unitary())

# Initialize fidelity simulation parameters
p_error = [0.05 * i for i in range(11)]
f1 = []
f2 = []

# Evolve initial state
for p in p_error:

    # Build noise channel
    bit_flip_channel = Kraus([[[0, np.sqrt(p)],
                               [np.sqrt(p), 0]],
                              [[np.sqrt(1-p), 0],
                               [0, np.sqrt(1-p)]]])
    bit_flip_channel = bit_flip_channel.tensor(bit_flip_channel).tensor(bit_flip_channel)
    bit_flip_channel = bit_flip_channel.expand(Kraus(np.eye(2))).expand(Kraus(np.eye(2)))

    # Apply channels
    corrupted_state = DensityMatrix(init_state.evolve(bit_flip_channel))
    corrected_state = DensityMatrix(corrupted_state.evolve(syndrome_op))
    corrected_state = DensityMatrix(corrected_state.evolve(qecc.correction_ckt))

    # Trace out syndrome
    ini = DensityMatrix(partial_trace(init_state, [3, 4]))
    corrupted_state = DensityMatrix(partial_trace(corrupted_state, [3, 4]))
    corrected_state = DensityMatrix(partial_trace(corrected_state, [3, 4]))

    # Record results
    f1.append(state_fidelity(ini, corrupted_state))
    f2.append(state_fidelity(ini, corrected_state))

# Plot fidelity
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.plot(p_error, f1, label='w/o code')
ax.plot(p_error, f2, label='with code')
ax.set_title("$Fidelity$ vs $P_{error}$")
ax.set_xlabel('$P_{error}$')
ax.set_ylabel('$Fidelity$')
ax.set_ylabel('$Fidelity$')
ax.legend()
plt.xlim(0, 0.5)
plt.ylim(0, 1)
plt.grid()
plt.show()

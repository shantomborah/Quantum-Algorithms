import numpy as np
import components as cmp
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit import Aer, execute
from qiskit.visualization import plot_histogram

# Initialize parameters
t0 = 2 * np.pi
r = 6
A = [[3.75, 2.25, 1.25, -0.75],
     [2.25, 3.75, 0.75, -1.25],
     [1.25, 0.75, 3.75, -2.25],
     [-0.75, -1.25, -2.25, 3.75]]
b = [0.5, 0.5, 0.5, 0.5]
x = [-0.0312, 0.2188, 0.3437, 0.4062]
p = [i ** 2 for i in x]
basis = ['00', '01', '10', '11']

# Build circuit
circ = QuantumCircuit(7, 3)
circ.initialize(b, range(2))
circ.append(cmp.ad_hoc_hhl(A, t0, r), range(7))
circ.measure(6, 2)
circ.measure([0, 1], [0, 1])

# Get simulators
qasm = Aer.get_backend('qasm_simulator')
svsm = Aer.get_backend('statevector_simulator')

# QASM simulation
job = execute(circ, qasm, shots=1024)
counts = job.result().get_counts()
measured_data = {}
expected_data = {basis[i]: np.floor(p[i] * 1024) for i in range(4)}
for key in counts.keys():
    if key[0] == '1':
        measured_data[key[1::]] = counts[key]
plot_histogram([expected_data, measured_data], title='HHL QASM Simulation', legend=['expected', 'measured'])
plt.subplots_adjust(left=0.15, right=0.72, top=0.9, bottom=0.15)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.extensions import HamiltonianGate
from qiskit.circuit.library.standard_gates import CRYGate


def quantum_fourier_transform(t, vis=False):
    reg = QuantumRegister(t, name='c')
    circ = QuantumCircuit(reg, name='$Q.F.T.$')
    for i in range(t // 2):
        circ.swap(i, t - 1 - i)
    for i in range(t):
        circ.h(i)
        for j in range(i + 1, t):
            circ.cu1(np.pi / (2 ** (j - i)), i, j)
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle("Quantum Fourier Transform", fontsize=16)
    return circ.to_gate()


def quantum_phase_estimation(n, t, unitary, vis=False):
    reg_b = QuantumRegister(n, name='b')
    reg_c = QuantumRegister(t, name='c')
    circ = QuantumCircuit(reg_b, reg_c, name='$Q.P.E.$')
    circ.h(range(n, n + t))
    for i in range(t):
        circ.append(unitary.control(1).power(2**i), [n + i] + list(range(n)))
    circ.append(quantum_fourier_transform(t, vis=vis).inverse(), range(n, n + t))
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle("Quantum Phase Estimation", fontsize=16)
    return circ.to_gate()


def subroutine_a(t, m, l, k, t0, vis=False):
    reg_c = QuantumRegister(t, name='c')
    reg_m = QuantumRegister(m, name='m')
    reg_l = QuantumRegister(l, name='l')
    circ = QuantumCircuit(reg_c, reg_m, reg_l, name='$Sub_A$')
    vis_temp = vis
    for i in range(t):
        gate = subroutine_c(m, t - i, l - k, t0, vis=vis_temp)
        circ.append(gate.control(2), [reg_l[k], reg_c[i]] + [reg_m[j] for j in range(m)])
        vis_temp = False
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle("Subroutine A", fontsize=16)
    return circ.to_gate()


def subroutine_b(t, m, l, t0, vis=False):
    reg_c = QuantumRegister(t, name='c')
    reg_m = QuantumRegister(m, name='m')
    reg_l = QuantumRegister(l, name='l')
    circ = QuantumCircuit(reg_c, reg_m, reg_l, name='$Sub_B$')
    vis_temp = vis
    for i in range(l):
        gate = subroutine_a(t, m, l, i, t0, vis=vis_temp)
        circ.append(gate, range(t + m + l))
        vis_temp = False
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle("Subroutine B", fontsize=16)
    return circ.to_gate()


def subroutine_c(m, u, v, t0, vis=False):
    reg = QuantumRegister(m, name='m')
    circ = QuantumCircuit(reg, name='$Sub_C$')
    t = -t0 / (2 ** (u + v - m))
    for i in range(m):
        circ.rz(t / (2 ** (i + 1)), i)
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle("Subroutine C", fontsize=16)
    return circ.to_gate()


def hhl_forward_ckt(n, t, m, l, A, t0, vis=False):
    reg_b = QuantumRegister(n, name='b')
    reg_c = QuantumRegister(t, name='c')
    reg_m = QuantumRegister(m, name='m')
    reg_l = QuantumRegister(l, name='l')
    temp = QuantumCircuit(reg_b, name='$U$')
    temp.append(HamiltonianGate(A, t0 / (2 ** t)), reg_b)
    circ = QuantumCircuit(reg_b, reg_c, reg_m, reg_l, name='$Fwd$')
    circ.append(quantum_phase_estimation(n, t, temp.to_gate(), vis=vis), range(n + t))
    circ.h(reg_m)
    circ.h(reg_l)
    for i in range(m):
        circ.rz(t0 / (2 ** (m - i)), reg_m[i])
    circ.append(subroutine_b(t, m, l, t0, vis=vis), range(n, n + t + m + l))
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle('HHL Forward Computation', fontsize=16)
    return circ.to_gate()


def hhl_circuit(A, t0, theta, size, vis=False):
    n, t, m, l = size
    reg_b = QuantumRegister(n, name='b')
    reg_c = QuantumRegister(t, name='c')
    reg_m = QuantumRegister(m, name='m')
    reg_l = QuantumRegister(l, name='l')
    ancil = QuantumRegister(1, name='anc')
    circ = QuantumCircuit(reg_b, reg_c, reg_m, reg_l, ancil, name='$HHL$')
    circ.append(hhl_forward_ckt(n, t, m, l, A, t0, vis=vis), range(sum(size)))
    for i in range(l):
        circ.append(CRYGate(theta).power(2**i), [reg_l[i], ancil])
    circ.append(hhl_forward_ckt(n, t, m, l, A, t0).inverse(), range(sum(size)))
    if vis:
        circ.draw('mpl', reverse_bits=True, style={'fontsize': 6, 'subfontsize': 3})\
            .suptitle('HHL Circuit', fontsize=16)
    return circ


def ad_hoc_hhl(A, t0, r):
    reg_b = QuantumRegister(2)
    reg_c = QuantumRegister(4)
    ancil = QuantumRegister(1)
    circ = QuantumCircuit(reg_b, reg_c, ancil)
    circ.append(quantum_phase_estimation(2, 4, HamiltonianGate(A, t0/16)), range(6))
    circ.swap(reg_c[1], reg_c[3])
    for i in range(4):
        circ.cry(np.pi * (2 ** (4-i-r)), reg_c[i], ancil[0])
        circ.barrier()
    circ.swap(reg_c[1], reg_c[3])
    circ.append(quantum_phase_estimation(2, 4, HamiltonianGate(A, t0 / 16)).inverse(), range(6))
    return circ


if __name__ == '__main__':
    size = [3, 4, 4, 4]
    theta = np.pi/12
    t0 = 2 * np.pi
    A = [[0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 0]]
    circ = hhl_circuit(A, t0, theta, size, vis=True)
    plt.show()

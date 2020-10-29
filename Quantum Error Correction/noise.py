from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import pauli_error
from qiskit.providers.aer.noise import depolarizing_error


def bit_flip_noise(p):
    noise_model = NoiseModel()
    error = pauli_error([('X', p), ('I', 1 - p)])
    noise_model.add_all_qubit_quantum_error(error, 'noise')
    noise_model.add_basis_gates(['unitary'])
    return noise_model


def depolarizing_noise(p):
    noise_model = NoiseModel()
    error = depolarizing_error(p, num_qubits=1)
    noise_model.add_all_qubit_quantum_error(error, 'noise')
    noise_model.add_basis_gates(['unitary'])
    return noise_model

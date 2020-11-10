import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import ParameterVector
from qiskit.extensions import HamiltonianGate
from qiskit.visualization import plot_histogram
from qiskit.aqua.components.optimizers import COBYLA


class QAOA:

    def __init__(self, clauses, p, num_shots=1024):

        # Assign weights and clauses
        if isinstance(clauses, dict):
            self.clauses = list(clauses.values())
            self.weights = list(clauses.keys())
        else:
            self.clauses = clauses
            self.weights = [1] * len(clauses)

        # Assign size parameters
        self.m = len(self.clauses)
        self.n = len(self.clauses[0])
        self.p = p

        # Assign auxiliary parameters
        self.num_shots = num_shots
        self.error = -1

        # Create variational parameters
        self.gamma = ParameterVector('gamma', length=p)
        self.beta = ParameterVector('beta', length=p)
        self.gamma_val = list(np.random.rand(p))
        self.beta_val = list(np.random.rand(p))

        # Create hamiltonians and variational circuit
        self.B = np.eye(2 ** self.n)[::-1]
        self.C = np.diag([self.cost(z) for z in range(2 ** self.n)])
        self.varckt = self.build_varckt()
        self.optimize()

    def cost(self, z):

        # Convert to bitstr
        if not isinstance(z, str):
            z = format(z, '0' + str(self.n) + 'b')
        z: str

        # Evaluate C(z)
        cost = 0
        for i in range(self.m):
            s = True
            for j in range(self.n):
                if self.clauses[i][j] != 'X' and self.clauses[i][j] != z[j]:
                    s = False
                    break
            if s:
                cost += self.weights[i]

        # Return output
        return cost

    def expectation(self, beta=None, gamma=None):

        # Resolve default values
        if beta is None:
            beta = self.beta_val
        if gamma is None:
            gamma = self.gamma_val

        # Evaluate expectation value
        circ = self.varckt.bind_parameters({self.beta: beta, self.gamma: gamma})
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(circ, simulator, shots=self.num_shots).result()
        counts = result.get_counts()
        expval = sum([self.cost(z) * counts[z] / self.num_shots for z in counts.keys()])
        return expval

    def optimize(self):

        # Define objective function
        def objfunc(params):
            return -self.expectation(beta=params[0:self.p], gamma=params[self.p:2*self.p])

        # Optimize parameters
        optimizer = COBYLA(maxiter=1000, tol=0.0001)
        params = self.beta_val + self.gamma_val
        ret = optimizer.optimize(num_vars=2*self.p, objective_function=objfunc, initial_point=params)
        self.beta_val = ret[0][0:self.p]
        self.gamma_val = ret[0][self.p:2*self.p]
        self.error = ret[1]
        return

    def build_varckt(self):

        # Build variational circuit
        circ = QuantumCircuit(self.n)
        circ.h(range(self.n))
        for i in range(self.p):
            eC = QuantumCircuit(self.n, name='$U(C,\\gamma_' + str(i + 1) + ')$')
            eC.append(HamiltonianGate(self.C, self.gamma[i]), range(self.n))
            eB = QuantumCircuit(self.n, name='$U(B,\\beta_' + str(i + 1) + ')$')
            eB.append(HamiltonianGate(self.B, self.beta[i]), range(self.n))
            circ.append(eC.to_gate(), range(self.n))
            circ.append(eB.to_gate(), range(self.n))
        circ.measure_all()
        return circ

    def sample(self, shots=None, vis=False):

        # Resolve defaults
        if shots is None:
            shots = self.num_shots

        # Sample maximum cost value
        circ = self.varckt.bind_parameters({self.beta: self.beta_val, self.gamma: self.gamma_val})
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(circ, simulator, shots=shots).result()
        counts = result.get_counts()
        if vis:
            plot_histogram(counts, title='Sample Output', bar_labels=False)
            plt.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.15)
        return max(counts, key=counts.get)


if __name__ == '__main__':
    qaoa = QAOA(['10XX0', '11XXX'], 3)
    print('Maximized Expectation Value: ' + str(qaoa.expectation()))
    print('Sampled Output: ' + qaoa.sample())
    qaoa.varckt.draw('mpl').suptitle('Variational Circuit', fontsize=16)
    plt.show()

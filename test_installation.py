# test_installation.py
from qiskit import QuantumCircuit
from qiskit_aer import Aer

print("Qiskit Installed Successfully!")
print(f"Qiskit version: {__import__('qiskit').__version__}")

# Create a simple quantum circuit
qc = QuantumCircuit(1)
qc.x(0)
print("\nQuantum Circuit:")
print(qc)

# Show available backends
print("\nAvailable backends:")
backend = Aer.get_backend('qasm_simulator')
print(f"- {backend.name}")

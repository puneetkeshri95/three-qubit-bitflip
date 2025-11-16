# bit_flip_error_simulation.py
"""
Bit-Flip Error Simulation

This script demonstrates how to introduce bit-flip errors into the encoded 3-qubit system.
It simulates real-world quantum errors that can occur during computation or transmission.

A bit-flip error is represented by an X gate that flips |0⟩ ↔ |1⟩
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


def create_encoding_circuit():
    """
    Creates the basic 3-qubit encoding circuit.
    
    Returns:
        QuantumCircuit: Encoding circuit with 3 qubits
    """
    qc = QuantumCircuit(3, 3)
    
    # Encoding: duplicate qubit 0 into qubits 1 and 2
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    return qc


def introduce_bit_flip_error(qc, qubit_index):
    """
    Introduces a bit-flip error on a specific qubit.
    
    Args:
        qc: QuantumCircuit to modify
        qubit_index: Index of the qubit to flip (0, 1, or 2)
    
    Returns:
        QuantumCircuit: Circuit with error introduced
    """
    if qubit_index not in [0, 1, 2]:
        raise ValueError("Qubit index must be 0, 1, or 2")
    
    # Add a barrier for visualization
    qc.barrier()
    
    # Apply X gate to simulate bit-flip error
    qc.x(qubit_index)
    
    # Add another barrier
    qc.barrier()
    
    return qc


def create_circuit_with_error(initial_state='0', error_qubit=None):
    """
    Creates a complete circuit with encoding and optional error.
    
    Args:
        initial_state: '0' or '1' for the initial state
        error_qubit: Index of qubit to flip (0, 1, 2) or None for no error
    
    Returns:
        QuantumCircuit: Complete circuit with encoding and error
    """
    qc = QuantumCircuit(3, 3)
    
    # Initialize the first qubit
    if initial_state == '1':
        qc.x(0)
    
    qc.barrier(label='Init')
    
    # Apply encoding
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    # Introduce error if specified
    if error_qubit is not None:
        qc.barrier(label='Error')
        qc.x(error_qubit)
    
    qc.barrier(label='Measure')
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc


def simulate_circuit(qc, shots=1024):
    """
    Simulates the quantum circuit and returns measurement results.
    
    Args:
        qc: QuantumCircuit to simulate
        shots: Number of measurement shots
    
    Returns:
        dict: Measurement counts
    """
    # Use Aer's qasm_simulator
    simulator = Aer.get_backend('qasm_simulator')
    
    # Transpile circuit for simulator
    compiled_circuit = transpile(qc, simulator)
    
    # Run simulation
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    
    # Get counts
    counts = result.get_counts(qc)
    
    return counts


def visualize_results(counts, title="Measurement Results"):
    """
    Visualizes measurement results as a histogram.
    
    Args:
        counts: Dictionary of measurement counts
        title: Title for the plot
    """
    print(f"\n{title}:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / sum(counts.values())) * 100
        print(f"  |{state}⟩: {count:4d} times ({percentage:5.1f}%)")


def demonstrate_bit_flip_errors():
    """
    Demonstrates bit-flip errors on different qubits.
    """
    print("\n" + "="*70)
    print("BIT-FLIP ERROR SIMULATION")
    print("="*70)
    
    print("\n📖 Concept:")
    print("   After encoding |0⟩ → |000⟩, we introduce X gate errors")
    print("   to simulate bit flips on different qubits.\n")
    
    # Test Case 1: No error (baseline)
    print("\n" + "="*70)
    print("1️⃣  BASELINE: Encoding |0⟩ with NO error")
    print("="*70)
    
    qc_no_error = create_circuit_with_error(initial_state='0', error_qubit=None)
    print(qc_no_error.draw(output='text'))
    
    counts_no_error = simulate_circuit(qc_no_error)
    visualize_results(counts_no_error, "Expected: |000⟩")
    
    # Test Case 2: Error on qubit 0
    print("\n" + "="*70)
    print("2️⃣  ERROR on Qubit 0: |000⟩ → |100⟩")
    print("="*70)
    
    qc_error_0 = create_circuit_with_error(initial_state='0', error_qubit=0)
    print(qc_error_0.draw(output='text'))
    
    counts_error_0 = simulate_circuit(qc_error_0)
    visualize_results(counts_error_0, "Expected: |100⟩ (error on q0)")
    
    # Test Case 3: Error on qubit 1
    print("\n" + "="*70)
    print("3️⃣  ERROR on Qubit 1: |000⟩ → |010⟩")
    print("="*70)
    
    qc_error_1 = create_circuit_with_error(initial_state='0', error_qubit=1)
    print(qc_error_1.draw(output='text'))
    
    counts_error_1 = simulate_circuit(qc_error_1)
    visualize_results(counts_error_1, "Expected: |010⟩ (error on q1)")
    
    # Test Case 4: Error on qubit 2
    print("\n" + "="*70)
    print("4️⃣  ERROR on Qubit 2: |000⟩ → |001⟩")
    print("="*70)
    
    qc_error_2 = create_circuit_with_error(initial_state='0', error_qubit=2)
    print(qc_error_2.draw(output='text'))
    
    counts_error_2 = simulate_circuit(qc_error_2)
    visualize_results(counts_error_2, "Expected: |001⟩ (error on q2)")
    
    # Test Case 5: Encoding |1⟩ with error on qubit 1
    print("\n" + "="*70)
    print("5️⃣  BONUS: Encoding |1⟩ → |111⟩ with error on Qubit 1")
    print("="*70)
    
    qc_1_error = create_circuit_with_error(initial_state='1', error_qubit=1)
    print(qc_1_error.draw(output='text'))
    
    counts_1_error = simulate_circuit(qc_1_error)
    visualize_results(counts_1_error, "Expected: |101⟩ (|111⟩ with error on q1)")
    
    print("\n" + "="*70)
    print("✓ Error simulation completed!")
    print("="*70)
    print("\n💡 Key Observations:")
    print("   • Without error: All measurements give |000⟩ or |111⟩")
    print("   • With error: One qubit differs from the others")
    print("   • Error detection: Use syndrome measurement to identify the faulty qubit")
    print("   • Next step: Implement error correction to fix the bit flip")


def test_single_error_function():
    """
    Tests the introduce_bit_flip_error function directly.
    """
    print("\n" + "="*70)
    print("TESTING: introduce_bit_flip_error() function")
    print("="*70)
    
    for qubit_idx in range(3):
        print(f"\n--- Introducing error on qubit {qubit_idx} ---")
        
        # Create encoding circuit
        qc = create_encoding_circuit()
        
        # Add error
        qc = introduce_bit_flip_error(qc, qubit_idx)
        
        # Add measurement
        qc.measure_all()
        
        print(qc.draw(output='text'))
        
        # Simulate
        counts = simulate_circuit(qc, shots=100)
        print(f"Result: {counts}")


if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_bit_flip_errors()
    
    # Test the error introduction function
    test_single_error_function()
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("• Implement syndrome measurement to detect errors")
    print("• Build error correction logic")
    print("• Combine encoding + error + correction into full pipeline")
    print("="*70 + "\n")

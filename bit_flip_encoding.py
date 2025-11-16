# bit_flip_encoding.py
"""
Three-Qubit Bit-Flip Encoding Circuit

This script demonstrates how to encode a single logical qubit into three physical qubits
to protect against single bit-flip errors using quantum error correction.

Encoding Process:
- Start with qubit q0 in state |ψ⟩ = α|0⟩ + β|1⟩
- Apply CNOT(q0, q1) to copy q0 to q1
- Apply CNOT(q0, q2) to copy q0 to q2
- Result: |ψ⟩ → α|000⟩ + β|111⟩
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt


def create_bit_flip_encoding_circuit():
    """
    Creates a 3-qubit bit-flip encoding circuit.
    
    Returns:
        QuantumCircuit: The encoding circuit with 3 qubits
    """
    # Create a quantum circuit with 3 qubits
    qc = QuantumCircuit(3, name='Bit-Flip Encoding')
    
    # Qubit 0 is the original data qubit
    # Qubits 1 and 2 are redundant copies
    
    # Apply CNOT gates to create entanglement
    # CNOT(control=q0, target=q1): copies q0 to q1
    qc.cx(0, 1)
    
    # CNOT(control=q0, target=q2): copies q0 to q2
    qc.cx(0, 2)
    
    return qc


def create_encoding_with_initial_state(initial_state='0'):
    """
    Creates encoding circuit with a specific initial state.
    
    Args:
        initial_state: '0' for |0⟩, '1' for |1⟩, '+' for |+⟩, '-' for |-⟩
    
    Returns:
        QuantumCircuit: The complete circuit with initialization
    """
    qc = QuantumCircuit(3, name=f'Encoding from |{initial_state}⟩')
    
    # Initialize the first qubit to desired state
    if initial_state == '1':
        qc.x(0)  # Flip to |1⟩
    elif initial_state == '+':
        qc.h(0)  # Hadamard to create |+⟩ = (|0⟩ + |1⟩)/√2
    elif initial_state == '-':
        qc.x(0)
        qc.h(0)  # Create |-⟩ = (|0⟩ - |1⟩)/√2
    
    qc.barrier()  # Visual separator
    
    # Apply encoding
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    return qc


def visualize_circuit(qc, filename=None):
    """
    Visualizes the quantum circuit.
    
    Args:
        qc: QuantumCircuit to visualize
        filename: Optional filename to save the circuit diagram
    """
    print(f"\n{'='*60}")
    print(f"Circuit: {qc.name}")
    print('='*60)
    print(qc.draw(output='text'))
    
    if filename:
        try:
            fig = qc.draw(output='mpl', style={'backgroundcolor': '#FFFFFF'})
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✓ Circuit diagram saved to: {filename}")
        except Exception as e:
            print(f"\nNote: Could not save matplotlib figure: {e}")


def demonstrate_encoding():
    """
    Demonstrates the bit-flip encoding with different initial states.
    """
    print("\n" + "="*60)
    print("THREE-QUBIT BIT-FLIP ENCODING DEMONSTRATION")
    print("="*60)
    
    print("\n📖 Concept:")
    print("   Encoding maps: |ψ⟩ = α|0⟩ + β|1⟩")
    print("              to: α|000⟩ + β|111⟩")
    print("   This protects against single bit-flip errors!\n")
    
    # Basic encoding circuit
    print("\n1️⃣  Basic Encoding Circuit (no initialization)")
    basic_circuit = create_bit_flip_encoding_circuit()
    visualize_circuit(basic_circuit)
    
    # Encoding from |0⟩
    print("\n2️⃣  Encoding from |0⟩ state")
    circuit_0 = create_encoding_with_initial_state('0')
    visualize_circuit(circuit_0)
    print("   Result: |0⟩ → |000⟩")
    
    # Encoding from |1⟩
    print("\n3️⃣  Encoding from |1⟩ state")
    circuit_1 = create_encoding_with_initial_state('1')
    visualize_circuit(circuit_1)
    print("   Result: |1⟩ → |111⟩")
    
    # Encoding from |+⟩ (superposition)
    print("\n4️⃣  Encoding from |+⟩ state (superposition)")
    circuit_plus = create_encoding_with_initial_state('+')
    visualize_circuit(circuit_plus)
    print("   Result: |+⟩ = (|0⟩+|1⟩)/√2 → (|000⟩+|111⟩)/√2")
    
    print("\n" + "="*60)
    print("✓ Encoding circuits created successfully!")
    print("="*60)
    
    # Circuit statistics
    print(f"\n📊 Circuit Statistics:")
    print(f"   • Number of qubits: {basic_circuit.num_qubits}")
    print(f"   • Number of gates: {len(basic_circuit.data)}")
    print(f"   • Circuit depth: {basic_circuit.depth()}")
    print(f"   • Gate types: CNOT (2×)")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_encoding()
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("• Add bit-flip errors to test error correction")
    print("• Implement syndrome measurement")
    print("• Build the full decoding circuit")
    print("• Simulate error recovery")
    print("="*60 + "\n")

# majority_vote_detection.py
"""
Majority-Vote Error Detection Logic

This script implements the core error detection mechanism for the 3-qubit bit-flip code.
The majority-vote logic compares all three qubits and determines the correct value
based on what the majority (at least 2 out of 3) of qubits are.

Majority Vote Rules:
- If 2 or 3 qubits are |0⟩ → Majority is 0
- If 2 or 3 qubits are |1⟩ → Majority is 1
- This allows detection and correction of single bit-flip errors
"""

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer
from collections import Counter


def create_encoding_circuit_with_registers():
    """
    Creates encoding circuit with separate quantum and classical registers.
    
    Returns:
        QuantumCircuit: Circuit with named registers
    """
    # Create quantum and classical registers
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    
    qc = QuantumCircuit(qr, cr)
    
    # Encoding: duplicate q0 into q1 and q2
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    
    return qc


def add_error_and_measure(qc, error_qubit=None):
    """
    Adds optional error and measures all qubits.
    
    Args:
        qc: QuantumCircuit to modify
        error_qubit: Index of qubit to flip (0, 1, 2) or None
    
    Returns:
        QuantumCircuit: Modified circuit
    """
    if error_qubit is not None:
        qc.barrier(label='Error')
        qc.x(error_qubit)
    
    qc.barrier(label='Measure')
    
    # Measure all three qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc


def simulate_and_get_measurements(qc, shots=1000):
    """
    Simulates circuit and returns measurement results.
    
    Args:
        qc: QuantumCircuit to simulate
        shots: Number of measurement shots
    
    Returns:
        dict: Measurement counts
    """
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)
    
    return counts


def majority_vote(bit_string):
    """
    Implements majority-vote logic on a 3-bit string.
    
    Args:
        bit_string: String of 3 bits (e.g., '010', '111')
    
    Returns:
        tuple: (majority_bit, error_detected, error_position)
            - majority_bit: '0' or '1' (the majority value)
            - error_detected: Boolean indicating if an error was found
            - error_position: Index of the error (0, 1, 2) or None
    """
    if len(bit_string) != 3:
        raise ValueError("Bit string must be exactly 3 bits")
    
    # Count occurrences of '0' and '1'
    count_0 = bit_string.count('0')
    count_1 = bit_string.count('1')
    
    # Determine majority
    if count_0 > count_1:
        majority_bit = '0'
    else:
        majority_bit = '1'
    
    # Detect error: if not all bits match, there's an error
    error_detected = not (count_0 == 3 or count_1 == 3)
    
    # Find error position if error exists
    error_position = None
    if error_detected:
        # The minority bit is the error
        minority_bit = '1' if majority_bit == '0' else '0'
        error_position = bit_string.index(minority_bit)
    
    return majority_bit, error_detected, error_position


def analyze_measurement_results(counts):
    """
    Analyzes measurement results using majority-vote logic.
    
    Args:
        counts: Dictionary of measurement counts
    
    Returns:
        dict: Analysis results
    """
    results = {
        'total_shots': sum(counts.values()),
        'measurements': {}
    }
    
    for bit_string, count in counts.items():
        majority_bit, error_detected, error_position = majority_vote(bit_string)
        
        results['measurements'][bit_string] = {
            'count': count,
            'percentage': (count / results['total_shots']) * 100,
            'majority_bit': majority_bit,
            'error_detected': error_detected,
            'error_position': error_position
        }
    
    return results


def print_analysis(results, title="Majority Vote Analysis"):
    """
    Prints formatted analysis results.
    
    Args:
        results: Analysis results dictionary
        title: Title for the output
    """
    print(f"\n{'='*70}")
    print(f"{title}")
    print('='*70)
    print(f"Total shots: {results['total_shots']}\n")
    
    for bit_string, data in sorted(results['measurements'].items(), 
                                   key=lambda x: x[1]['count'], reverse=True):
        print(f"Measured: |{bit_string}⟩ ({data['count']} times, {data['percentage']:.1f}%)")
        print(f"  → Majority bit: {data['majority_bit']}")
        
        if data['error_detected']:
            print(f"  → ⚠️  ERROR DETECTED at position {data['error_position']}")
            print(f"     (Qubit {data['error_position']} differs from majority)")
        else:
            print(f"  → ✓ No error detected (all qubits agree)")
        print()


def demonstrate_majority_vote():
    """
    Demonstrates majority-vote error detection with various scenarios.
    """
    print("\n" + "="*70)
    print("MAJORITY-VOTE ERROR DETECTION DEMONSTRATION")
    print("="*70)
    
    print("\n📖 Concept:")
    print("   The majority-vote logic compares all 3 qubits:")
    print("   • If ≥2 qubits are |0⟩ → Majority is 0")
    print("   • If ≥2 qubits are |1⟩ → Majority is 1")
    print("   • Single bit-flip errors are detectable!\n")
    
    # Test cases
    test_cases = [
        ("No Error (|0⟩ encoded)", '0', None, "|000⟩"),
        ("Error on Qubit 0", '0', 0, "|001⟩"),
        ("Error on Qubit 1", '0', 1, "|010⟩"),
        ("Error on Qubit 2", '0', 2, "|100⟩"),
        ("No Error (|1⟩ encoded)", '1', None, "|111⟩"),
        ("Error on Qubit 1 (|1⟩ encoded)", '1', 1, "|101⟩"),
    ]
    
    for idx, (description, initial_state, error_qubit, expected) in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"{idx}️⃣  {description}")
        print(f"Expected output: {expected}")
        print('='*70)
        
        # Create circuit
        qc = QuantumCircuit(3, 3)
        
        # Initialize
        if initial_state == '1':
            qc.x(0)
        
        qc.barrier(label='Init')
        
        # Encode
        qc.cx(0, 1)
        qc.cx(0, 2)
        
        # Add error and measure
        qc = add_error_and_measure(qc, error_qubit)
        
        # Show circuit
        print(qc.draw(output='text', fold=-1))
        
        # Simulate
        counts = simulate_and_get_measurements(qc, shots=1000)
        
        # Analyze with majority vote
        results = analyze_measurement_results(counts)
        print_analysis(results, f"Results for: {description}")


def test_majority_vote_function():
    """
    Tests the majority_vote function with all possible 3-bit combinations.
    """
    print("\n" + "="*70)
    print("TESTING: majority_vote() Function")
    print("="*70)
    print("\nTesting all 8 possible 3-bit combinations:\n")
    
    test_strings = ['000', '001', '010', '011', '100', '101', '110', '111']
    
    print(f"{'Bit String':<12} {'Majority':<10} {'Error?':<10} {'Error Pos':<12} {'Interpretation'}")
    print("-" * 70)
    
    for bit_string in test_strings:
        majority, error_detected, error_pos = majority_vote(bit_string)
        error_str = "YES" if error_detected else "NO"
        pos_str = str(error_pos) if error_pos is not None else "N/A"
        
        # Interpretation
        if not error_detected:
            if majority == '0':
                interp = "Valid |000⟩ codeword"
            else:
                interp = "Valid |111⟩ codeword"
        else:
            interp = f"Error at q{error_pos}, should be {majority}"
        
        print(f"|{bit_string}⟩{' '*8} {majority}{' '*9} {error_str}{' '*7} {pos_str}{' '*11} {interp}")
    
    print("\n💡 Observations:")
    print("   • Only |000⟩ and |111⟩ are valid codewords (no error)")
    print("   • All other states indicate a single bit-flip error")
    print("   • The error position is uniquely identified")


def compare_classical_vs_quantum():
    """
    Compares classical majority vote with quantum measurement results.
    """
    print("\n" + "="*70)
    print("CLASSICAL vs QUANTUM: Majority Vote Comparison")
    print("="*70)
    
    print("\n🔍 Classical Majority Vote Logic:")
    print("   Given 3 classical bits, find the majority:")
    
    # Classical examples
    classical_examples = [
        ("000", "All 0s → Majority: 0, No error"),
        ("001", "Two 0s, one 1 → Majority: 0, Error at position 0"),
        ("101", "Two 1s, one 0 → Majority: 1, Error at position 1"),
        ("111", "All 1s → Majority: 1, No error"),
    ]
    
    for bits, explanation in classical_examples:
        majority, error_det, error_pos = majority_vote(bits)
        print(f"   {bits} → {explanation}")
    
    print("\n🔬 Quantum Implementation:")
    print("   After quantum encoding and measurement:")
    print("   1. Measure all 3 qubits → get classical bits")
    print("   2. Apply classical majority vote logic")
    print("   3. Identify error and determine correction")
    
    print("\n✨ Key Advantage:")
    print("   Quantum encoding creates redundancy that survives")
    print("   measurement, allowing classical error correction!")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_majority_vote()
    
    # Test the majority vote function
    test_majority_vote_function()
    
    # Compare classical vs quantum
    compare_classical_vs_quantum()
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("• Implement syndrome measurement circuit")
    print("• Build automatic correction logic")
    print("• Create full error correction pipeline")
    print("• Test with random errors")
    print("="*70 + "\n")

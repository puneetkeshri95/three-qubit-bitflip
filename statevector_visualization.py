# statevector_visualization.py
"""
Statevector Visualization - Before & After Error Correction

This script uses Qiskit's Statevector simulator to visualize how the quantum
state evolves through the error correction pipeline:
1. Initial state
2. After encoding
3. After error introduction
4. After correction

This provides deep insight into the quantum mechanics of error correction.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
from typing import List, Tuple, Dict


def format_complex(value: complex, precision: int = 4) -> str:
    """
    Format complex number for display.
    
    Args:
        value: Complex number
        precision: Decimal precision
        
    Returns:
        Formatted string
    """
    real = np.real(value)
    imag = np.imag(value)
    
    # Handle very small values
    if abs(real) < 1e-10:
        real = 0.0
    if abs(imag) < 1e-10:
        imag = 0.0
    
    if imag == 0:
        return f"{real:.{precision}f}"
    elif real == 0:
        if imag == 1:
            return "i"
        elif imag == -1:
            return "-i"
        return f"{imag:.{precision}f}i"
    else:
        sign = "+" if imag >= 0 else ""
        return f"{real:.{precision}f}{sign}{imag:.{precision}f}i"


def get_statevector_dict(statevector: Statevector, 
                        threshold: float = 1e-10) -> Dict[str, complex]:
    """
    Convert statevector to dictionary with non-zero amplitudes.
    
    Args:
        statevector: Qiskit Statevector
        threshold: Minimum amplitude to display
        
    Returns:
        Dictionary mapping basis states to amplitudes
    """
    state_dict = {}
    num_qubits = statevector.num_qubits
    
    for i in range(2**num_qubits):
        amplitude = statevector.data[i]
        if abs(amplitude) > threshold:
            # Convert index to binary string
            basis_state = format(i, f'0{num_qubits}b')
            state_dict[basis_state] = amplitude
    
    return state_dict


def print_statevector(statevector: Statevector, title: str = "Statevector"):
    """
    Print statevector in readable format.
    
    Args:
        statevector: Qiskit Statevector
        title: Title for the display
    """
    print(f"\n{'='*70}")
    print(f"{title}")
    print('='*70)
    
    state_dict = get_statevector_dict(statevector)
    
    if not state_dict:
        print("  |000⟩ (all zeros)")
        return
    
    # Build state representation
    terms = []
    for basis_state, amplitude in sorted(state_dict.items()):
        coeff = format_complex(amplitude, precision=4)
        
        # Simplify common coefficients
        if coeff == "0.7071":
            coeff = "1/√2"
        elif coeff == "-0.7071":
            coeff = "-1/√2"
        elif coeff == "1.0000":
            coeff = ""
        elif coeff == "-1.0000":
            coeff = "-"
        
        if coeff and coeff != "-":
            terms.append(f"{coeff}|{basis_state}⟩")
        elif coeff == "-":
            terms.append(f"-|{basis_state}⟩")
        else:
            terms.append(f"|{basis_state}⟩")
    
    # Print the state
    state_str = " + ".join(terms)
    state_str = state_str.replace(" + -", " - ")
    
    print(f"\n  |ψ⟩ = {state_str}")
    
    # Print probability distribution
    print(f"\n  Probability Amplitudes:")
    for basis_state, amplitude in sorted(state_dict.items()):
        probability = abs(amplitude)**2
        print(f"    |{basis_state}⟩: {format_complex(amplitude):>20} "
              f"(prob: {probability:.4f})")
    
    print('='*70)


def visualize_encoding_process(initial_state: str = '0'):
    """
    Visualizes statevector during encoding process.
    
    Args:
        initial_state: '0', '1', '+', or '-'
    """
    print("\n" + "="*70)
    print("ENCODING PROCESS - STATEVECTOR EVOLUTION")
    print("="*70)
    print(f"\nInitial logical state: |{initial_state}⟩")
    
    # Step 1: Initial state (1 qubit, then pad to 3)
    print("\n" + "-"*70)
    print("STEP 1: Initial State")
    print("-"*70)
    
    qc_init = QuantumCircuit(3)
    
    if initial_state == '1':
        qc_init.x(0)
    elif initial_state == '+':
        qc_init.h(0)
    elif initial_state == '-':
        qc_init.x(0)
        qc_init.h(0)
    
    sv_initial = Statevector.from_instruction(qc_init)
    print_statevector(sv_initial, f"Initial State: |{initial_state}⟩⊗|0⟩⊗|0⟩")
    
    # Step 2: After encoding
    print("\n" + "-"*70)
    print("STEP 2: After Encoding (CNOT gates)")
    print("-"*70)
    
    qc_encoded = QuantumCircuit(3)
    
    if initial_state == '1':
        qc_encoded.x(0)
    elif initial_state == '+':
        qc_encoded.h(0)
    elif initial_state == '-':
        qc_encoded.x(0)
        qc_encoded.h(0)
    
    qc_encoded.cx(0, 1)
    qc_encoded.cx(0, 2)
    
    sv_encoded = Statevector.from_instruction(qc_encoded)
    print_statevector(sv_encoded, "Encoded State")
    
    print("\n💡 Observation:")
    if initial_state == '0':
        print("   |0⟩ → |000⟩ (all qubits in state 0)")
    elif initial_state == '1':
        print("   |1⟩ → |111⟩ (all qubits in state 1)")
    elif initial_state == '+':
        print("   |+⟩ → (|000⟩+|111⟩)/√2 (entangled state)")


def visualize_error_and_correction(initial_state: str = '0', 
                                   error_qubit: int = 1):
    """
    Visualizes complete error correction pipeline with statevectors.
    
    Args:
        initial_state: '0' or '1'
        error_qubit: Which qubit to flip (0, 1, or 2)
    """
    print("\n" + "="*70)
    print("COMPLETE ERROR CORRECTION - STATEVECTOR ANALYSIS")
    print("="*70)
    print(f"\nScenario: Encode |{initial_state}⟩ with error on qubit {error_qubit}")
    
    # Step 1: Initial + Encoding
    print("\n" + "-"*70)
    print("STEP 1: Initial State + Encoding")
    print("-"*70)
    
    qc = QuantumCircuit(3)
    
    if initial_state == '1':
        qc.x(0)
    
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    sv_encoded = Statevector.from_instruction(qc)
    print_statevector(sv_encoded, "After Encoding")
    
    # Step 2: After error
    print("\n" + "-"*70)
    print(f"STEP 2: After Bit-Flip Error on Qubit {error_qubit}")
    print("-"*70)
    
    qc.x(error_qubit)
    
    sv_error = Statevector.from_instruction(qc)
    print_statevector(sv_error, f"After Error (X gate on q{error_qubit})")
    
    print("\n⚠️  Error Effect:")
    expected = '000' if initial_state == '0' else '111'
    error_state = list(expected)
    error_state[2-error_qubit] = '1' if error_state[2-error_qubit] == '0' else '0'
    error_state = ''.join(error_state)
    print(f"   Original: |{expected}⟩")
    print(f"   Corrupted: |{error_state}⟩")
    print(f"   One qubit has flipped!")
    
    # Step 3: After correction
    print("\n" + "-"*70)
    print(f"STEP 3: After Correction (X gate on q{error_qubit})")
    print("-"*70)
    
    qc.x(error_qubit)  # Apply correction
    
    sv_corrected = Statevector.from_instruction(qc)
    print_statevector(sv_corrected, "After Correction")
    
    print("\n✅ Correction Result:")
    print(f"   State restored to: |{expected}⟩")
    print(f"   Error successfully corrected!")


def compare_states(sv1: Statevector, sv2: Statevector, 
                  label1: str, label2: str) -> float:
    """
    Compare two statevectors and show differences.
    
    Args:
        sv1: First statevector
        sv2: Second statevector
        label1: Label for first state
        label2: Label for second state
        
    Returns:
        Fidelity between states
    """
    print("\n" + "="*70)
    print("STATE COMPARISON")
    print("="*70)
    
    # Calculate fidelity
    fidelity = abs(sv1.inner(sv2))**2
    
    print(f"\n{label1}:")
    dict1 = get_statevector_dict(sv1)
    for state, amp in sorted(dict1.items()):
        prob = abs(amp)**2
        print(f"  |{state}⟩: {format_complex(amp):>20} (prob: {prob:.4f})")
    
    print(f"\n{label2}:")
    dict2 = get_statevector_dict(sv2)
    for state, amp in sorted(dict2.items()):
        prob = abs(amp)**2
        print(f"  |{state}⟩: {format_complex(amp):>20} (prob: {prob:.4f})")
    
    print(f"\n📊 Fidelity: {fidelity:.6f}")
    
    if fidelity > 0.9999:
        print("   ✅ States are identical (perfect correction)")
    elif fidelity > 0.99:
        print("   ✓ States are very similar")
    else:
        print("   ⚠️  States differ significantly")
    
    return fidelity


def demonstrate_all_error_positions(initial_state: str = '0'):
    """
    Shows statevector for errors on all three qubits.
    
    Args:
        initial_state: '0' or '1'
    """
    print("\n" + "="*70)
    print("ERROR POSITION COMPARISON")
    print("="*70)
    print(f"\nInitial state: |{initial_state}⟩")
    
    expected = '000' if initial_state == '0' else '111'
    
    # Get encoded state
    qc_encoded = QuantumCircuit(3)
    if initial_state == '1':
        qc_encoded.x(0)
    qc_encoded.cx(0, 1)
    qc_encoded.cx(0, 2)
    sv_encoded = Statevector.from_instruction(qc_encoded)
    
    print("\n" + "-"*70)
    print("Encoded State (no error)")
    print("-"*70)
    print_statevector(sv_encoded, f"Encoded: |{expected}⟩")
    
    # Show each error position
    for error_qubit in range(3):
        print("\n" + "-"*70)
        print(f"Error on Qubit {error_qubit}")
        print("-"*70)
        
        qc_error = QuantumCircuit(3)
        if initial_state == '1':
            qc_error.x(0)
        qc_error.cx(0, 1)
        qc_error.cx(0, 2)
        qc_error.x(error_qubit)
        
        sv_error = Statevector.from_instruction(qc_error)
        print_statevector(sv_error, f"With error on q{error_qubit}")


def visualize_superposition_correction():
    """
    Demonstrates error correction on superposition states.
    """
    print("\n" + "="*70)
    print("SUPERPOSITION STATE ERROR CORRECTION")
    print("="*70)
    print("\nInitial state: |+⟩ = (|0⟩+|1⟩)/√2")
    
    # Step 1: Encoded superposition
    print("\n" + "-"*70)
    print("STEP 1: Encoded Superposition")
    print("-"*70)
    
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    sv_encoded = Statevector.from_instruction(qc)
    print_statevector(sv_encoded, "Encoded |+⟩")
    
    print("\n💡 Key Insight:")
    print("   The superposition is preserved in encoded form:")
    print("   (|000⟩+|111⟩)/√2")
    
    # Step 2: Error on qubit 1
    print("\n" + "-"*70)
    print("STEP 2: Error on Qubit 1")
    print("-"*70)
    
    qc.x(1)
    sv_error = Statevector.from_instruction(qc)
    print_statevector(sv_error, "After error on q1")
    
    # Step 3: Correction
    print("\n" + "-"*70)
    print("STEP 3: Correction Applied")
    print("-"*70)
    
    qc.x(1)
    sv_corrected = Statevector.from_instruction(qc)
    print_statevector(sv_corrected, "After correction")
    
    print("\n✨ Result:")
    print("   Superposition restored perfectly!")
    print("   Error correction works for quantum superpositions!")
    
    # Compare fidelity
    compare_states(sv_encoded, sv_corrected, 
                  "Original encoded state", 
                  "After error + correction")


def demonstrate_phase_information():
    """
    Shows that relative phases are preserved.
    """
    print("\n" + "="*70)
    print("PHASE PRESERVATION ANALYSIS")
    print("="*70)
    
    print("\n📐 Testing with |-⟩ state (has relative phase)")
    print("   |-⟩ = (|0⟩-|1⟩)/√2")
    
    # Encode |-⟩
    qc = QuantumCircuit(3)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    sv_encoded = Statevector.from_instruction(qc)
    print_statevector(sv_encoded, "Encoded |-⟩")
    
    # Add error and correct
    qc.x(2)  # Error on q2
    qc.x(2)  # Correction
    
    sv_corrected = Statevector.from_instruction(qc)
    print_statevector(sv_corrected, "After error + correction")
    
    # Check fidelity
    fidelity = compare_states(sv_encoded, sv_corrected,
                             "Original encoded |-⟩",
                             "After correction")
    
    if fidelity > 0.9999:
        print("\n✅ Relative phase preserved!")
        print("   The minus sign in (|000⟩-|111⟩)/√2 is maintained")


def main():
    """
    Main demonstration function.
    """
    print("\n" + "="*70)
    print("STATEVECTOR VISUALIZATION - ERROR CORRECTION ANALYSIS")
    print("="*70)
    print("\n📊 Using Qiskit Statevector Simulator")
    print("   This provides exact quantum state information")
    print("   (not possible on real quantum hardware!)")
    
    # Demo 1: Encoding process
    print("\n\n" + "🔷"*35)
    print("DEMO 1: Encoding Process")
    print("🔷"*35)
    visualize_encoding_process(initial_state='0')
    
    input("\n➡️  Press Enter to continue...")
    
    # Demo 2: Complete correction pipeline
    print("\n\n" + "🔷"*35)
    print("DEMO 2: Complete Error Correction Pipeline")
    print("🔷"*35)
    visualize_error_and_correction(initial_state='0', error_qubit=1)
    
    input("\n➡️  Press Enter to continue...")
    
    # Demo 3: All error positions
    print("\n\n" + "🔷"*35)
    print("DEMO 3: Errors on Different Qubits")
    print("🔷"*35)
    demonstrate_all_error_positions(initial_state='0')
    
    input("\n➡️  Press Enter to continue...")
    
    # Demo 4: Superposition correction
    print("\n\n" + "🔷"*35)
    print("DEMO 4: Superposition State Correction")
    print("🔷"*35)
    visualize_superposition_correction()
    
    input("\n➡️  Press Enter to continue...")
    
    # Demo 5: Phase preservation
    print("\n\n" + "🔷"*35)
    print("DEMO 5: Phase Preservation")
    print("🔷"*35)
    demonstrate_phase_information()
    
    # Final summary
    print("\n\n" + "="*70)
    print("✅ STATEVECTOR ANALYSIS COMPLETE")
    print("="*70)
    
    print("\n🎯 Key Learnings:")
    print("   ✓ Encoding creates entangled states (|000⟩ or |111⟩)")
    print("   ✓ Errors corrupt the quantum state")
    print("   ✓ Correction restores the original state perfectly")
    print("   ✓ Superposition states are preserved")
    print("   ✓ Relative phases are maintained")
    
    print("\n💡 Important Notes:")
    print("   • Statevector simulation shows exact quantum state")
    print("   • Real quantum hardware only gives measurement results")
    print("   • This visualization helps understand quantum mechanics")
    print("   • Error correction preserves quantum information")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Visualization interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

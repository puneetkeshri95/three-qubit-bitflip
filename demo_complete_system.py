# demo_complete_system.py
"""
Complete 3-Qubit Bit-Flip Error Correction - Interactive Demo

This script provides an interactive demonstration of the complete
quantum error correction system with visual explanations and comparisons.
"""

from full_error_correction_pipeline import BitFlipErrorCorrection
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile
import random


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70)


def print_section(title):
    """Print a section divider."""
    print("\n" + "-"*70)
    print(title)
    print("-"*70)


def demo_introduction():
    """Introduces the quantum error correction concept."""
    print_header("3-QUBIT BIT-FLIP ERROR CORRECTION SYSTEM")
    
    print("\n📚 What is Quantum Error Correction?")
    print("\nQuantum computers are extremely sensitive to errors. Even tiny")
    print("disturbances can cause qubits to flip from |0⟩ to |1⟩ or vice versa.")
    print("This is called a 'bit-flip error'.")
    
    print("\n🛡️ The Solution: Quantum Error Correction")
    print("\nWe protect quantum information by encoding it redundantly:")
    print("• 1 logical qubit → 3 physical qubits")
    print("• |0⟩ becomes |000⟩")
    print("• |1⟩ becomes |111⟩")
    
    print("\n🔍 Error Detection & Correction:")
    print("• If one qubit flips, we can detect which one")
    print("• Use majority-vote: 2 out of 3 qubits determine the correct value")
    print("• Apply correction to restore the original state")
    
    print("\n✨ Result: Protection against single bit-flip errors!")
    
    input("\n➡️  Press Enter to see the demonstration...")


def demo_encoding():
    """Demonstrates the encoding process."""
    print_header("STEP 1: ENCODING")
    
    print("\n🔧 Encoding Process:")
    print("   Input:  Single qubit in state |ψ⟩ = α|0⟩ + β|1⟩")
    print("   Output: Three qubits in state α|000⟩ + β|111⟩")
    
    print("\n📋 Example: Encoding |0⟩")
    print("   |0⟩ on q0 → Apply CNOT(0,1) → Apply CNOT(0,2) → |000⟩")
    
    # Show encoding circuit
    qc = QuantumCircuit(3)
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    print("\n🔌 Encoding Circuit:")
    print(qc.draw(output='text'))
    
    print("\n✓ The quantum information is now protected by redundancy!")
    
    input("\n➡️  Press Enter to continue...")


def demo_error_introduction():
    """Demonstrates error introduction."""
    print_header("STEP 2: ERROR SIMULATION")
    
    print("\n⚠️  Simulating Real-World Errors:")
    print("   In real quantum computers, errors occur due to:")
    print("   • Environmental noise")
    print("   • Imperfect quantum gates")
    print("   • Decoherence")
    
    print("\n🎲 We simulate this by randomly applying an X gate (bit-flip)")
    print("   to one of the three qubits.")
    
    print("\n📊 Possible Error Scenarios:")
    scenarios = [
        ("|000⟩", "→", "|001⟩", "(error on q0)"),
        ("|000⟩", "→", "|010⟩", "(error on q1)"),
        ("|000⟩", "→", "|100⟩", "(error on q2)"),
    ]
    
    for before, arrow, after, desc in scenarios:
        print(f"   {before} {arrow} {after} {desc}")
    
    input("\n➡️  Press Enter to continue...")


def demo_detection():
    """Demonstrates error detection."""
    print_header("STEP 3: ERROR DETECTION")
    
    print("\n🔍 Majority-Vote Logic:")
    print("   After measuring all 3 qubits, we compare their values:")
    
    print("\n📋 Examples:")
    examples = [
        ("|000⟩", "All 0s", "✓ No error detected"),
        ("|001⟩", "Two 0s, one 1", "⚠️  Error on qubit 0 (q0 is the 1)"),
        ("|010⟩", "Two 0s, one 1", "⚠️  Error on qubit 1 (q1 is the 1)"),
        ("|100⟩", "Two 0s, one 1", "⚠️  Error on qubit 2 (q2 is the 1)"),
        ("|111⟩", "All 1s", "✓ No error detected"),
        ("|101⟩", "Two 1s, one 0", "⚠️  Error on qubit 1 (q1 is the 0)"),
    ]
    
    for state, description, result in examples:
        print(f"   {state}: {description:<18} → {result}")
    
    print("\n💡 Key Insight:")
    print("   The minority bit reveals which qubit has the error!")
    
    input("\n➡️  Press Enter to continue...")


def demo_correction():
    """Demonstrates error correction."""
    print_header("STEP 4: ERROR CORRECTION")
    
    print("\n🔧 Applying Correction:")
    print("   Once we identify the faulty qubit, we fix it by")
    print("   applying an X gate (bit-flip) to that qubit.")
    
    print("\n📋 Example: Error on qubit 1")
    print("   Measured: |010⟩")
    print("   Detected: Error at position 1 (minority is at q1)")
    print("   Action:   Apply X gate to qubit 1")
    print("   Result:   |010⟩ → |000⟩ ✓")
    
    print("\n✨ The quantum state is restored!")
    
    input("\n➡️  Press Enter to see a live demonstration...")


def demo_live_correction():
    """Runs a live correction demonstration."""
    print_header("LIVE DEMONSTRATION")
    
    # Test cases
    test_cases = [
        ("Test 1", '0', 0, "|0⟩ with error on q0"),
        ("Test 2", '0', 1, "|0⟩ with error on q1"),
        ("Test 3", '1', 2, "|1⟩ with error on q2"),
    ]
    
    for test_name, initial_state, error_qubit, description in test_cases:
        print_section(f"{test_name}: {description}")
        
        pipeline = BitFlipErrorCorrection(initial_state=initial_state, verbose=True)
        results = pipeline.run_pipeline(shots=100, error_qubit=error_qubit)
        
        if results['success_rate'] == 100.0:
            print("\n✅ SUCCESS: Error corrected perfectly!")
        else:
            print(f"\n⚠️  Partial success: {results['success_rate']:.1f}%")
        
        input("\n➡️  Press Enter for next test...")


def demo_statistics():
    """Shows statistical performance."""
    print_header("STATISTICAL PERFORMANCE")
    
    print("\n📊 Running 50 random tests to measure reliability...")
    print("(Testing various initial states and random error positions)\n")
    
    success_count = 0
    total_tests = 50
    
    for i in range(total_tests):
        initial_state = random.choice(['0', '1'])
        error_qubit = random.randint(0, 2)
        
        pipeline = BitFlipErrorCorrection(initial_state=initial_state, verbose=False)
        results = pipeline.run_pipeline(shots=100, error_qubit=error_qubit)
        
        if results['success_rate'] >= 99.0:
            success_count += 1
            symbol = "✓"
        else:
            symbol = "✗"
        
        if (i + 1) % 10 == 0:
            print(f"Tests {i-8:2d}-{i+1:2d}: {symbol*10}")
    
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n{'='*70}")
    print(f"RESULTS: {success_count}/{total_tests} tests successful")
    print(f"Overall Success Rate: {success_rate:.0f}%")
    print('='*70)
    
    if success_rate >= 95:
        print("\n🎉 EXCELLENT: The error correction system is highly reliable!")
    
    input("\n➡️  Press Enter to continue...")


def demo_comparison():
    """Compares with and without correction."""
    print_header("IMPACT DEMONSTRATION")
    
    print("\n🔬 Let's compare what happens with and without error correction")
    print("   when a bit-flip error occurs...\n")
    
    # Without correction
    print_section("WITHOUT Error Correction")
    print("Scenario: Encode |0⟩, error occurs on q1")
    
    qc_no_corr = QuantumCircuit(3, 3)
    qc_no_corr.cx(0, 1)
    qc_no_corr.cx(0, 2)
    qc_no_corr.barrier()
    qc_no_corr.x(1)  # Error
    qc_no_corr.barrier()
    qc_no_corr.measure([0, 1, 2], [0, 1, 2])
    
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(transpile(qc_no_corr, simulator), shots=100)
    counts_no_corr = job.result().get_counts()
    
    print(f"Result: {list(counts_no_corr.keys())[0]}")
    print("❌ ERROR PERSISTS: The quantum information is corrupted!")
    
    # With correction
    print_section("WITH Error Correction")
    print("Same scenario: Encode |0⟩, error on q1, but now we correct it")
    
    pipeline = BitFlipErrorCorrection(initial_state='0', verbose=False)
    results = pipeline.run_pipeline(shots=100, error_qubit=1)
    
    print(f"Result: {list(results['counts'].keys())[0]}")
    print("✅ ERROR CORRECTED: The quantum information is restored!")
    
    print("\n💡 Conclusion:")
    print("   Without correction: Information is lost")
    print("   With correction: Information is preserved")
    
    input("\n➡️  Press Enter to finish...")


def demo_conclusion():
    """Concludes the demonstration."""
    print_header("SUMMARY & CONCLUSIONS")
    
    print("\n🎯 What We've Learned:")
    print("   ✓ Quantum error correction protects quantum information")
    print("   ✓ Redundancy (1 → 3 qubits) enables error detection")
    print("   ✓ Majority-vote logic identifies the faulty qubit")
    print("   ✓ Corrective X gates restore the original state")
    print("   ✓ Single bit-flip errors can be corrected with ~100% success")
    
    print("\n🔬 Technical Implementation:")
    print("   • Encoding: Two CNOT gates")
    print("   • Detection: Syndrome measurement + majority-vote")
    print("   • Correction: Conditional X gate application")
    print("   • Verification: Final state measurement")
    
    print("\n🌟 Real-World Impact:")
    print("   • Essential for fault-tolerant quantum computing")
    print("   • Enables longer quantum computations")
    print("   • Protects quantum communication channels")
    print("   • Foundation for more advanced error correction codes")
    
    print("\n📚 Advanced Topics (Future Extensions):")
    print("   • Phase-flip errors (Shor code)")
    print("   • Stabilizer codes")
    print("   • Surface codes (2D error correction)")
    print("   • Topological quantum computing")
    
    print("\n" + "="*70)
    print("Thank you for exploring Quantum Error Correction!".center(70))
    print("="*70 + "\n")


def run_interactive_demo():
    """Runs the complete interactive demonstration."""
    demo_introduction()
    demo_encoding()
    demo_error_introduction()
    demo_detection()
    demo_correction()
    demo_live_correction()
    demo_statistics()
    demo_comparison()
    demo_conclusion()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("WELCOME TO THE QUANTUM ERROR CORRECTION DEMO".center(70))
    print("="*70)
    print("\nThis interactive demonstration will guide you through")
    print("the complete 3-qubit bit-flip error correction system.")
    print("\nPress Ctrl+C at any time to exit.")
    
    input("\n➡️  Press Enter to start...")
    
    try:
        run_interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
    
    print("\n✨ Demo complete! Check out the other Python files for")
    print("   detailed implementations of each component.\n")

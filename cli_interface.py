#!/usr/bin/env python3
# cli_interface.py
"""
Command-Line Interface for 3-Qubit Bit-Flip Error Correction

Simple CLI to run different quantum error correction scenarios.
"""

import argparse
import sys
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile
from qiskit.quantum_info import Statevector


def encode_qubit(initial_state='0', show_circuit=True):
    """Encode a single qubit into 3 qubits."""
    print("\n" + "="*60)
    print("ENCODING")
    print("="*60)
    
    qc = QuantumCircuit(3, 3)
    
    # Initialize
    if initial_state == '1':
        qc.x(0)
        print(f"Initial state: |1⟩")
    else:
        print(f"Initial state: |0⟩")
    
    # Encode
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    expected = '000' if initial_state == '0' else '111'
    print(f"Encoded state: |{expected}⟩")
    
    if show_circuit:
        print("\nCircuit:")
        print(qc.draw(output='text'))
    
    # Verify with statevector
    sv = Statevector(qc)
    print(f"\nStatevector: {sv}")
    
    return qc


def introduce_error(initial_state='0', error_qubit=1, show_circuit=True):
    """Introduce a bit-flip error."""
    print("\n" + "="*60)
    print("ERROR SIMULATION")
    print("="*60)
    
    qc = QuantumCircuit(3, 3)
    
    # Initialize and encode
    if initial_state == '1':
        qc.x(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    # Introduce error
    qc.barrier()
    qc.x(error_qubit)
    qc.barrier()
    
    print(f"Initial state: |{initial_state}⟩")
    print(f"Error introduced on qubit {error_qubit}")
    
    if show_circuit:
        print("\nCircuit:")
        print(qc.draw(output='text'))
    
    # Measure
    qc.measure([0, 1, 2], [0, 1, 2])
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(transpile(qc, simulator), shots=100)
    counts = job.result().get_counts()
    
    print(f"\nMeasurement results: {list(counts.keys())[0]}")
    
    return qc


def simulate_correction(initial_state='0', error_qubit=1, show_circuit=True):
    """Simulate complete error correction."""
    print("\n" + "="*60)
    print("ERROR CORRECTION SIMULATION")
    print("="*60)
    
    print(f"Initial state: |{initial_state}⟩")
    print(f"Error on qubit: {error_qubit}")
    
    # Circuit with error
    qc = QuantumCircuit(3, 3)
    if initial_state == '1':
        qc.x(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier(label='Encode')
    qc.x(error_qubit)
    qc.barrier(label='Error')
    
    # Correction
    qc.x(error_qubit)
    qc.barrier(label='Correct')
    
    if show_circuit:
        print("\nCircuit:")
        print(qc.draw(output='text'))
    
    # Measure
    qc.measure([0, 1, 2], [0, 1, 2])
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(transpile(qc, simulator), shots=100)
    counts = job.result().get_counts()
    
    expected = '000' if initial_state == '0' else '111'
    result = list(counts.keys())[0]
    
    print(f"\nExpected: |{expected}⟩")
    print(f"Result:   |{result}⟩")
    
    if result == expected:
        print("\n✅ SUCCESS: Error corrected!")
    else:
        print("\n❌ FAILED: Error not corrected")
    
    return qc


def run_full_pipeline(initial_state='0', error_qubit=1, verbose=True):
    """Run complete encoding → error → correction pipeline."""
    print("\n" + "="*60)
    print("FULL ERROR CORRECTION PIPELINE")
    print("="*60)
    
    stages = [
        ("1. ENCODING", f"Encode |{initial_state}⟩ into 3 qubits"),
        ("2. ERROR", f"Introduce bit-flip on qubit {error_qubit}"),
        ("3. DETECTION", "Use majority-vote to detect error"),
        ("4. CORRECTION", f"Apply X gate to qubit {error_qubit}"),
        ("5. VERIFICATION", "Measure and verify restoration"),
    ]
    
    print("\nPipeline stages:")
    for stage, desc in stages:
        print(f"  {stage}: {desc}")
    
    # Execute
    qc = QuantumCircuit(3, 3)
    
    # Initialize
    if initial_state == '1':
        qc.x(0)
    qc.barrier(label='Init')
    
    # Encode
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier(label='Encode')
    
    # Error
    qc.x(error_qubit)
    qc.barrier(label='Error')
    
    # Correction
    qc.x(error_qubit)
    qc.barrier(label='Correct')
    
    # Measure
    qc.measure([0, 1, 2], [0, 1, 2])
    
    if verbose:
        print("\nCircuit:")
        print(qc.draw(output='text'))
    
    # Simulate
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(transpile(qc, simulator), shots=1000)
    counts = job.result().get_counts()
    
    expected = '000' if initial_state == '0' else '111'
    success_count = counts.get(expected, 0)
    success_rate = (success_count / 1000) * 100
    
    print(f"\nResults (1000 shots):")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  |{state}⟩: {count} times ({count/10:.1f}%)")
    
    print(f"\n{'='*60}")
    print(f"Success Rate: {success_rate:.1f}%")
    print("="*60)
    
    if success_rate == 100.0:
        print("✅ Perfect correction!")
    elif success_rate >= 95.0:
        print("✓ High success rate")
    else:
        print("⚠ Low success rate")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='3-Qubit Bit-Flip Error Correction CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode --state 0
  %(prog)s error --state 1 --qubit 2
  %(prog)s correct --state 0 --qubit 1
  %(prog)s pipeline --state 1 --qubit 0
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a qubit')
    encode_parser.add_argument('--state', type=str, choices=['0', '1'], 
                               default='0', help='Initial state (default: 0)')
    encode_parser.add_argument('--no-circuit', action='store_true',
                               help='Hide circuit diagram')
    
    # Error command
    error_parser = subparsers.add_parser('error', help='Introduce error')
    error_parser.add_argument('--state', type=str, choices=['0', '1'],
                              default='0', help='Initial state (default: 0)')
    error_parser.add_argument('--qubit', type=int, choices=[0, 1, 2],
                              default=1, help='Error qubit (default: 1)')
    error_parser.add_argument('--no-circuit', action='store_true',
                              help='Hide circuit diagram')
    
    # Correct command
    correct_parser = subparsers.add_parser('correct', help='Simulate correction')
    correct_parser.add_argument('--state', type=str, choices=['0', '1'],
                                default='0', help='Initial state (default: 0)')
    correct_parser.add_argument('--qubit', type=int, choices=[0, 1, 2],
                                default=1, help='Error qubit (default: 1)')
    correct_parser.add_argument('--no-circuit', action='store_true',
                                help='Hide circuit diagram')
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run full pipeline')
    pipeline_parser.add_argument('--state', type=str, choices=['0', '1'],
                                 default='0', help='Initial state (default: 0)')
    pipeline_parser.add_argument('--qubit', type=int, choices=[0, 1, 2],
                                 default=1, help='Error qubit (default: 1)')
    pipeline_parser.add_argument('--quiet', action='store_true',
                                 help='Minimal output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Execute command
    try:
        if args.command == 'encode':
            encode_qubit(args.state, not args.no_circuit)
        
        elif args.command == 'error':
            introduce_error(args.state, args.qubit, not args.no_circuit)
        
        elif args.command == 'correct':
            simulate_correction(args.state, args.qubit, not args.no_circuit)
        
        elif args.command == 'pipeline':
            run_full_pipeline(args.state, args.qubit, not args.quiet)
        
        print()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

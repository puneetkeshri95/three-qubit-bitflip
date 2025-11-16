# flask_backend.py
"""
Flask Backend for 3-Qubit Bit-Flip Error Correction

RESTful API server that runs quantum error correction jobs.
Endpoints for encoding, error simulation, and correction.
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from werkzeug.utils import secure_filename
import json
import os
import random
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for frontend

# Configure upload settings for Local Blob API
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'json', 'qasm', 'py', 'png', 'jpg', 'jpeg', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simulator backend
simulator = Aer.get_backend('qasm_simulator')


@app.route('/')
def home():
    """Serve the main HTML interface."""
    return send_from_directory('.', 'index.html')


@app.route('/api')
def api_docs():
    """API documentation."""
    return jsonify({
        'name': '3-Qubit Bit-Flip Error Correction API',
        'version': '2.0',
        'description': 'Complete Flask API with Local Blob Storage for quantum error correction',
        'endpoints': {
            'quantum_operations': {
                '/encode': {
                    'method': 'POST',
                    'description': 'Encode a single qubit into 3 qubits',
                    'input': {'state': '0 or 1'},
                    'output': 'Encoded state and circuit'
                },
                '/error': {
                    'method': 'POST',
                    'description': 'Introduce bit-flip error on specified qubit',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Measurements after error'
                },
                '/add_error': {
                    'method': 'POST',
                    'description': 'Add error (alias for /error)',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Measurements after error'
                },
                '/error/random': {
                    'method': 'POST',
                    'description': 'Introduce random bit-flip error',
                    'input': {'state': '0 or 1'},
                    'output': 'Measurements with randomly selected error qubit'
                },
                '/correct': {
                    'method': 'POST',
                    'description': 'Simulate error correction',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Correction results and success rate'
                },
                '/correct_error': {
                    'method': 'POST',
                    'description': 'Correct error (alias for /correct)',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Correction results and success rate'
                },
                '/pipeline': {
                    'method': 'POST',
                    'description': 'Run full error correction pipeline',
                    'input': {'state': '0 or 1', 'error_qubit': '0-2', 'random_error': 'bool', 'shots': 'int'},
                    'output': 'Complete pipeline results with measurements'
                },
                '/statevector': {
                    'method': 'POST',
                    'description': 'Get statevector analysis at each stage',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Probability distributions for all stages'
                },
                '/visualize_circuit': {
                    'method': 'POST',
                    'description': 'Generate circuit visualization with metadata',
                    'input': {'state': '0 or 1', 'error_qubit': '0, 1, or 2'},
                    'output': 'Circuit drawing, depth, gate count'
                }
            },
            'blob_api': {
                '/upload': {
                    'method': 'POST',
                    'description': 'Upload file to server (Local Blob API)',
                    'input': 'multipart/form-data with file',
                    'output': 'Upload confirmation with download URL',
                    'max_size': '16 MB',
                    'allowed_types': list(ALLOWED_EXTENSIONS)
                },
                '/download/<filename>': {
                    'method': 'GET',
                    'description': 'Download file from server',
                    'input': 'filename in URL',
                    'output': 'File download'
                },
                '/files': {
                    'method': 'GET',
                    'description': 'List all uploaded files with metadata',
                    'input': 'None',
                    'output': 'Array of file objects with details'
                },
                '/delete/<filename>': {
                    'method': 'DELETE',
                    'description': 'Delete file from server',
                    'input': 'filename in URL',
                    'output': 'Deletion confirmation'
                }
            },
            'system': {
                '/health': {
                    'method': 'GET',
                    'description': 'Health check endpoint',
                    'output': 'Service status'
                },
                '/api': {
                    'method': 'GET',
                    'description': 'This documentation',
                    'output': 'Complete API reference'
                }
            }
        },
        'configuration': {
            'upload_folder': UPLOAD_FOLDER,
            'max_upload_size': f"{MAX_CONTENT_LENGTH / (1024*1024):.0f} MB",
            'allowed_extensions': list(ALLOWED_EXTENSIONS),
            'simulator': 'qasm_simulator',
            'cors_enabled': True
        }
    })



@app.route('/encode', methods=['POST'])
def encode():
    """Encode a single qubit into 3 qubits."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        
        # Create circuit
        qc = QuantumCircuit(3, 3)
        if initial_state == '1':
            qc.x(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Simulate
        job = simulator.run(transpile(qc, simulator), shots=1000)
        counts = job.result().get_counts()
        
        # Get circuit as string
        circuit_str = str(qc.draw(output='text', fold=-1)).split('\n')
        
        return jsonify({
            'success': True,
            'initial_state': initial_state,
            'encoded_state': '000' if initial_state == '0' else '111',
            'circuit': circuit_str,
            'measurements': counts,
            'shots': 1000
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/error', methods=['POST'])
def introduce_error():
    """Introduce a bit-flip error."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        error_qubit = data.get('error_qubit', 1)
        
        if error_qubit not in [0, 1, 2]:
            return jsonify({'success': False, 'error': 'Invalid qubit'}), 400
        
        # Create circuit with error
        qc = QuantumCircuit(3, 3)
        if initial_state == '1':
            qc.x(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier()
        qc.x(error_qubit)
        qc.barrier()
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Simulate
        job = simulator.run(transpile(qc, simulator), shots=1000)
        counts = job.result().get_counts()
        
        circuit_str = str(qc.draw(output='text', fold=-1)).split('\n')
        
        return jsonify({
            'success': True,
            'initial_state': initial_state,
            'error_qubit': error_qubit,
            'circuit': circuit_str,
            'measurements': counts,
            'shots': 1000
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/error/random', methods=['POST'])
def introduce_random_error():
    """Introduce a random bit-flip error on one of the three qubits."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        
        # Randomly select error qubit (0, 1, or 2)
        error_qubit = random.randint(0, 2)
        
        # Create circuit with random error
        qc = QuantumCircuit(3, 3)
        if initial_state == '1':
            qc.x(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier()
        qc.x(error_qubit)
        qc.barrier()
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Simulate
        job = simulator.run(transpile(qc, simulator), shots=1000)
        counts = job.result().get_counts()
        
        circuit_str = str(qc.draw(output='text', fold=-1)).split('\n')
        
        return jsonify({
            'success': True,
            'initial_state': initial_state,
            'error_qubit': error_qubit,
            'randomly_selected': True,
            'circuit': circuit_str,
            'measurements': counts,
            'shots': 1000
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/correct', methods=['POST'])
def correct():
    """Simulate error correction."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        error_qubit = data.get('error_qubit', 1)
        
        if error_qubit not in [0, 1, 2]:
            return jsonify({'success': False, 'error': 'Invalid qubit'}), 400
        
        # Create circuit with error and correction
        qc = QuantumCircuit(3, 3)
        if initial_state == '1':
            qc.x(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier(label='Encode')
        qc.x(error_qubit)
        qc.barrier(label='Error')
        qc.x(error_qubit)
        qc.barrier(label='Correct')
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Simulate
        job = simulator.run(transpile(qc, simulator), shots=1000)
        counts = job.result().get_counts()
        
        expected = '000' if initial_state == '0' else '111'
        success_count = counts.get(expected, 0)
        success_rate = (success_count / 1000) * 100
        
        circuit_str = str(qc.draw(output='text', fold=-1)).split('\n')
        
        return jsonify({
            'success': True,
            'initial_state': initial_state,
            'error_qubit': error_qubit,
            'expected_state': expected,
            'success_rate': success_rate,
            'circuit': circuit_str,
            'measurements': counts,
            'shots': 1000
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/pipeline', methods=['POST'])
def pipeline():
    """Run complete error correction pipeline."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        error_qubit = data.get('error_qubit', 1)
        shots = data.get('shots', 1000)
        use_random_error = data.get('random_error', False)
        
        # Generate random error qubit if requested
        if use_random_error:
            error_qubit = random.randint(0, 2)
        elif error_qubit not in [0, 1, 2]:
            return jsonify({'success': False, 'error': 'Invalid qubit'}), 400
        
        # Create pipeline circuit
        qc = QuantumCircuit(3, 3)
        
        # Initialize
        if initial_state == '1':
            qc.x(0)
        
        # Encode
        qc.cx(0, 1)
        qc.cx(0, 2)
        
        # Error
        qc.x(error_qubit)
        
        # Correct (flip the same qubit back)
        qc.x(error_qubit)
        
        # Decode
        qc.cx(0, 2)
        qc.cx(0, 1)
        
        # Measure
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Simulate
        job = simulator.run(transpile(qc, simulator), shots=shots)
        counts = job.result().get_counts()
        
        processed_counts = counts
        
        expected = '000' if initial_state == '0' else '111'
        success_count = processed_counts.get(expected, 0)
        success_rate = (success_count / shots) * 100
        
        circuit_str = str(qc.draw(output='text', fold=-1)).split('\n')
        
        return jsonify({
            'success': True,
            'pipeline': {
                'initial_state': initial_state,
                'error_qubit': error_qubit,
                'randomly_selected': use_random_error,
                'expected_state': expected,
                'success_rate': success_rate,
                'corrected': success_rate >= 99.0
            },
            'circuit': circuit_str,
            'measurements': processed_counts,
            'shots': shots
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/statevector', methods=['POST'])
def statevector_analysis():
    """Get statevector analysis at each stage."""
    try:
        data = request.json
        initial_state = data.get('state', '0')
        error_qubit = data.get('error_qubit', 1)
        use_random_error = data.get('random_error', False)
        
        # Generate random error qubit if requested
        if use_random_error:
            error_qubit = random.randint(0, 2)
        elif error_qubit not in [0, 1, 2]:
            return jsonify({'success': False, 'error': 'Invalid qubit'}), 400
        
        results = {}
        
        # Stage 1: Initial
        qc1 = QuantumCircuit(3)
        if initial_state == '1':
            qc1.x(0)
        sv1 = Statevector(qc1)
        results['initial'] = {
            'statevector': [complex(x).real if complex(x).imag == 0 else str(complex(x)) 
                           for x in sv1.data],
            'probabilities': [float(abs(x)**2) for x in sv1.data]
        }
        
        # Stage 2: Encoded
        qc2 = QuantumCircuit(3)
        if initial_state == '1':
            qc2.x(0)
        qc2.cx(0, 1)
        qc2.cx(0, 2)
        sv2 = Statevector(qc2)
        results['encoded'] = {
            'statevector': [complex(x).real if complex(x).imag == 0 else str(complex(x))
                           for x in sv2.data],
            'probabilities': [float(abs(x)**2) for x in sv2.data]
        }
        
        # Stage 3: With error
        qc3 = QuantumCircuit(3)
        if initial_state == '1':
            qc3.x(0)
        qc3.cx(0, 1)
        qc3.cx(0, 2)
        qc3.x(error_qubit)
        sv3 = Statevector(qc3)
        results['with_error'] = {
            'statevector': [complex(x).real if complex(x).imag == 0 else str(complex(x))
                           for x in sv3.data],
            'probabilities': [float(abs(x)**2) for x in sv3.data]
        }
        
        # Stage 4: Corrected
        qc4 = QuantumCircuit(3)
        if initial_state == '1':
            qc4.x(0)
        qc4.cx(0, 1)
        qc4.cx(0, 2)
        qc4.x(error_qubit)
        qc4.x(error_qubit)
        sv4 = Statevector(qc4)
        results['corrected'] = {
            'statevector': [complex(x).real if complex(x).imag == 0 else str(complex(x))
                           for x in sv4.data],
            'probabilities': [float(abs(x)**2) for x in sv4.data]
        }
        
        return jsonify({
            'success': True,
            'error_qubit': error_qubit,
            'randomly_selected': use_random_error,
            'stages': results,
            'basis_states': ['000', '001', '010', '011', '100', '101', '110', '111']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'quantum-error-correction',
        'simulator': 'qasm_simulator'
    })


# =====================================================
# LOCAL BLOB API - FILE UPLOAD/DOWNLOAD
# =====================================================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload file endpoint - Local Blob API
    Saves files to uploads/ folder
    
    Request: multipart/form-data with 'file' field
    Response: JSON with filename and upload details
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file part in request'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Add timestamp to prevent overwrites
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}{ext}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Get file info
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'original_filename': file.filename,
            'size': file_size,
            'size_formatted': f"{file_size / 1024:.2f} KB",
            'upload_time': datetime.now().isoformat(),
            'download_url': f'/download/{unique_filename}'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Download file endpoint - Local Blob API
    Retrieves files from uploads/ folder
    
    URL Parameter: filename
    Response: File download
    """
    try:
        # Secure the filename
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Send file
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/files', methods=['GET'])
def list_files():
    """
    List all uploaded files - Local Blob API
    
    Response: JSON with list of files and metadata
    """
    try:
        files = []
        upload_folder = app.config['UPLOAD_FOLDER']
        
        for filename in os.listdir(upload_folder):
            filepath = os.path.join(upload_folder, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'size_formatted': f"{stat.st_size / 1024:.2f} KB",
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'download_url': f'/download/{filename}'
                })
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'count': len(files),
            'files': files
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """
    Delete file endpoint - Local Blob API
    Removes file from uploads/ folder
    
    URL Parameter: filename
    Response: JSON with deletion status
    """
    try:
        # Secure the filename
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Delete file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': 'File deleted successfully',
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =====================================================
# VISUALIZATION ENDPOINTS
# =====================================================

@app.route('/visualize_circuit', methods=['POST'])
def visualize_circuit():
    """
    Generate circuit visualization
    
    Request: JSON with state and error_qubit
    Response: JSON with circuit drawing and metadata
    """
    try:
        data = request.get_json()
        state = data.get('state', '0')
        error_qubit = data.get('error_qubit', 0)
        
        # Create the full error correction circuit
        qc = QuantumCircuit(3, 3)
        
        # Initial state preparation
        if state == '1':
            qc.x(0)
        
        # Encoding
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.barrier()
        
        # Error introduction
        qc.x(error_qubit)
        qc.barrier()
        
        # Syndrome measurement
        qc.cx(0, 1)
        qc.cx(0, 2)
        
        # Measurements
        qc.measure([0, 1, 2], [0, 1, 2])
        
        # Get circuit as string
        circuit_str = str(qc.draw(output='text', fold=-1))
        
        # Get circuit depth and gate count
        depth = qc.depth()
        gate_count = sum(qc.count_ops().values())
        
        return jsonify({
            'success': True,
            'circuit': circuit_str.split('\n'),
            'depth': depth,
            'gate_count': gate_count,
            'num_qubits': qc.num_qubits,
            'num_clbits': qc.num_clbits,
            'operations': dict(qc.count_ops())
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/add_error', methods=['POST'])
def add_error():
    """
    Add error to encoded state (alias for /error endpoint)
    
    Request: JSON with state and error_qubit
    Response: JSON with measurements after error
    """
    return error()


@app.route('/correct_error', methods=['POST'])
def correct_error():
    """
    Correct error (alias for /correct endpoint)
    
    Request: JSON with state and error_qubit
    Response: JSON with correction results
    """
    return correct()


if __name__ == '__main__':
    print("="*60)
    print("3-QUBIT BIT-FLIP ERROR CORRECTION API")
    print("="*60)
    print("\nServer starting on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("\n--- Core Quantum Operations ---")
    print("  POST /encode         - Encode a qubit")
    print("  POST /error          - Introduce error")
    print("  POST /add_error      - Add error (alias)")
    print("  POST /error/random   - Introduce random error")
    print("  POST /correct        - Simulate correction")
    print("  POST /correct_error  - Correct error (alias)")
    print("  POST /pipeline       - Run full pipeline (supports random)")
    print("  POST /statevector    - Get statevector analysis")
    print("  POST /visualize_circuit - Generate circuit visualization")
    print("\n--- Local Blob API (File Management) ---")
    print("  POST   /upload       - Upload file to server")
    print("  GET    /download/<filename> - Download file from server")
    print("  GET    /files        - List all uploaded files")
    print("  DELETE /delete/<filename> - Delete file from server")
    print("\n--- System ---")
    print("  GET  /health         - Health check")
    print("  GET  /api            - API documentation")
    print("\n" + "="*60)
    print(f"\nUploads directory: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Max upload size: {MAX_CONTENT_LENGTH / (1024*1024):.0f} MB")
    print(f"Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

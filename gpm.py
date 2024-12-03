import os
import sys
import tempfile
import subprocess
import shutil
import threading
from flask import Flask, request, render_template_string
from flask_socketio import SocketIO, emit

def read_output(process, sid, socketio):
    """Read output from the subprocess and emit to the client."""
    for line in iter(process.stdout.readline, b''):
        if line:  # Ensure there's output
            socketio.emit('output', {'data': line.decode().strip()}, namespace='/', to=sid)
    
    # Also read stderr
    for line in iter(process.stderr.readline, b''):
        if line:
            socketio.emit('output', {'data': line.decode().strip()}, namespace='/', to=sid)

class CodeExecutor:
    active_process = None  # Store the subprocess for ongoing interaction
    temp_dir = None  # Track temporary directory for manual cleanup

    @staticmethod
    def start_code_execution(language, code, additional_flags=None):
        """
        Start code execution with optional additional compilation flags.
        
        :param language: Programming language ('cpp' or 'python')
        :param code: Source code to execute
        :param additional_flags: Optional list of additional compilation flags
        :return: Tuple of (process, error)
        """
        # Create a temporary directory manually
        temp_dir = tempfile.mkdtemp()
        CodeExecutor.temp_dir = temp_dir  # Store for later cleanup

        file_extension = '.cpp' if language == 'cpp' else '.py'
        temp_file_path = os.path.join(temp_dir, f'program{file_extension}')

        # Write the code to a temporary file
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(code)

        # Prepare commands
        if language == 'cpp':
            # Prepare base compile command
            compile_command = ['g++', '-std=c++17', temp_file_path, '-o', os.path.join(temp_dir, 'program.out')]
            
            # Add additional flags if provided
            if additional_flags:
                # Validate and sanitize flags to prevent command injection
                safe_flags = []
                allowed_flag_prefixes = [
                    '-W',   # Warning flags
                    '-O',   # Optimization levels
                    '-g',   # Debug information
                    '-std=' # Language standard
                ]
                
                for flag in additional_flags:
                    # Check if flag starts with any of the allowed prefixes
                    if any(flag.startswith(prefix) for prefix in allowed_flag_prefixes):
                        safe_flags.append(flag)
                
                compile_command.extend(safe_flags)
            
            # Run compilation
            compile_result = subprocess.run(compile_command, capture_output=True, text=True)
            if compile_result.returncode != 0:
                return None, compile_result.stderr.strip()
            
            run_command = [os.path.join(temp_dir, 'program.out')]
        
        elif language == 'python':
            run_command = ['python3', temp_file_path]
        else:
            return None, "Unsupported language"

        # Start the process
        process = subprocess.Popen(
            run_command, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            bufsize=1,  # Line buffered
            universal_newlines=False  # Use binary mode for better compatibility
        )
        return process, None

    # ... [rest of the CodeExecutor class remains the same]

class GPMServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.setup_routes()
        self.setup_socket_events()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Interactive Code Runner</title>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.min.js"></script>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 900px; margin: auto; line-height: 1.6; }
                    #output { background: #f0f0f0; padding: 10px; margin-top: 10px; overflow-y: auto; max-height: 300px; }
                </style>
            </head>
            <body>
                <h1>Interactive Code Runner</h1>
                <textarea id="code-editor" placeholder="Enter your code here..." style="width:100%;height:200px;"></textarea>
                <br>
                <select id="language-select">
                    <option value="cpp">C++</option>
                    <option value="python">Python</option>
                </select>
                <input id="compile-flags" type="text" placeholder="Optional compile flags (for C++)" style="width:100%;" />
                <button id="start-code">Start Code</button>
                <button id="stop-code">Stop Code</button>
                <div id="output"></div>
                <input id="user-input" type="text" placeholder="Enter input..." style="width:100%;" />
                <script>
                    const socket = io();
                    const outputDiv = document.getElementById('output');
                    const userInput = document.getElementById('user-input');

                    document.getElementById('start-code').addEventListener('click', () => {
                        const code = document.getElementById('code-editor').value;
                        const language = document.getElementById('language-select').value;
                        const compileFlags = document.getElementById('compile-flags').value
                            .split(' ')
                            .filter(flag => flag.trim() !== '');
                        
                        socket.emit('start_code', { 
                            code: code, 
                            language: language,
                            compile_flags: language === 'cpp' ? compileFlags : []
                        });
                    });

                    document.getElementById('stop-code').addEventListener('click', () => {
                        socket.emit('stop_code');
                    });

                    userInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter') {
                            socket.emit('user_input', userInput.value);
                            userInput.value = '';
                        }
                    });
					
                    // Allow TAB key in textareas
                    function enableTabInTextarea(id) {
                        const textarea = document.getElementById(id);
                        textarea.addEventListener('keydown', function(e) {
                            if (e.key === 'Tab') {
                                e.preventDefault();
                                const start = this.selectionStart;
                                const end = this.selectionEnd;

                                // Set textarea value to: text before caret + tab + text after caret
                                this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);

                                // Put caret at right position again
                                this.selectionStart = this.selectionEnd = start + 1;
                            }
                        });
                    }
                    
                    enableTabInTextarea('code-editor');

                    socket.on('output', (data) => {
                        outputDiv.innerHTML += `<pre>${data.data}</pre>`;
                        outputDiv.scrollTop = outputDiv.scrollHeight; // Auto-scroll to bottom
                    });
                </script>
            </body>
            </html>
            """)

    def setup_socket_events(self):
        @self.socketio.on('start_code')
        def handle_start_code(data):
            language = data['language']
            code = data['code']
            
            # Extract compile flags (if any)
            compile_flags = data.get('compile_flags', [])
            
            # Start code execution
            process, error = CodeExecutor.start_code_execution(
                language, 
                code, 
                additional_flags=compile_flags if language == 'cpp' else None
            )
            
            if error:
                emit('output', {'data': f"Error: {error}"})
                return

            CodeExecutor.active_process = process

            # Start a thread to read output and emit it to the client
            thread = threading.Thread(target=read_output, args=(process, request.sid, self.socketio))
            thread.daemon = True
            thread.start()

        @self.socketio.on('user_input')
        def handle_user_input(input_data):
            if CodeExecutor.active_process:
                CodeExecutor.active_process.stdin.write((input_data + '\n').encode())
                CodeExecutor.active_process.stdin.flush()

        @self.socketio.on('stop_code')
        def handle_stop_code():
            CodeExecutor.stop_code_execution()
            emit('output', {'data': "Process terminated"})

    def run(self):
        self.socketio.run(self.app, debug=True, port=5000)

if __name__ == '__main__':
    GPMServer().run()
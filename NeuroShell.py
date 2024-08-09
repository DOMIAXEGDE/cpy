import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import os
import math

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = [self.initialize_weights(layers[i], layers[i+1]) for i in range(len(layers)-1)]
        self.biases = [self.initialize_biases(layers[i+1]) for i in range(len(layers)-1)]
        self.outputs = None
    
    def initialize_weights(self, input_size, output_size):
        return [[1 for _ in range(output_size)] for _ in range(input_size)]
    
    def initialize_biases(self, output_size):
        return [1 for _ in range(output_size)]
    
    def forward_propagation(self, inputs):
        for layer_idx, (weights, biases) in enumerate(zip(self.weights, self.biases)):
            outputs = []
            for node_idx in range(len(biases)):
                output = sum(weights[i][node_idx] * inputs[i] for i in range(len(inputs))) + biases[node_idx]
                outputs.append(max(0, output))  # ReLU activation function
            inputs = outputs  # Output of this layer becomes the input for the next
        self.outputs = inputs
        return self.outputs
    
    def backpropagation(self, target):
        for layer_idx in range(len(self.weights)):
            self.weights[layer_idx] = [[w + 1 for w in weights] for weights in self.weights[layer_idx]]
            self.biases[layer_idx] = [b + 1 for b in self.biases[layer_idx]]
    
    def reset_network(self):
        self.weights = [self.initialize_weights(self.layers[i], self.layers[i+1]) for i in range(len(self.layers)-1)]
        self.biases = [self.initialize_biases(self.layers[i+1]) for i in range(len(self.layers)-1)]
        self.outputs = None
    
    def save_session(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_session(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural Network Training")
        self.network = None
        self.current_layer = 0
        self.create_widgets()
    
    def create_widgets(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Session", command=self.load_session)
        file_menu.add_command(label="Save Session", command=self.save_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        training_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Training", menu=training_menu)
        training_menu.add_command(label="Set Network Structure", command=self.set_network_structure)
        training_menu.add_command(label="Forward Propagation", command=self.forward_propagation)
        training_menu.add_command(label="Backpropagation", command=self.backpropagation)
        training_menu.add_command(label="Reset", command=self.reset_network)
        training_menu.add_command(label="Run Test", command=self.run_test)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help Documentation", command=self.show_help)

        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill="x")
        
        tk.Label(input_frame, text="Input Data (Positive Integers):").pack(side="left")
        self.input_entry = tk.Entry(input_frame, width=40)
        self.input_entry.pack(side="left", padx=(5, 20))
        
        self.metadata_frame = tk.Frame(self.root, padx=10, pady=10)
        self.metadata_frame.pack(fill="both", expand=True)
        
        self.metadata_label = tk.Label(self.metadata_frame, text="Metadata:", anchor="w")
        self.metadata_label.pack(fill="both")
        
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill="x")
        
        self.forward_button = tk.Button(control_frame, text="Forward Propagation", command=self.forward_propagation)
        self.forward_button.pack(side="left", padx=5)
        
        self.backward_button = tk.Button(control_frame, text="Backpropagation", command=self.backpropagation)
        self.backward_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_network)
        self.reset_button.pack(side="left", padx=5)
        
        nav_frame = tk.Frame(self.root, padx=10, pady=10)
        nav_frame.pack(fill="x")
        
        self.prev_layer_button = tk.Button(nav_frame, text="Previous Layer", command=self.show_previous_layer)
        self.prev_layer_button.pack(side="left", padx=5)
        
        self.next_layer_button = tk.Button(nav_frame, text="Next Layer", command=self.show_next_layer)
        self.next_layer_button.pack(side="left", padx=5)
        
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # Bind click event
    
    def load_session(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.network = NeuralNetwork.load_session(filename)
            self.update_metadata("Session Loaded")
            self.current_layer = 0
            self.show_layer(self.current_layer)

    def save_session(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pkl")
        if filename and self.network:
            self.network.save_session(filename)
            self.update_metadata("Session Saved")

    def set_network_structure(self):
        layer_string = simpledialog.askstring("Network Structure", 
                                              "Enter the number of nodes in each layer as a comma-separated list (e.g., 4,9,16):")
        if layer_string:
            try:
                layers = [int(x) for x in layer_string.split(",") if int(x) > 0 and math.isqrt(int(x))**2 == int(x)]
                if layers:
                    self.network = NeuralNetwork(layers)
                    self.update_metadata(f"Network Structure Set: {layers}")
                    self.current_layer = 0
                    self.show_layer(self.current_layer)
                else:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid list of positive square integers (e.g., 4,9,16).")
    
    def forward_propagation(self):
        if not self.network:
            self.initialize_network()
        inputs = [int(i) for i in self.input_entry.get().split() if i.isdigit() and int(i) > 0]
        if inputs:
            outputs = self.network.forward_propagation(inputs)
            self.update_metadata(f"Forward Propagation Complete: {outputs}")
        else:
            self.update_metadata("Invalid Input: Please enter positive integers only.")

    def backpropagation(self):
        if not self.network:
            self.initialize_network()
        target = [int(e) for e in self.input_entry.get().split() if e.isdigit() and int(e) > 0]
        if target:
            self.network.backpropagation(target)
            self.update_metadata("Backpropagation Complete")
        else:
            self.update_metadata("Invalid Target: Please enter positive integers only.")

    def reset_network(self):
        if not self.network:
            self.initialize_network()
        self.network.reset_network()
        self.update_metadata("Network Reset")
        self.current_layer = 0
        self.show_layer(self.current_layer)

    def initialize_network(self):
        default_structure = [4, 9, 16]
        self.network = NeuralNetwork(default_structure)
        self.update_metadata(f"Default Network Initialized: {default_structure}")
        self.current_layer = 0
        self.show_layer(self.current_layer)

    def show_layer(self, layer_index):
        if self.network:
            layer_size = self.network.layers[layer_index]
            grid_size = math.isqrt(layer_size)
            self.canvas.delete("all")
            square_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // grid_size
            for i in range(grid_size):
                for j in range(grid_size):
                    x0 = j * square_size
                    y0 = i * square_size
                    x1 = x0 + square_size
                    y1 = y0 + square_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="light gray", outline="black")
            self.update_metadata(f"Showing Layer {layer_index + 1}/{len(self.network.layers)} with {layer_size} nodes")

    def show_previous_layer(self):
        if self.network and self.current_layer > 0:
            self.current_layer -= 1
            self.show_layer(self.current_layer)

    def show_next_layer(self):
        if self.network and self.current_layer < len(self.network.layers) - 1:
            self.current_layer += 1
            self.show_layer(self.current_layer)

    def run_test(self):
        if not self.network:
            self.initialize_network()
        
        predefined_input = [1 for _ in range(self.network.layers[0])]
        outputs = self.network.forward_propagation(predefined_input)
        
        result_message = f"Test Run Completed:\nInput: {predefined_input}\nOutput: {outputs}"
        self.update_metadata(result_message)
        messagebox.showinfo("Test Result", result_message)

    def on_canvas_click(self, event):
        if not self.network:
            messagebox.showerror("Error", "Please set the network structure first.")
            return
        
        layer_size = self.network.layers[self.current_layer]
        grid_size = math.isqrt(layer_size)
        square_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // grid_size
        col = event.x // square_size
        row = event.y // square_size
        index = row * grid_size + col + 1
        
        filename = f"{index}.rb"
        if os.path.exists(filename):
            self.run_file(filename)
        else:
            messagebox.showerror("File Not Found", f"No file found for index {index}.")

    def run_file(self, filename):
        extension = filename.split('.')[-1]
        
        if extension in ['rb', 'py', 'js', 'php', 'cpp', 'c']:
            # Run the script
            try:
                if extension == 'rb':
                    subprocess.run(["ruby", filename])
                elif extension == 'py':
                    subprocess.run(["python", filename])
                elif extension == 'js':
                    subprocess.run(["node", filename])
                elif extension == 'php':
                    subprocess.run(["php", filename])
                elif extension == 'cpp':
                    subprocess.run(["g++", filename, "-o", "program.out"])
                    subprocess.run(["./program.out"])
                elif extension == 'c':
                    subprocess.run(["gcc", filename, "-o", "program.out"])
                    subprocess.run(["./program.out"])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run {filename}: {e}")
        
        elif extension == 'txt':
            # Open in the default web browser
            try:
                os.startfile(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {filename}: {e}")
        
        else:
            messagebox.showerror("Unsupported File Type", f"Cannot run files with extension {extension}")

    def update_metadata(self, message):
        self.metadata_label.config(text=f"Metadata: {message}")

    def show_help(self):
        help_text = (
            "Neural Network Training Application\n\n"
            "1. Set Network Structure: Define the architecture of the neural network by specifying the number of "
            "nodes in each layer as a comma-separated list. Each layer must have a square number of nodes.\n"
            "2. Input Data: Enter a series of positive integers separated by spaces. These correspond to the "
            "nodes for forward propagation.\n"
            "3. Forward Propagation: Click this option or the corresponding button to propagate the input data "
            "through the network. The output is displayed as metadata.\n"
            "4. Backpropagation: Enter the target values as positive integers and click this option or the corresponding "
            "button to perform backpropagation, adjusting the network's weights.\n"
            "5. Reset: Reset the neural network to its initial state.\n"
            "6. Navigate Layers: Use the 'Previous Layer' and 'Next Layer' buttons to navigate through the layers "
            "of the network. The grid will update to show the nodes in the selected layer.\n"
            "7. Run Test: Automatically test the network with a predefined input to see how it processes data and "
            "what the outputs are. This helps demonstrate the practical use of the network.\n"
            "8. Execute File: Click on any sub-square to execute a corresponding file (e.g., .rb, .html, .cpp). "
            "If a .txt file is selected, it will be opened in the default web browser.\n"
            "9. Save/Load Session: Save the current state of the network or load a previously saved session.\n\n"
            "Ensure that all required libraries and compilers are installed on your local machine to execute the files."
        )
        messagebox.showinfo("Help Documentation", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()

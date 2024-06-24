from tkinter import *
import tkinter as tk
import random
import os
os.environ['QT_API'] = 'pyqt5'
import math
from PIL import Image
import subprocess
import io #experiment
import pygame
import importlib
import requests
import webbrowser
import csv
from bs4 import BeautifulSoup
import datetime
import sys
import json
import re
from PIL import ImageGrab
import pickle
from tkinter import simpledialog
from tkinter import Menu, Checkbutton, BooleanVar #For Windows OS
#from tkinter import Menu, Checkbutton #For macOS
#from tkinter import BooleanVar #For macOS
from tkinter.colorchooser import askcolor
import logging
import time
import pyautogui
import keyboard
from tkinter import filedialog
from PIL import ImageTk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import schemdraw
import schemdraw.elements as elm
from schemdraw import logic
from itertools import product
from matplotlib import pyplot as plt
import numpy as np
import glob
from collections import defaultdict
from matplotlib.animation import FuncAnimation
import psutil
import schedule
from pathlib import Path
import shutil
import importlib.util
#import pyautogui
#from PIL import Image, experiment

from PIL import Image, ImageDraw
import plotly.graph_objects as go
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

templates = {
    "basic": ["id", "name", "value"],
    "detailed": ["id", "name", "description", "timestamp"]
}

print("""Here is a list of one hundred distinct fields within the realm of mathematical research and development:

1. Algebraic Geometry
2. Algebraic Topology
3. Algebraic Number Theory
4. Algebraic Combinatorics
5. Analytic Number Theory
6. Applied Mathematics
7. Approximation Theory
8. Arithmetic Geometry
9. Asymptotic Analysis
10. Biomathematics
11. Braid Theory
12. Calculus of Variations
13. Category Theory
14. Chaos Theory
15. Coding Theory
16. Combinatorial Topology
17. Combinatorics
18. Complex Analysis
19. Computational Algebra
20. Computational Geometry
21. Computational Number Theory
22. Control Theory
23. Cryptography
24. Differential Algebra
25. Differential Equations
26. Differential Geometry
27. Differential Topology
28. Discrete Geometry
29. Discrete Mathematics
30. Dynamical Systems
31. Elliptic Curves
32. Enumerative Combinatorics
33. Ergodic Theory
34. Experimental Mathematics
35. Finite Geometry
36. Fluid Dynamics
37. Fourier Analysis
38. Fractal Geometry
39. Functional Analysis
40. Fuzzy Mathematics
41. Game Theory
42. Geometric Analysis
43. Geometric Topology
44. Graph Theory
45. Group Theory
46. Harmonic Analysis
47. Homological Algebra
48. Homotopy Theory
49. Hyperbolic Geometry
50. Incidence Geometry
51. Information Theory
52. Integral Equations
53. Integrable Systems
54. K-Theory
55. Knot Theory
56. Lie Algebras
57. Lie Groups
58. Linear Algebra
59. Linear Programming
60. Logic
61. Manifold Theory
62. Mathematical Biology
63. Mathematical Finance
64. Mathematical Logic
65. Mathematical Physics
66. Matrix Theory
67. Measure Theory
68. Model Theory
69. Noncommutative Geometry
70. Nonlinear Dynamics
71. Number Theory
72. Numerical Analysis
73. Operator Algebras
74. Operator Theory
75. Optimization
76. Ordinary Differential Equations
77. Partial Differential Equations
78. Percolation Theory
79. Perturbation Theory
80. Probability Theory
81. Quantum Algebra
82. Quantum Groups
83. Quantum Topology
84. Queueing Theory
85. Real Analysis
86. Representation Theory
87. Riemannian Geometry
88. Ring Theory
89. Set Theory
90. Singularity Theory
91. Spectral Theory
92. Statistical Mechanics
93. Stochastic Processes
94. Symplectic Geometry
95. Systems Theory
96. Tensor Analysis
97. Topological Groups
98. Topology
99. Tropical Geometry
100. Wavelets and Multiresolution Analysis

These fields represent a vast landscape of mathematical inquiry and have extensive applications across various scientific and engineering domains.

Here is a description of twelve broad fields of study that encompass many of the specialized areas of mathematical research and development just listed:

1. Algebraic Structures: This field includes studies in algebraic geometry, algebraic topology, algebraic number theory, and algebraic combinatorics. It involves the exploration of mathematical structures that are fundamentally algebraic in nature, involving operations within sets that follow specific axioms, like groups, rings, and fields. These studies are crucial for understanding geometrical properties through algebraic expressions.

2. Number Theory: Comprising analytic number theory, algebraic number theory, and arithmetic geometry, this field focuses on the properties and relationships of numbers, particularly the integers. It utilizes techniques from a broad range of mathematical disciplines to solve problems related to divisibility, congruences, and the distribution of primes.

3. Combinatorics and Graph Theory: This includes enumerative combinatorics, algebraic combinatorics, and graph theory. It studies combinatorial structures and their algebraic properties to understand configurations and relations like those found in graph structures, designs, and codes.

4. Topological Studies: This field covers areas such as algebraic topology, differential topology, and geometric topology. It deals with properties that are preserved through deformations, twistings, and stretchings of objects, investigating concepts like continuity, compactness, and connectedness.

5. Differential Geometry and Geometric Analysis: This encompasses differential geometry, differential topology, and geometric analysis. It involves the use of calculus and algebra to study problems in geometry, focusing on curves, surfaces, and higher-dimensional analogues.

6. Analytical Studies: Fields like complex analysis, functional analysis, and harmonic analysis fall under this category. They involve the detailed investigation of functions, their spaces, and other related mathematical entities, providing a deep understanding of their behavior and properties.

7. Applied Mathematical Sciences: This includes applied mathematics, mathematical physics, mathematical finance, and biomathematics, focusing on the application of mathematical methods by different fields such as science and engineering. This area applies theories and techniques from the pure parts of mathematics to practical problems.

8. Computational Mathematics: This field covers computational algebra, computational geometry, and numerical analysis. It deals with mathematical research in areas that require large-scale computation and algorithmic precision, often for simulations, optimizations, and complex calculations.

9. Discrete Mathematics: Including discrete geometry, combinatorial topology, and discrete mathematics itself, this field investigates mathematical structures that are fundamentally discrete rather than continuous. It has applications in computer science, cryptography, and information theory.

10. Dynamical Systems and Ergodic Theory: Studying areas like dynamical systems, chaos theory, and ergodic theory, this field explores systems that evolve over time according to specific rules. It examines how these systems behave, evolve, and respond to various inputs over the long term.

11. Mathematical Logic and Foundations: Covering logic, set theory, and model theory, this field studies the formal basis of mathematics. It investigates the principles of mathematical reasoning, the nature of mathematical objects, and the theoretical underpinnings of mathematical theories.

12. Optimization and Control Theory: Encompassing linear programming, optimization, control theory, and systems theory, this field is concerned with finding the best possible solution to a problem, given constraints and objectives, and controlling the behavior of dynamic systems in an optimal manner.

Each of these fields is vast and interconnects with multiple areas of mathematics, illustrating the profound depth and breadth of mathematical research and development.

Enumerative Mathematical Framework of Thought:

1	[ Definitions And Operators ]

1	Proof = The absence of doubt.

2	Solution = To solve a problem without the cause of another.

3	Problem = The presence of doubt.

4	Context = Only one context is ever present. That is, once true, always true.

5	Number = A physical structure, present due to a state transition.

6	Unit transition = The least effective change of state.

7	Compound transition = A sequence of unit transitions.

8	Set = An array of numbers.

9	Map = One Number results in another Number, by a defined Unit or Compound transition.

10	Claim = A map.

11	Completion = Proof of Claim.

12	And

13	Xor (Exclusively Or)

14	Not

2	[ Statement ]

1	1.6 + 1.6 = 1.7

2	by definition

3	2 of 1.6 and 1.7 1 has achieved 1.11

3	[ Statement ]

1	(a - b) is prime

2	i = a

3	i = b

4	Summation of

5	(i + 1)

6	4 5 from 2 to 3

7	The square root of

8	6/(a/2)

9	decimal part of 8

10	Exclusively OR

11	1 - (decimal part of 8)

12	9 10 11

13	8 plus or minus 12, is prime

14	zero is less than 10 equal to 12 which is less than 10 equal to one

15	(-1) is the step value of 6

16	(a > b)

17	zero is less than (a - b) which is less than 10 equal to 12

18	1 6 8 12 17 13 15 16

19	Execute 18 as the 1.6 10 1.7

20	19 outputs (The number 2, 3 Xor 5)""")

#test
# Define functions for various operations
def list_files(directory='.'):
    return os.listdir(directory)

def get_system_info():
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'virtual_memory': psutil.virtual_memory()._asdict(),
        'disk_usage': psutil.disk_usage('/')._asdict()
    }

def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    return f"Downloaded {url} to {save_path}"

def move_mouse(x, y, duration=1):
    try:
        x = int(x)
        y = int(y)
        duration = float(duration)
        pyautogui.moveTo(x, y, duration=duration)
        return f"Moved mouse to ({x}, {y}) in {duration} seconds"
    except ValueError:
        return "Error: x and y must be integers, and duration must be a float or an integer."
    except Exception as e:
        return f"Error executing move_mouse: {e}"

def take_screenshot(save_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    return f"Screenshot saved to {save_path}"

# Define a mapping of command names to functions
COMMANDS = {
    'list_files': list_files,
    'get_system_info': get_system_info,
    'download_file': download_file,
    'move_mouse': move_mouse,
    'take_screenshot': take_screenshot,
    # Add more commands as needed
}

# Create a global dictionary to hold the user-defined variables and functions
global_context = {}

# Function to execute predefined commands
def execute_user_command(command_name, *args):
    if command_name in COMMANDS:
        try:
            result = COMMANDS[command_name](*args)
            return result
        except Exception as e:
            return f"Error executing command: {e}"
    else:
        return f"Unknown command: {command_name}"

# Function to execute dynamic code
def execute_dynamic_code(user_code):
    try:
        # Execute the code within the global context
        exec(user_code, global_context)
    except Exception as e:
        print(f"Error executing code: {e}")

def eval_dynamic_code(user_code):
    try:
        # Evaluate the code within the global context
        result = eval(user_code, global_context)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")

# Function to handle multiline input
def multiline_input():
    print("Enter your Python code (type 'end' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().lower() == 'end':
            break
        lines.append(line)
    return '\n'.join(lines)

# Interactive CLI
def interactive_cli():
    print("Welcome to the Python CLI for Windows Control")
    print("Type 'help' to see available commands, 'exit' to quit, or prefix with '!' to execute Python code.")
    print("Type 'multi' to enter multiline Python code.")
    
    while True:
        user_input = input("> ")
        
        if user_input in ['exit', 'quit']:
            break
        elif user_input == 'help':
            print("Available commands:")
            for cmd in COMMANDS:
                print(f"  {cmd}")
            print("You can also enter Python code prefixed with '!' to execute.")
            print("Type 'multi' to enter multiline Python code.")
        elif user_input == 'multi':
            code = multiline_input()
            execute_dynamic_code(code)
        elif user_input.startswith('!'):
            if "=" in user_input or 'import' in user_input:
                # Handle assignment and execution statements
                execute_dynamic_code(user_input[1:])
            else:
                # Handle evaluation statements
                eval_dynamic_code(user_input[1:])
        else:
            # Execute predefined commands
            command_parts = user_input.split()
            command_name = command_parts[0]
            command_args = command_parts[1:]
            output = execute_user_command(command_name, *command_args)
            print(output)
#test

class TuringCompleteAutomaton23:
    def __init__(self):
        self.tape = {}
        self.head_position = 0

    def write_tape23(self, value):
        self.tape[self.head_position] = value
        # Generate the point before moving the head
        self.generate_point23()
        print(f"Written {value} at position {self.head_position}")
        self.move_head23('right', 1)  # Move head right after writing and generating point

    def move_head23(self, direction, steps=1):
        old_position = self.head_position
        if direction == 'left':
            self.head_position -= steps
        elif direction == 'right':
            self.head_position += steps
        print(f"Moved from {old_position} to {self.head_position}")

    def generate_point23(self):
        x = self.head_position
        y = self.tape.get(self.head_position, 0)
        print(f"Generated point ({x}, {y})")

def read_file23(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def process_file_content23(content, tca):
    character_map = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
        'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25,
        ' ': 26, '\n': 27, '\t': 28, '\\': 29, '\'': 30, ',': 31, '/': 32, '<': 33, '>': 34, '?': 35, ';': 36, ':': 37,
        '@': 38, '#': 39, '~': 40, ']': 41, '[': 42, '{': 43, '}': 44, '"': 45, '¬': 46, '|': 47, '¦': 48, '!': 49,
        '£': 50, '$': 51, '%': 52, '^': 53, '&': 54, '*': 55, '(': 56, ')': 57, '-': 58, '_': 59, '+': 60, '=': 61,
        '.': 62, 'A': 63, 'B': 64, 'C': 65, 'D': 66, 'E': 67, 'F': 68, 'G': 69, 'H': 70, 'I': 71, 'J': 72, 'K': 73,
        'L': 74, 'M': 75, 'N': 76, 'O': 77, 'P': 78, 'Q': 79, 'R': 80, 'S': 81, 'T': 82, 'U': 83, 'V': 84, 'W': 85,
        'X': 86, 'Y': 87, 'Z': 88, '0': 89, '1': 90, '2': 91, '3': 92, '4': 93, '5': 94, '6': 95, '7': 96, '8': 97, '9': 98, '`': 99
    }
    for char in content:
        value = character_map.get(char, -1)
        tca.write_tape23(value)

def main23():
    filename = input("Enter the filename of the .txt file: ")
    content = read_file23(filename)
    tca = TuringCompleteAutomaton23()
    process_file_content23(content, tca)
    plot_coordinates23(tca.tape)

def plot_coordinates23(tape):
    x_vals, y_vals = list(tape.keys()), list(tape.values())
    fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='markers+lines', name='Coordinates'))
    fig.update_layout(title='Interactive Plot of Generated Coordinates',
                      xaxis_title='X Axis',
                      yaxis_title='Y Axis')
    fig.show()
    # Optionally, you can save the plot as an HTML file
    fig.write_html('plot.html')
    print("Plot saved as 'plot.html'.")

class TuringCompleteAutomaton:
    def __init__(self):
        self.tape = {}
        self.head_position = 0

    def write_tape(self, value):
        self.tape[self.head_position] = value
        print(f"Written {value} at position {self.head_position}")

    def move_head(self, direction, steps):
        old_position = self.head_position
        if direction == 'left':
            self.head_position -= steps
        elif direction == 'right':
            self.head_position += steps
        print(f"Moved from {old_position} to {self.head_position}")

    def generate_point(self):
        x = self.head_position
        y = self.tape.get(self.head_position, 0)
        print(f"Generated point ({x}, {y})")
        return (x, y)

def main22():
    tca = TuringCompleteAutomaton()
    points = []

    print("Welcome to the Turing Complete Coordinate Point Simulator")
    print("Instructions:")
    print("  write [value] - Write a value at the current tape position.")
    print("  move left [steps] - Move the head left by a specified number of steps.")
    print("  move right [steps] - Move the head right by a specified number of steps.")
    print("  generate - Generate a point based on the current tape and head position.")
    print("  exit - Exit the program.")
    print()

    while True:
        command = input("Enter command: ").strip().lower()
        parts = command.split()
        action = parts[0]

        if action == "write" and len(parts) > 1:
            value = float(parts[1])
            tca.write_tape(value)
        elif action in ["move", "move"] and len(parts) == 3:
            direction = parts[1]
            steps = int(parts[2])
            tca.move_head(direction, steps)
        elif action == "generate":
            points.append(tca.generate_point())
        elif action == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command. Please try again.")

    print("Generated Coordinates:", points)
    plot_coordinates22(points)

def plot_coordinates22(points):
    x_vals, y_vals = zip(*points) if points else ([], [])
    fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='markers+lines', name='Coordinates'))
    fig.update_layout(title='Interactive Plot of Generated Coordinates',
                      xaxis_title='X Axis',
                      yaxis_title='Y Axis')
    fig.show()
    # Optionally, you can save the plot as an HTML file
    fig.write_html('plot.html')
    print("Plot saved as 'plot.html'.")

def is_prime21(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

class ProximalPrimeFSM:
    def __init__(self, initial_a, initial_b, user_iterations):
        self.initial_a = initial_a
        self.initial_b = initial_b
        self.user_iterations = user_iterations
        self.primes = []

    def run(self):
        base_iterations = 144  # Default for all combinations
        total_iterations = base_iterations + self.user_iterations
        for _ in range(total_iterations):
            a, b = self.initial_a, self.initial_b
            for j in range(12, 0, -1):  # Descending loop for a
                for k in range(12, 0, -1):  # Descending loop for b
                    self.a = a + j
                    self.b = b + k
                    if self.validate():
                        p = self.compute_p()
                        z = self.compute_z(p)
                        epsilons = self.compute_epsilons(z)
                        self.prepare_z_values(z, epsilons)
            # Reset to initial values plus maximum shift for next iteration
            self.initial_a += 12
            self.initial_b += 12
    
    def validate(self):
        return self.a > self.b and 0 < (self.a - self.b) <= 12
    
    def compute_p(self):
        return sum(i + 1 for i in range(self.b, self.a + 1))
    
    def compute_z(self, p):
        return math.sqrt(p / (self.a / 2))
    
    def compute_epsilons(self, z):
        epsilon1 = z - int(z)
        return [epsilon1, 1 - epsilon1, 1]
    
    def prepare_z_values(self, z, epsilons):
        z_values = [z + epsilon for epsilon in epsilons] + [z - epsilon for epsilon in epsilons]
        for z_val in z_values:
            if int(z_val) == z_val and is_prime21(int(z_val)):
                self.primes.append(z_val)

# Prepare 3D coordinates
def prepare_coordinates21(primes):
    coords = []
    for i in range(0, len(primes), 3):
        chunk = primes[i:i+3]
        if len(chunk) < 3:
            chunk += [1] * (3 - len(chunk))
        coords.append(chunk)
    return coords

# Animation setup
def animate21(i):
    ax.clear()
    ax.scatter(*zip(*coords[:i+1]), c='r', marker='o')
    ax.set_xlim(0, max(coords, key=lambda x: x[0])[0] + 10)
    ax.set_ylim(0, max(coords, key=lambda x: x[1])[1] + 10)
    ax.set_zlim(0, max(coords, key=lambda x: x[2])[2] + 10)

###################


def index_to_rgb19(color_index):
    """Convert a color index to an RGB tuple."""
    red = (color_index >> 16) & 255  # Shift right by 16 bits and mask with 255 to get the red component
    green = (color_index >> 8) & 255  # Shift right by 8 bits and mask with 255 to get the green component
    blue = color_index & 255  # Mask with 255 to get the blue component
    return (red, green, blue)

def calculate_configuration_index19(square_color_index, symbol_index, font_color_index):
    NUM_SYMBOLS = 97
    NUM_FONT_COLORS = 256**3
    index = (square_color_index * NUM_SYMBOLS * NUM_FONT_COLORS) + (symbol_index * NUM_FONT_COLORS) + font_color_index
    return index

def save_configuration_to_file19(file_name, grid_size, square_size, font_size, configurations):
    with open(file_name, 'w') as file:
        file.write(f"Grid Size: {grid_size}x{grid_size}\n")
        file.write(f"Sub-square Pixel Length: {square_size}\n")
        file.write(f"Font Size: {font_size}\n")
        file.write("Configurations:\n")
        
        for config in configurations:
            square_color_index, symbol_index, font_color_index = config
            index = calculate_configuration_index19(square_color_index, symbol_index, font_color_index)
            # Convert indices to RGB
            square_color_rgb = index_to_rgb19(square_color_index)
            font_color_rgb = index_to_rgb19(font_color_index)
            file.write(f"Index: {index}, Square Color Index: {square_color_index} (RGB: {square_color_rgb}), Symbol: {symbol_index}, Font Color Index: {font_color_index} (RGB: {font_color_rgb})\n")


def is_prime18(num):
    """Check if a number is prime. Assumes num is a positive integer."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def main18():
    # Input a and b
    a = int(input("Enter a (a > b): "))
    b = int(input("Enter b (b < a): "))

    # Validate conditions for a and b
    if not (a > b and 0 < (a - b) <= 12):
        print("The conditions 0 < (a - b) <= 12 and a > b are not met.")
        return
    
    # Calculate p, the sum from i = a to i = b of (i + 1)
    p = sum(i + 1 for i in range(b, a + 1))
    
    # Calculate z
    z = math.sqrt(p / (a / 2))
    
    # Calculate epsilon (decimal part of z)
    epsilon1 = z - int(z)
    epsilon2 = 1 - epsilon1
    epsilon3 = 1
    
    # Prepare the possible z values to check for primality
    z_values = {
        "z + epsilon2": z + epsilon2,
        "z - epsilon1": z - epsilon1,
        "z - epsilon2": z - epsilon2,
        "z + epsilon1": z + epsilon1,
        "z + epsilon3": z + epsilon3,
        "z - epsilon3": z - epsilon3
    }
    
    # Get file name from user and write the results
    file_name = input("Enter the name of the file to save results: ")
    with open(file_name, "w") as file:
        file.write(f"Input values: a = {a}, b = {b}\n")
        file.write(f"Calculated p: {p}\n")
        file.write(f"Calculated z: {z}\n")
        file.write(f"Calculated epsilon1: {epsilon1}\n")
        file.write(f"Calculated epsilon2: {epsilon2}\n")
        file.write(f"epsilon3: {epsilon3}\n")
        for label, value in z_values.items():
            if int(value) == value:
                prime_status = is_prime18(int(value))
            else:
                prime_status = "N/A (not an integer)"
            file.write(f"Is {label} = {value} prime? {prime_status}\n")

def append_string_to_file2(directory, filename, user_string):
    """Appends the user string to a file if it does not already exist in the file."""
    # Create full file path
    file_path = os.path.join(directory, filename)
    
    # Check if file exists and read its contents if it does
    if(os.path.exists(file_path) and len(user_string) > 4):
        with open(file_path, 'r', encoding='utf-8') as file:
            if user_string in file.read():
                print("The string is already in the file.")
                return
    else:
        print(f"\n\n{filename} does exist.")
        print("\n\tNote: Your string must be greater than 4 characters in length. Generate 1.txt, 2.txt, 3.txt, 4.txt in llanguageMod/mappings using mode 12 ...\n\n")
    
    if len(user_string) > 4:
        # First, determine the current number of lines in the file
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                current_line_number = sum(1 for _ in file) + 1
        else:
            current_line_number = 1  # File doesn't exist yet, so start from line 1

        # Append the string to the file, adding the line number before the string
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{current_line_number} {user_string}\n")
        print(f"String added to {filename}")


def main2():
    # Read user input
    user_string = input("Please enter a string: ")
    
    # Calculate the length of the string
    n = len(user_string)
    
    # Define directory and filename
    directory = "llanguageMod/mappings"
    filename = f"{n}.txt"
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory {directory}")
    
    # Append string to the appropriate file
    append_string_to_file2(directory, filename, user_string)

def base_x_to_binary(num, base):
  """Converts a base x integer to a binary string."""
  digits = "0123456789ABCDEF" # Up to base 16
  if base < 2 or base > 16:
    raise ValueError("Base must be between 2 and 16")

  binary = ""
  while num > 0:
    binary = digits[num % 2] + binary
    num //= 2
  return binary


def convert_file(input_file, output_file, base):
  """Converts a file of base x integers to a file of binary strings.

  Args:
      input_file: Path to the input file.
      output_file: Path to the output file.
      base: The base of the integers in the input file.
  """
  with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
      numbers = [int(x) for x in line.strip().split()]
      binary_strings = [base_x_to_binary(num, base) for num in numbers]
      f_out.write(" ".join(binary_strings) + "\n")

def generate_and_save_n_bit_combinations(file_path, n):
    with open(file_path, "w") as file:
        for i in range(2**n):  # 2^n combinations
            combination = bin(i)[2:].zfill(n)
            file.write(combination + "\n")

def decompile_data():
    """Decompiles data using a dynamically loaded decompile function."""
    name = input("Enter the name of the data structure to decompile: ")
    filename = f"{name}_logic.py"
    if not os.path.exists(filename):
        print(f"Logic script for {name} not found. Please ensure the data structure is defined and compiled first.")
        return
    
    compiled_input = input("Enter compiled data string: ")
    try:
        decompiled_data = execute_dynamic_script(name, f"decompile_{name}", compiled_input)
        print("Decompiled Data:", json.dumps(decompiled_data, indent=4))
    except Exception as e:
        print("An error occurred:", e)

def execute_dynamic_script(name, function_name, data):
    """Dynamically import and execute a function from a generated script."""
    filename = f"{name}_logic.py"
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, function_name)
    return func(data)
    
def populate_data(name):
    """Prompt the user to enter data for the defined structure and save to a text file."""
    filename = f"{name}.json"
    if not os.path.exists(filename):
        print(f"Data structure definition for {name} not found. Please define the data structure first.")
        return

    try:
        with open(filename, 'r') as file:
            data_structure = json.load(file)
        
        data = {}
        for field in data_structure['fields']:
            data[field] = input(f"Enter value for {field}: ")

        data_filename = f"{name}_data.txt"
        with open(data_filename, 'a') as file:
            file.write(' | '.join(str(data[field]) for field in data_structure['fields']) + '\n')
        print(f"Data saved to {data_filename}.")
    
    except FileNotFoundError:
        print("Error loading data structure file. Please check the file system.")


def countables():
    while True:
        print("\nMain Menu:")
        print("1. Define Data Structure")
        print("2. Populate Data")
        print("3. Compile Data")
        print("4. Decompile Data")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            define_data_structure()
        elif choice == "2":
            name = input("Enter the name of the data structure to populate: ")
            populate_data(name)
        elif choice == "3":
            name = input("Enter the name of the data structure to compile: ")
            compile_data(name)
        elif choice == "4":
            decompile_data()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please select again.")

# Assuming the execute_dynamic_script function is already defined and imported as discussed.

def define_data_structure():
    template_choice = input("Select template (basic, detailed): ")
    if template_choice not in templates:
        print("Invalid template. Returning to main menu.")
        return

    name = input("Enter name for the data structure: ")
    data_structure = {'name': name, 'fields': templates[template_choice]}
    filename = f"{name}.json"
    with open(filename, 'w') as file:
        json.dump(data_structure, file)
    script_content = generate_scripts(name, templates[template_choice])
    save_script(name, script_content)
    print(f"Data structure {name} defined with template {template_choice} and saved as {filename}.")

def generate_scripts(name, fields):
    compile_func = f"def compile_{name}(data):\n"
    compile_func += "    return '|'.join(str(data[field]) for field in data)\n"
    
    decompile_func = f"def decompile_{name}(data):\n"
    decompile_func += "    fields = " + str(fields) + "\n"
    decompile_func += "    return dict(zip(fields, data.split('|')))\n"
    
    return compile_func + "\n" + decompile_func

def save_script(name, content):
    filename = f"{name}_logic.py"
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Compile/Decompile logic saved to {filename}.")
    
def compile_data(name):    
    """Compiles data using a dynamically loaded compile function."""
    filename = f"{name}_logic.py"
    if not os.path.exists(filename):
        print(f"Logic script for {name} not found. Please ensure the data structure is defined and compiled first.")
        return

    print("Enter data to compile (format as JSON, e.g., {'id':'123', 'name':'John'}):")
    print("Note: Ensure your JSON is correctly formatted for your command line environment.")
    data_input = input()
    try:
        # Strip out unwanted characters if necessary (specific to your environment)
        data_input = data_input.strip()
        if data_input.startswith("'") and data_input.endswith("'"):
            data_input = data_input[1:-1]  # Remove surrounding single quotes for Unix/Linux shells
        data = json.loads(data_input)  # Safely parse the JSON input
        compiled_data = execute_dynamic_script(name, f"compile_{name}", data)
        print("Compiled Data:", compiled_data)
    except json.JSONDecodeError:
        print("Invalid JSON input. Please check the format and try again.")
    except Exception as e:
        print("An error occurred:", e)

# Directly invoking the main menu function when the script runs
#countables()
#####################

def main0():
    print("\n\nWelcome. Choose your operation: ")
    # User option to generate mappings or not
    generate_mappings = input("Do you want to generate mappings? 1 [for yes], 0 [for no]: ")
    if generate_mappings == "1":
        Llanguage_model()

    # Define input and output directories
    in1 = "llanguageMod/inputs"
    out1 = "llanguageMod/outfile"
    out2 = "llanguageMod/outb"


    
    proces = input("Do you want to process files? 1 [for yes], 0 [for no]: ")
    if(proces == '1'):
        # Read mappings only if they are necessary
        mappings = read_mappings()
        # Get user input for the range of files to process
        start = int(input("Enter the start of the range of files to read (e.g., 5 for 5.txt): "))
        end = int(input("Enter the end of the range of files to read (e.g., 15 for 15.txt): "))

        # Process files within the specified range
        process_files(in1, out1, start, end, mappings, out2)

    # Optionally, generate an image from text input
    questione = input("Generate text input to image file? 1 [for yes], 0 [for no]: ")
    if questione == "1":
        data = open_file0()
        if data:
            process_image_generation0(data)

def process_image_generation0(data):
    """Generates an image from provided data."""
    if not data:
        print("No data to process for image generation.")
        return
    print("Data received for image generation:", data)
    color_data = data_to_color0(data)
    if not color_data:
        print("No color data generated.")
        return
    image = create_image0(color_data)
    image.show()  # Optionally display the image
    save_option = input("Do you want to save this image as a PDF? (yes/no): ")
    if save_option.lower() == 'yes':
        # Assuming 'image' is a PIL Image object you've created or manipulated
        file_path = input("Enter the path to save the PDF file (including filename): ")
        save_image_as_pdf0(image, file_path)
        
def create_image0(color_data):
    """ Create an image from the color data based on user input dimensions and pixel size. """
    # Dimensions based on the length of color_data to create a square image
    num_pixels_width = int(len(color_data) ** 0.5)  # Assuming a roughly square image for simplicity
    num_pixels_height = num_pixels_width if num_pixels_width ** 2 == len(color_data) else num_pixels_width + 1
    
    pixel_side_length = 10  # Each color block will be 10x10 pixels

    img_width = pixel_side_length * num_pixels_width
    img_height = pixel_side_length * num_pixels_height

    # Create a new image with white background
    image = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw each block
    index = 0
    for i in range(num_pixels_height):
        for j in range(num_pixels_width):
            if index < len(color_data):
                top_left = (j * pixel_side_length, i * pixel_side_length)
                bottom_right = ((j + 1) * pixel_side_length, (i + 1) * pixel_side_length)
                draw.rectangle([top_left, bottom_right], fill=color_data[index])
            index += 1

    return image
        
def data_to_color0(data):
    """ Convert each data item to a unique color based on its hash value. """
    if not data:  # Validate input
        print("No data provided to convert to color.")
        return []
    return ['#' + '{:06X}'.format(hash(datum) & 0xFFFFFF) for datum in data if isinstance(datum, str)]


def open_file0():
    """ Prompt user to enter a file path, read the file, and return the content as a list of words. """
    file_path = input("Enter the path of the text file: ")
    try:
        with open(file_path, 'r') as file:
            data = file.read().split()
        print("File successfully opened.")
        return data
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

# Uncomment the following line to run the main function in a script environment
# main()


def Llanguage_model():
    characters = 'abcdefghijklmnopqrstuvwxyz \n\t\\\',/<>?;:@#~][{}\'¬|¦!"£$%^&*()-_+=.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    # Asking user for input
    try:
        pinned = int(input("Enter the number of characters to use (up to 100), or 100 for all: "))
        characters = characters[:pinned]
    except ValueError:
        print("Invalid number, using all characters.")
        pinned = 100
    
    start_length = int(input("Enter the start length for combinations (e.g., 1): "))
    end_length = int(input("Enter the end length for combinations (e.g., 4): "))
    create_custom_array = input("Do you want to create a custom array? (yes/no): ").lower() == 'yes'
    
    if create_custom_array:
        custom_array = []
        print("Enter the indices for your custom character array:")
        for _ in range(pinned):
            index = int(input(f"Enter index {0 + 1}/{pinned} (0-indexed): "))
            custom_array.append(characters[index])
        characters = custom_array

    # Ensure the output directory exists
    output_directory = "llanguageMod/mappings"
    os.makedirs(output_directory, exist_ok=True)

    for length in range(start_length, end_length + 1):
        with open(f"{output_directory}/{length}.txt", "w") as file:
            print(f"Generating {length}-character combinations...")
            num_combinations = math.pow(len(characters), length)
            for i in range(int(num_combinations)):
                combination = ""
                temp = i
                for j in range(length):
                    combination = characters[temp % len(characters)] + combination
                    temp //= len(characters)
                file.write(f"{i} {combination}\n")

    print("Combinations generated successfully.")

# Example of how to call the function (uncomment the following line to use it in an actual script)
# Llanguage_model()


def read_mappings():
    """Reads mappings from files named 1.txt to 4.txt and stores them in a list of dictionaries."""
    mappings = [{} for _ in range(4)]
    for i in range(1, 5):
        try:
            with open(f"llanguageMod/mappings/{i}.txt", "r") as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        id_str, value_str = parts
                        mappings[i-1][value_str] = id_str
        except FileNotFoundError:
            print(f"Error opening file mappings/{i}.txt")
    return mappings

def process_files(input_directory, output_directory, start, end, mappings, outdir2):
    """Processes files within a given range using predefined mappings and generates output files."""
    max_file_number = max([int(os.path.splitext(os.path.basename(f))[0]) for f in glob.glob(f"{output_directory}/*.txt")], default=0)
    for i in range(start, end + 1):
        input_file_path = f"{input_directory}/{i}.txt"
        try:
            process_large_file(input_file_path, output_directory, mappings, max_file_number)
            process_large_file2(input_file_path, outdir2, mappings, max_file_number)
            max_file_number += 1
        except FileNotFoundError:
            print(f"Could not open the file {input_file_path}")

def process_large_file(input_file_path, output_directory, mappings, file_number):
    """Efficiently processes a large file using mappings and saves to an output file."""
    output_file_path = f"{output_directory}/{file_number + 1}.txt"
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        for line in input_file:
            output_content = convert_content(line, mappings)
            output_file.write(output_content)

def process_large_file2(input_file_path, output_directory, mappings, file_number):
    """Efficiently processes a large file using mappings and saves to an output file."""
    output_file_path = f"{output_directory}/{file_number + 1}.txt"
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        for line in input_file:
            output_b = convert_content2(line, mappings)
            output_file.write(output_b)
            

def convert_content(content, mappings):
    """Converts content using mappings."""
    output_content = ""
    index = 0
    while index < len(content):
        if content[index] == '\n':
            output_content += "1.27 "
            index += 1
            continue
        
        found = False
        for length in range(4, 0, -1):
            if index + length <= len(content):
                substr = content[index:index + length]
                if substr in mappings[length - 1]:
                    output_content += f"{length}.{mappings[length - 1][substr]} "
                    index += length
                    found = True
                    break
        if not found:
            output_content += "0 "
            index += 1
    return output_content

def convert_content2(content, mappings):
    """Converts content using mappings."""
    output_b = ""
    index = 0
    while index < len(content):
        if content[index] == '\n':
            output_b += "27 "
            index += 1
            continue
        
        found = False
        for length in range(4, 0, -1):
            if index + length <= len(content):
                substr = content[index:index + length]
                if substr in mappings[length - 1]:
                    #output_b += f"{length}.{mappings[length - 1][substr]} "
                    #output_b += f"{100**(length - 1) + (mappings[length-1])} "
                    if((length - 1) == 0):
                        output_b += f"{mappings[length-1][substr]} "
                    if((length - 1) == 1):
                        output_b += f"{100**(length - 1) + int(mappings[length-1][substr])} "
                    if((length - 1) == 2):
                        output_b += f"{100**(length - 1) + 100**(length - 2) + int(mappings[length-1][substr])} "
                    if((length - 1) == 3):
                        output_b += f"{100**(length - 1) + 100**(length - 2) + 100**(length - 3) + int(mappings[length-1][substr])} "
                    index += length
                    found = True
                    break
        if not found:
            output_b += "0 "
            index += 1
    return output_b 

#from PIL import Image

def save_image_as_pdf0(image, file_path):
    """
    Saves an image as a PDF file at the specified path.
    
    Args:
    image (PIL.Image): The image to save as a PDF.
    file_path (str): The full path where the PDF should be saved.
    """
    # Ensure the file path ends with '.pdf'
    if not file_path.lower().endswith('.pdf'):
        file_path += '.pdf'
    
    # Save the image as a PDF
    try:
        image.save(file_path, "PDF", resolution=100.0)
        print(f"Image successfully saved as PDF at {file_path}")
    except Exception as e:
        print(f"Failed to save image as PDF. Error: {e}")

####################
####################

def request_user_input(prompt, input_type=int):
    try:
        value = input_type(input(prompt))
        if input_type is int and value <= 0:
            print("Please enter a positive integer.")
            return request_user_input(prompt, input_type)
        return value
    except ValueError:
        print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        return request_user_input(prompt, input_type)

def generate_classical_circuit_from_line(line, filename):
    # Only take the part of the line after the colon if it exists
    gates = line.split(':')[-1].strip().split(', ')
    d = schemdraw.Drawing()
    gates = line.strip().split(', ')
    last_element = None
    last_output = None

    for i, gate in enumerate(gates):
        gate = gate.strip()
        if gate == 'AND':
            element = logic.And(inputs=2, label=f'AND{i}')
        elif gate == 'OR':
            element = logic.Or(inputs=2, label=f'OR{i}')
        elif gate == 'NOT':
            element = logic.Not(label=f'NOT{i}')
        elif gate == 'NAND':
            element = logic.Nand(inputs=2, label=f'NAND{i}')
        elif gate == 'NOR':
            element = logic.Nor(inputs=2, label=f'NOR{i}')
        elif gate == 'XOR':
            element = logic.Xor(inputs=2, label=f'XOR{i}')
        elif gate == 'XNOR':
            element = logic.Xnor(inputs=2, label=f'XNOR{i}')
        else:
            print(f"Unrecognized gate: {gate}")
            continue

        # Add the element to the drawing with the correct position
        if last_element is not None:
            element.at(last_output)
            #d += element.at(last_element.anchors['out'])
            
        else:
            d += element

        #last_output = element.anchors['out']

        # Update last_element to the current one
        ###last_element = d.elements[-1]  # Get the reference to the actual added element
        last_output = d.elements[-1].anchors['out']

    d.save(filename)    
    return d



# Function to prompt the user for the number of cells (gate layers)
def get_user_input(prompt, input_type=int):
    try:
        value = input_type(input(prompt))
        if input_type is int and value <= 0:
            print("Please enter a positive integer.")
            return get_user_input(prompt, input_type)
        return value
    except ValueError:
        print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        return get_user_input(prompt, input_type)

def generate_circuit_from_line(line, num_qubits):
    qc = QuantumCircuit(num_qubits)
    commands = line.strip().split(' ')[2:]  # Skip the 'Circuit X:' part
    for cmd in commands:
        gate, args = cmd.split('(')
        args = args.strip(')').split(',')

        if gate in ['x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg']:
            getattr(qc, gate)(int(args[0]))
        elif gate in ['rx', 'ry', 'rz']:
            if 'pi/2' in args[0]:
                angle = np.pi / 2
            else:
                angle = float(args[0])  # Assuming other angles are directly specified
            getattr(qc, gate)(angle, int(args[1]))
        elif gate == 'cx':
            getattr(qc, gate)(int(args[0]), int(args[1]))
    return qc

def generate_cmp():
    # Create the 'instructionSet.txt' file
    name_m = input("Enter the name for your command matrix: ")
    with open(name_m, 'w') as f:
        # Lines 1 to 13107: string_var# = input('Enter string_var: ')
        for i in range(13107):
            f.write(f"string_var{i} = input('Enter string_var: ')\n")
        
        # Lines 13108 to 26214: var_given# = input('Enter the variable name to be used: ')
        for i in range(13107):
            f.write(f"var_given{i} = input('Enter the variable name to be used: ')\n")
        
        # Lines 26215 to 39321: var_glob# = globals()[var_given#]
        for i in range(13107):
            f.write(f"var_glob{i} = globals().get(var_given{i}, 'Variable not found')  # Error handling: 'Variable not found'\n")
        
        # Lines 39322 to 52428: exec(var_glob#)
        for i in range(13107):
            f.write(f"if isinstance(var_glob{i}, str): exec(var_glob{i})  # Error handling: Execute only if it's a string\n")
        
        # Lines 52429 to 65535: eval(var_glob#)
        for i in range(13107):
            f.write(f"if isinstance(var_glob{i}, str): result = eval(var_glob{i})  # Error handling: Evaluate only if it's a string\n")
        
        # Line 65536: Hyperlink
        f.write("webbrowser.open('https://www.openai.com')")

    # Note: For logging, you can add a line to write the executed or evaluated command to a log file.
    # Note: For user authentication, you can add a line to check user credentials before executing or evaluating a command.
    
def text_editor():
    print("Simple Text Editor")
    file_path = input("Enter the path of the text file to edit (or a new file name to create): ")

    # Try to open the file and read its contents into 'lines'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.rstrip() for line in lines]  # Remove newline characters
    except FileNotFoundError:
        print("File not found. Starting with an empty file.")
        lines = []

    while True:
        print("\n1. Add text")
        print("2. View text")
        print("3. Update a line")
        print("4. Delete a line")
        print("5. Save changes")
        print("6. Exit without saving")
        choice = input("Choose an option: ")

        if choice == '1':
            text = input("Enter your text: ")
            lines.append(text)
            print("Text added successfully.")
        elif choice == '2':
            if lines:
                print("\nCurrent Text:")
                for i, line in enumerate(lines, 1):
                    print(f"{i}. {line}")
            else:
                print("The text is empty.")
        elif choice == '3':
            line_num = int(input("Enter the line number to update: ")) - 1
            if 0 <= line_num < len(lines):
                new_text = input("Enter the new text: ")
                lines[line_num] = new_text
                print("Line updated successfully.")
            else:
                print("Invalid line number.")
        elif choice == '4':
            line_num = int(input("Enter the line number to delete: ")) - 1
            if 0 <= line_num < len(lines):
                del lines[line_num]
                print("Line deleted successfully.")
            else:
                print("Invalid line number.")
        elif choice == '5':
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(f"{line}\n")  # Add newline characters when writing
            print("Changes saved successfully.")
            break  # Exit after saving
        elif choice == '6':
            print("Exiting without saving changes.")
            break
        else:
            print("Invalid choice. Please try again.")



def img_generator():
    print("random() : ", random.random())
    master = Tk()
    master.attributes('-fullscreen', True)
    #a = 250
    #b = 200
    print("Welcome\n")
    print("Tip: side width should be a factor of the image width, the same goes for the image height in relation to the side height of each pixel.")
    change1 = input("Enter side width of image block:  ")
    change = int(change1)
    change2 = input("Enter side height of image block:  ")
    change_h = int(change2)
    #a = 1880
    #b = 1050 
    a1 = input("Enter width of image: ")
    a = int(a1)
    b1 = input ("Enter height of image:  ")
    b = int(b1)
    pin_p1 = a/change
    pin_p2 = b/change_h
    w = Canvas(master, width= a, height= b)

    #c = ["purple", "green", "gold", "red", "yellow", "orange", "pink", "brown", "cyan", "lime", "teal", "magenta"]
    c = []
    while True:
        app_end = input("Enter colour Hex with # or colour name: ")
        c.append(app_end)
        
        conti_ = input("Enter 1 to add another colour, 0 to move on: ")
        if conti_ != '1':  # Breaks the loop if input is not '1'
            break
    xc = 0
    zerox = 0
    zeroy = 0
    p = 1
    range_for = int((a/change)*(b/change_h))
    name = 1
    cells = ((a//change)*(b//change_h))
    upper = cells - 1
    nbr_comb = math.pow(len(c),cells)
    files = int(nbr_comb)
    #print(len(c))
    rown = 0
    img_fn_prefix = input("Enter Image filename prefix (omit the file extension name): ")
    file_count = 0    
    for t in range(0,files):
        file_count = file_count + 1
        #if(file_count == 121):
        #    break
        switch = 1
        sw = 0
        #for x in range(range_for):
        #for x in range (0,cells):
        x = 0
        col = cells - 1
        #print(rown)
        while(x < cells):
            
            #f = open('%s.ps' % name, 'wb')
            #f.close
            if(switch == 1):
                row = 1
                nxleft = 0
                nxright = change
                nyleft = 0
                nyright = change_h
                zerox = 0
                zeroy = 0
            c_length = len(c)    
            switch = 0
            #ran = random.randint(0,c_length - 1)

            rdiv = math.pow(len(c),col)
            cell = (rown/rdiv) % (len(c))

            celled = int(cell)
            print(celled)

            #w.create_rectangle(zerox, nyleft, nxright,nyright, fill = c[celled], outline = "black", width = 0)
            w.create_rectangle(zerox, nyleft, nxright,nyright, fill = c[celled], outline = "black", width = 0)
            if(x <= cells):
                col = col - 1

            w.grid(row = zeroy, column = zerox + change)
            if(p >= pin_p1 and p%pin_p1 == 0):
                zeroy = zeroy + change_h
                zerox = -change
                #zerox = 0
                nxleft = change
                nxright = 0
                nyleft = nyleft + change_h
                nyright = nyright + change_h
            zerox = zerox + change
            p = p + 1
            #xc + 1
            nxright = nxright + change
            if(xc == 3):
                xc = 0
            x = x + 1    
        rown = rown + 1
        ce = str(name)
        w.update()
        #w.postscript(file = ce + ".ps", colormode='color')
        w.postscript(file=img_fn_prefix + ce + ".ps", colormode='color', x=0, y=0, width=a, height=b)
        name = name + 1

def compile_image_file():
    nof = input("Input number of files: ")
    nof_ = int(nof)
    ins_x = input("Enter first file id: ")
    x = int(ins_x)
    donu = input("Do you have more than one file (y [Yes], n [No]? ")
    if(donu == 'y'):
        ins_y = input("Enter last file id: ")
        y = int(ins_y)
    ins = input("Enter path of files: ")

    #def convert_to_png(path):
    pre = input("Enter filename-prefix: ")
    if(nof_ > 1):
        for i in range(x,y+1):
            ixy = str(i)
            #pre = input("Enter filename-prefix: ")
            path= ins + "\\" + pre + ixy + ".ps"
            img = Image.open(path)
            img.save(pre + ixy + ".png")
    if(nof_ == 1):
        #pre = input("Enter filename-prefix: ")
        path = ins + "\\" + pre + ins_x + ".ps"
        img = Image.open(path)
        img.save(pre + ins_x + ".png")

    print("Done")


    #master.mainloop()

def programming_engine():
    ####import pywebbrowser
    #create a custom event type
    MY_CUSTOM_EVENT = pygame.USEREVENT + 1

    # Initialize pygame
    pygame.init()

    # Initialize joystick module
    pygame.joystick.init()

    # Check if any joysticks are connected
    if pygame.joystick.get_count() > 0:
        # Get the first joystick
        joystick = pygame.joystick.Joystick(0)
        # Initialize the joystick
        joystick.init()

    # Set screen size
    #enter = int(input("Enter the dimension --> options 422, and multiples of 422"))
    enter = 422
    screen_width = enter
    screen_height = enter


    bls = 52
    screen = pygame.display.set_mode((screen_width, screen_height))
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    ##################

    #Create Commands
    bus_ = 255
    amount_ = (bus_ + 1) * (bus_ + 1)
    line_number_ = 0
                
    create_f = open("Command_Template.txt", "w")
    while(line_number_ < amount_):
        #i = log10(line_number)
        create_f.write("print(\"[Empty Command Slot] (Change using a text-editor to Update this slot in Command_Template.txt\") #remembering to rename Command_Template.txt\n")
        line_number_ = line_number_ + 1

    create_f.close()

    #LoadCommands
    xin = 0
    filnam = "Command_Template.txt"
    with open(filnam, 'r') as file:
        commands = file.readlines()
        xin = xin + 1


    star = [0]

    for i, command in enumerate(commands):
        commands[i] = command.strip()
        #cmd = command.split(",")
        star.append(command)
    del star[0]

    ###################

    ##################

    #LoadCoordinates
    xin2 = 0
    with open('Coordinates_Python.txt', 'r') as file2:
        commands2 = file2.readlines()
        xin2 = xin2 + 1


    starsx = [0]
    starsy = [0]

    for i2, command2 in enumerate(commands2):
        commands2[i2] = command2.strip()
        cmd2 = command2.split(",")
        starsx.append(int(cmd2[1]))
        varys = int(cmd2[2].strip())
        starsy.append(varys)
        
    del starsx[0]
    del starsy[0]

    """
    for i3, commandy in starsy:
        new = starsy[i3].strip()
        starsy[i3] = int(new)
    """

    print(starsx)
    print(starsy)
    ###################


    # Load images
    block_images = []
    for i in range(256):
        block_images.append(pygame.image.load(f"block{i+1}.png"))


    # Maze layout
    maze_layout = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]


    #Function to check if a position is inside the maze
    def is_inside_maze(x, y, maze_width, maze_height, bls):
        return 0 <= x < maze_width * bls and 0 <= y < maze_height * bls

    # Load player images
    player_image = pygame.image.load("player.png")
    player_image2 = pygame.image.load("player2.png")

    #scaled_block_images = [pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img in block_images]
    #scaled_player_image = pygame.transform.scale(player_image, (int(player_image.get_width() * scale_factor), int(player_image.get_height() * scale_factor)))


    # Set player position
    player_x = 0
    player_y = 0
    con_program = int(input("Continue? 1 [yes], 0 [no]: "))
    if(con_program == 1):
        print("Ok ...")
    if(con_program == 0):
        print("Exiting ...")
        exit()
    if(con_program != 0 and con_program != 1):
        print("Error")
        exit()
    # Set initial input type
    typei = "k"
    print("\n\nIn Local Command Mode\n\n")
    print("Switch Command Matrix [s],\n mouse [m],\nkeyboard arrows [k],\nD-Pad (Xbox One Controller) [d]\nPress [SPACEBAR] to call a command from Commands_Template.txt (Commands can be changed using a text-editor)  ... ")
    print("For mode 'd' A (sub-matrix start region) Then A (sub-matrix end region). Press start for help (Secure Internet Access Required).")
    # some input variable
    input_variable = 0
    # add the custom event to the event queue
    pygame.event.post(pygame.event.Event(MY_CUSTOM_EVENT, {"input_variable": input_variable}))
    #etch loop
    etch = 0

    #maze width
    maze_width = 16
    maze_height = 16
    # Main game loop
    running = True
    #new screen size settings
    ##screen_width, screen_height = pygame.display.get_surface().get_size()
    scale_factor_x = screen_width / maze_width
    #scale_factor_y = screen_height / maze_height
    #scale_factor = min(scale_factor_x, scale_factor_y)
    scale_factor = scale_factor_x

    bls = int(bls * 0.5)

    scaled_block_images = []

    # Before the main loop
    is_selecting_submatrix = False
    submatrix_start_pos = None
    selected_command = None
    execute_command_prompt = False

    for ni in range(256):
        s_i = pygame.transform.scale(block_images[ni], (bls, bls))
        block_images[ni] = s_i



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    ############
            elif event.type == pygame.KEYDOWN:
                # Check for key press event
                if event.key == pygame.K_m and typei != "m":
                    # Update input type
                    typei = "m"
                elif event.key == pygame.K_k and typei != "k":
                    # Update input type
                    typei = "k"
                elif event.key == pygame.K_s and typei != "s":
                    # Update input type
                    typei = "s"
                elif event.key == pygame.K_d and typei != "d":
                    # Update input type
                    typei = "d"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #update input_type
                        typei = "n"
                        #check for status
                        enter_cma = int(input("Enter command? 1[yes], 0 [no]: "))
                        """
                        # user input variable
                        if(enter_cma == 0):
                            typei = "k"
                            player_x = 0
                            player_y = 0
                            etch = 1
                        """
                        if(enter_cma == 0):
                            typei = "k"
                            player_x = 0
                            player_y = 0
                        if(enter_cma == 1):
                            input_variable = int(input("Enter command number ID (0 to 65535): "))
                        # add the custom event to the event queue
                        pygame.event.post(pygame.event.Event(MY_CUSTOM_EVENT, {"input_variable": input_variable}))
                        #pygame.event.post(pygame.event.Event(MY_CUSTOM_EVENT, {"input_variable": cma}))
                '''
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Get mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if the clicked position is inside the maze
                    if is_inside_maze(mouse_x, mouse_y, len(maze_layout[0]), len(maze_layout), bls):
                        # Calculate the clicked cell
                        cell_x = mouse_x // bls
                        cell_y = mouse_y // bls

                        # Execute the desired action (e.g., print a message with the image ID)
                        print(f"Hello, world! Image ID: {maze_layout[cell_y][cell_x]}")
                '''
         
            # check for custom event type
            for event in pygame.event.get(MY_CUSTOM_EVENT):
                # access the input variable from the event object
                cma = event.input_variable
                # do something with the input variable
                #pass...
                if(typei == 'n'):
                    
                    #enter_cma = int(input("Enter command? 1[yes], 0 [no]: "))
                    if(enter_cma == 1 and enter_cma != 0):
                        player_x = 0
                        player_y = 0
                        
                        # Clear screen
                        screen.fill((255, 255, 255))
                        # Update display
                        #pygame.display.update()
                        
                        #cma = int(input("Enter command number ID (0 to 65535): "))
                        try:
                            exec(star[cma], globals())
                        except:
                            print("Try again, there was an error")
                        #update command index pointer
                        bus = 255 + 1
                        if(cma <= 255):
                            cmd_index = 0
                            command_point = cma
                        elif(cma > 255):
                            cmd_index = cma//bus
                            command_point = cma
                            for tip in range(0, cmd_index):
                                command_point = command_point - (bus)
                        #print(command_point)

                        prompt = "Executing Command " + str(cma) + " from index: " + str(cmd_index)
                        print(prompt)
                        #print(starsx)
                        
                        player_x = starsy[cmd_index]
                        player_y = starsx[cmd_index]
                        command_point_x = starsy[command_point]
                        command_point_y = starsx[command_point]
                        
       

                        # Render player image at new position --> screen.blit(player_image, (player_x, player_y))

                        ####################

         

                        # Draw blocks
                        for y in range(int(screen_height/bls)):
                            for x in range(int(screen_width /bls)):
                                relative_x = x - player_x
                                relative_y = y - player_y
                                screen.blit(block_images[relative_x + relative_y * int(screen_width/bls)], (x * bls, y * bls))
                                #screen.blit(scaled_block_images[relative_x + relative_y * int(screen_width // (bls * scale_factor))], (x * bls * scale_factor, y * bls * scale_factor))

                        if(typei == 'n'):
                            #Draw2 player
                            screen.blit(player_image2, (player_x * bls, player_y * bls))
                            #Draw Command pointer
                            screen.blit(player_image, (command_point_x * bls, command_point_y * bls))
                            #screen.blit(scaled_player_image, (player_x * bls * scale_factor, player_y * bls * scale_factor))

                        # Update display
                        pygame.display.update()
                        
                        #cma = int(input("Enter command number ID (0 to 65535): "))
                        
                        ####################
            '''                
            if(typei == 'd'):
                # Check for Xbox controller input
                if pygame.joystick.get_count() > 0:
                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()
                    # Check for D-Pad input
                    dpad = joystick.get_hat(0)
                    if dpad == (1, 0):
                        player_x += 1
                    elif dpad == (-1, 0):
                        player_x -= 1
                    elif dpad == (0, 1):
                        player_y -= 1
                    elif dpad == (0, -1):
                        player_y += 1
                    if player_x < 0:
                        player_x = 0
                    if player_x >= int(screen_width / bls):
                        player_x = int(screen_width / bls) - 1
                    if player_y < 0:
                        player_y = 0
                    if player_y >= int(screen_height / bls):
                        player_y = int(screen_height / bls) - 1
            '''
            # Assuming your commands are laid out in a grid with a known width (e.g., 16 for a 16x16 grid)
            comp = 16  # Adjust this based on your actual layout
            copmy = 256
            # Inside the main loop, in the 'if(typei == 'd'):' block
            if(typei == 'd'):
                # Check for Xbox controller input
                if pygame.joystick.get_count() > 0:
                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()
                    # Check for D-Pad input
                    dpad = joystick.get_hat(0)
                    if dpad == (1, 0):
                        player_x += 1
                    elif dpad == (-1, 0):
                        player_x -= 1
                    elif dpad == (0, 1):
                        player_y -= 1
                    elif dpad == (0, -1):
                        player_y += 1
                    if player_x < 0:
                        player_x = 0
                    if player_x >= int(screen_width / bls):
                        player_x = int(screen_width / bls) - 1
                    if player_y < 0:
                        player_y = 0
                    if player_y >= int(screen_height / bls):
                        player_y = int(screen_height / bls) - 1

                    # Handling button presses for A, X, B, Y
                    buttons = joystick.get_numbuttons()
                    for i in range(buttons):
                        if joystick.get_button(i):
                            if i == 0:  # A button
                                if not is_selecting_submatrix:
                                    is_selecting_submatrix = True
                                    submatrix_start_pos = (player_x, player_y)
                                    print("Sub-matrix selection started at position:", submatrix_start_pos)
                                else:
                                    is_selecting_submatrix = False
                                    print("Sub-matrix selected:", submatrix_start_pos, "to", (player_x, player_y))
                                    
                            # Assuming index 7 represents the Start button; adjust if necessary
                            elif i == 7:  # Start button
                                print("Start button pressed. Executing command 65535 to access documentation (Secure Internet Access Required).")
                                # Assuming command 65535 takes the user to the documentation
                                exec(star[65535])
                                # Optionally, set a flag or take additional action as needed



            if(typei == 's'):
                
                ##################

                #LoadCommands
                xin = 0
                filnam = input("Enter name of Command Matrix file, 'filename.txt': ")
                quet = int(input("Enter 1 if file already exists [Read mode], Else Enter 2 [Write mode], choose carefully: "))
                
                bus = 255
                amount = (bus + 1) * (bus + 1)
                line_number = 0
                #ai = log10(amount)
                if(quet == 2):
                    create_f = open(filnam, "w")
                    while(line_number < amount):
                        #i = log10(line_number)
                        create_f.write("print(\"[Empty Command Slot] Change using a text-editor to Update this slot in Command_Template.txt after renaming it accordingly.\")\n")
                        line_number = line_number + 1

                    create_f.close()
                
                with open(filnam, 'r') as file:
                    commands = file.readlines()
                    xin = xin + 1

                star = [0]

                for i, command in enumerate(commands):
                    commands[i] = command.strip()
                    #cmd = command.split(",")
                    star.append(command)
                del star[0]
                
                #reset state of matrix
                typei = "k"
                player_x = 0
                player_y = 0
            
            if(typei == 'k'):
                # Get user keyboard input
                keys = pygame.key.get_pressed()

                # Update move flag based on keyboard input
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    move = True
                else:
                    move = False

                # Update player position based on keyboard input
                if(move):
                    if keys[pygame.K_LEFT]:
                        player_x -= 1
                    if keys[pygame.K_RIGHT]:
                        player_x += 1
                    if keys[pygame.K_UP]:
                        player_y -= 1
                    if keys[pygame.K_DOWN]:
                        player_y += 1
                    if player_x < 0:
                        player_x = 0
                    if player_x >= int(screen_width / bls):
                        player_x = int(screen_width / bls) - 1
                    if player_y < 0:
                        player_y = 0
                    if player_y >= int(screen_height / bls):
                        player_y = int(screen_height / bls) - 1
                    
            if(typei == 'm'):
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Update player position based on mouse position
                player_x = mouse_x // bls
                player_y = mouse_y // bls

        
        # Clear screen
        screen.fill((255, 255, 255))

        
        
        # Draw blocks
        if(typei == 'k' or typei == 'm' or typei == 'd'):
            for y in range(int(screen_height/bls)):
                for x in range(int(screen_width/bls)):
                    relative_x = x - player_x
                    relative_y = y - player_y
                    screen.blit(block_images[relative_x + relative_y * int(screen_width // (bls))], (x * bls, y * bls))
            if(typei == 'k' or typei == 'm' or typei == 'd'):
                screen.blit(player_image, (player_x * bls, player_y * bls))


        if(typei == 'k' or typei == 'm' or typei == 'd'):
            # Update display
            pygame.display.update()
        

    # Quit pygame
    pygame.quit()

def help_print():
    print("\nWelcome to Amalec, here are your options ...\n\n")
    print("\n\tProof is the absence of doubt. Guess not move. By way of the unbreakable Law. \n\tThis is the solution. That is which solves without the cause of one problem exclusively or problems.\n\nWritten by Mr. Dominic Alexander Cooper")
    print("\n\nEnter 0: Image generator (Required for the use of 2)")
    print("Enter 1: Image Compiler")
    print("Enter 2: Programming Engine")
    print("Enter 3: Cosmology (Useable with 0, 1 and 2)")
    print("Enter 4: Sequential Language Generation (Warning, you must filter out the profane. Also a user .txt file must exist within the working directory that lists (one character per line) Unicode characters: ")
    print("Enter 5: Text Editor")
    print("Enter 6: Generate Command Matrix Plugin for 2")
    print("Enter 7: Exit Program")
    print("Enter 8: 3D CAD CAM Engine")
    print("Enter 9: Quantum Circuit Qiskit WorkBench")
    print("Enter 10: Classical Circuit SchemDraw WorkBench")
    print("Enter 11: Cosmological Simulation by Text")
    print("Enter 12: Large Language Model")
    print("Enter 13: Data Script by Custom Structures")
    print("Enter 14: Generate Binary Unique Strings to a custom.txt file")
    print("Enter 16: outb file to binaryout file (Extension of 12)")
    print("Enter 17: Text Database")
    print("Enter 18: Proximal Prime Numbers")
    print("Enter 19: Configurations for Mode 2")
    print("Enter 21: Proximal Primes Animator")
    print("Enter 22: Manual Turing Complete Finite State Machine")
    print("Enter 23: Automatic Turing Complete Finite State Machine")
    print("Enter 24: Python Enabled Command Line Interface")
    print("Enter 25: Automatic Control Engineering")
    print("Enter 26: Automated Design and Technology")
    print("Enter 27: Construct your own Linguistic Language")
    print("Enter 28: Convert Text Encoding (From 12) to a Convergent Image")
    print("Enter 29: Mathematics Lab")
        
while(True):
    
    entrance = int(input("\n\n\tEnter your mode of operation (15 for available options): "))
    if(entrance == 0):
        img_generator()
    if(entrance == 1):
        compile_image_file()
    if(entrance == 2):
        programming_engine()
    if(entrance == 3):
        current_col = 0
        current_row = 0
        resized_images = []  # Global variable to store resized images

        # Rest of your code...
        # Global variable for the image selection frame
        image_selection_frame = None
        selected_image = None  # Global variable to hold the currently selected image
        # Global variable to keep track of the current mode
        current_mode = "draw_char"  # Possible values: "draw_char", "image_mode"

        def toggle_mode():
            global current_mode
            if current_mode == "draw_char":
                current_mode = "image_mode"
                canvas.bind("<Button-1>", on_canvas_click_for_image)  # Bind the image drawing function
            else:
                current_mode = "draw_char"
                canvas.bind("<Button-1>", lambda event: draw_char(event.y // square_size, event.x // square_size))  # Bind draw_char function

                
        def select_image(img):
            global selected_image
            selected_image = img
            # You can add additional logic here, e.g., updating the UI to indicate the selected image

        def resize_and_add_image(file_path, size):
            try:
                with Image.open(file_path) as img:
                    # Resize and add to the list
                    #resized_img = img.resize(size, Image.Resampling.LANCZOS)  # For Pillow versions 8.0.0 and later
                    # resized_img = img.resize(size, Image.LANCZOS)  # For older versions of Pillow
                    resized_img = img.resize(size, Image.LANCZOS)
                    resized_images.append(resized_img)
                #update_image_selection_area()
            except Exception as e:
                print(f"Error loading image: {e}")

        def on_canvas_click_for_image(event):
            col = event.x // square_size
            row = event.y // square_size
            draw_image_on_canvas(row, col)



        def draw_image_on_canvas(row, col):
            global selected_image_path, square_size

            if selected_image_path:
                try:
                    with Image.open(selected_image_path) as img:
                        resized_image = img.resize((square_size, square_size), Image.LANCZOS)
                        tk_image = ImageTk.PhotoImage(resized_image)
                        
                        x = col * square_size
                        y = row * square_size
                        canvas.create_image(x, y, image=tk_image, anchor='nw')

                        if not hasattr(canvas, 'images'):
                            canvas.images = []
                        canvas.images.append(tk_image)  # Keep a reference
                except Exception as e:
                    print(f"Error loading image: {e}")


        def update_image_selection_area():
            global image_selection_frame

            # Clear existing buttons in the frame
            for widget in image_selection_frame.winfo_children():
                widget.destroy()

            # Create buttons for each image
            for img in resized_images:
                tk_image = ImageTk.PhotoImage(img)
                btn = tk.Button(image_selection_frame, image=tk_image, command=lambda img=img: select_image(img))
                btn.image = tk_image  # Keep a reference to avoid garbage collection
                btn.pack(side='left')


        def select_and_add_images():
            global selected_image_path

            # Ask the user to enter the file path
            file_path = input("Enter the image file path: ")
            selected_image_path = file_path  # Store the path of the selected image

            # Define a target size for the images
            wid = int(input("Target Width: "))
            hei = int(input("Target Height: "))
            target_size = (wid, hei)  # You can change this size as needed

            if file_path:
                # Resize the image and add it to the canvas
                resize_and_add_image(file_path, target_size)

        def resize_and_add_image(file_path, size):
            try:
                with Image.open(file_path) as img:
                    # Resize and add to the list
                    resized_img = img.resize(size, Image.Resampling.LANCZOS)  # For Pillow versions 8.0.0 and later
                    resized_images.append(resized_img)
                #update_image_selection_area()
            except Exception as e:
                print(f"Error loading image: {e}")


        def select_and_resize_image():
            # Ask the user to select an image file
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            if not file_path:
                return  # User cancelled the dialog

            # Prompt the user for the new size
            new_size = simpledialog.askstring("Resize Image", "Enter new size (width,height):")
            if not new_size:
                return  # User cancelled the dialog

            try:
                # Parse the size input and resize the image
                width, height = map(int, new_size.split(','))
                resize_image(file_path, (width, height))
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")

        def resize_image(input_path, size):
            try:
                # Construct a new file name based on the original path
                dir_name, file_name = os.path.split(input_path)
                name, ext = os.path.splitext(file_name)
                output_path = os.path.join(dir_name, f"{name}_resized{ext}")

                # Open, resize, and save the image
                with Image.open(input_path) as img:
                    # Use Image.Resampling.LANCZOS for Pillow versions 8.0.0 and later
                    img = img.resize(size, Image.Resampling.LANCZOS)
                    # For older versions of Pillow, use Image.LANCZOS
                    # img = img.resize(size, Image.LANCZOS)
                    img.save(output_path)

                tk.messagebox.showinfo("Success", f"Image saved successfully to {output_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")



        def get_random_color():
            r = lambda: random.randint(0,255)
            return '#%02X%02X%02X' % (r(),r(),r())

        def get_random_char():
            random_int = random.randint(0x0021, 0x007E)
            return chr(random_int)

        def draw_grid():
            for i in range(grid_size):
                for j in range(grid_size):
                    color = get_random_color()
                    square = canvas.create_rectangle(j*square_size, i*square_size, (j+1)*square_size, (i+1)*square_size, fill=color)
                    char = get_random_char()
                    text = canvas.create_text(j*square_size + square_size/2, i*square_size + square_size/2, text=char, font=("Arial", 18), anchor="center")


        def draw_grid_IDE():
            global col
            try:
                for i in range(grid_size):
                    for j in range(grid_size):
                        color = "blue"
                        square = canvas.create_rectangle(j*square_size, i*square_size, (j+1)*square_size, (i+1)*square_size, fill=color, outline = "white")
                if typing_mode:
                    # In the function where you create the canvas...
                    canvas.bind("<Key>", on_key_press)
                    canvas.focus_set()
            except:
                print("Submit an app mode ...")


        def toggle_color_mode():
            """Toggles between manual color mode and random color mode"""
            global color_mode_var
            color_mode_var.set(not color_mode_var.get())

        font_size = 9

        def draw_char1(canvas, char, row, col, font_size, color):
            global cell_size, font_color, square_size, grid_size, last_drawn, note, char_note


            try:
                x = col * square_size + square_size / 2
                y = row * square_size + square_size / 2
                
                print(f"Drawing char '{char}' at ({x}, {y})")  # Debug print to check coordinates
                canvas.create_rectangle(col * square_size, row * square_size, (col+1) * square_size, (row+1) * square_size, fill=color)
                canvas.create_text(x, y, text=char, fill=font_color, font=('Calibri', int(font_size)))
                note = char_note.get()
                # Log the color and character info
                logging.info(f"Position:'{x};{y}',Xp:'{x}',Yp:'{y}',Character:'{char}',Square color:'{color}',Font color:'{font_color}',Note:'{note}'")
                # Log the color and character info in a text file
                if(note == ''):
                    note = "emptyNote"
                with open("color_log.txt", "a", encoding='utf-8') as login:
                    print(f"{x},{y},{char},{color},{font_color},{note}", file=login)

            except Exception as e:
                print(f"Something Went Wrong... Error: {e}")



        def draw_char(i=None, j=None):
            try:
                """Draws a character from input field in a specific square"""
                global char_count, IDE_mode, typing_mode, last_drawn, font_color
                if(mode == 'IDE'):
                    IDE_mode = True
                # Check if last_drawn is defined, otherwise define it
                if 'last_drawn' not in globals():
                    last_drawn = []

                # If i, j are not provided, calculate them based on char_count
                if i is None or j is None:
                    i, j = divmod(char_count, grid_size)
                    # Handle out-of-grid situations
                    if i >= grid_size or j >= grid_size:
                        print('Out of grid!')
                        return

                # Generate a random color if not in typing mode, white otherwise
                ##color = get_random_color() if not typing_mode else "white"

                # Check color mode
                if color_mode_var.get():
                    # Manual color mode
                    # Show a color picker and get the chosen color for the square
                    color = askcolor(title="Choose square color")[1]

                    # Ask for the font color
                    color_result = askcolor(title="Choose font color")
                    if color_result is not None:
                        font_color = color_result[1]
                    else:
                        # Handle the case when the user cancelled the color selection
                        font_color = "#000000"  # default to black, for example


                else:
                    # Random color mode
                    color = "#" + "".join([random.choice('0123456789ABCDEF') for i in range(6)])
                    color1 = "#" + "".join([random.choice('0123456789ABCDEF') for i in range(6)])
                    font_color = color1 #"#000000"


                square = canvas.create_rectangle(j*square_size, i*square_size, (j+1)*square_size, (i+1)*square_size, fill=color)
                char = char_entry.get()[:1]
                note = char_note.get()
                text = canvas.create_text(j*square_size + square_size/2, i*square_size + square_size/2, text=char, font=("Arial", font_size), fill=font_color, anchor="center")

                '''
                # Log the color and character info
                logging.info(f"Position:'{i};{j}',Xp:'{i}',Yp:'{j}',Character:'{char}',Square color:'{color}',Font color:'{font_color}'")
                # Log the color and character info in a text file
                with open("color_log.txt", "a") as login:
                    print(f"{i},{j},{char},{color},{font_color}", file=login)
                '''

                # Log the color and character info
                logging.info(f"Position:'{i};{j}',Xp:'{i}',Yp:'{j}',Character:'{char}',Square color:'{color}',Font color:'{font_color}',Note:'{note}'")
                # Log the color and character info in a text file
                if(note == ''):
                    note = "emptyNote"
                with open("color_log.txt", "a", encoding='utf-8') as login:
                    print(f"{i},{j},{char},{color},{font_color},{note}", file=login)

                
                if len(char_entry.get()) > 0:  # Check if there's more than one character
                    char_entry.delete(0, 1)  # Delete the first character

                last_drawn.append((square, text))

                if not IDE_mode:
                    char_count = (char_count + 1) % (grid_size * grid_size)
                    if char_count == 0:  # If we've filled the canvas, clear it
                        canvas.delete('all')

                return square, text
            except:
                print("Submit an app mode ...")


        def adjust_grid_and_font():
            global grid_size, square_size, font_size, canvas_width, current_row, current_col

            n_g_s = simpledialog.askstring("Change Grid Size (Grid Width)", "Enter New Grid Size (+Integer):")
            if(n_g_s != ''):
                new_grid_size = n_g_s
            n_f_s = simpledialog.askstring("Change Font Size (Default = 9)", "Enter New Font Size (+Integer):")
            if(n_f_s != ''):
                new_font_size = n_f_s
                # Update the global variables
            if(new_grid_size==None and new_font_size==None):
                grid_size = 10
                font_size = 9
            if((not new_grid_size==None) and (not new_font_size==None)):
                try: 
                    grid_size = int(new_grid_size)
                    square_size = canvas_width / grid_size
                    font_size = int(new_font_size)
                except:
                    print("positive integers please")
                
            '''
            # Get new values from input fields
            new_grid_size = grid_size_entry.get()
            new_font_size = font_size_entry.get()
            
            # Update the global variables
            grid_size = int(new_grid_size)
            square_size = canvas_width // grid_size
            font_size = int(new_font_size)
            '''

            # Redraw the grid
            refresh_canvas()
            qit = input("Are you in typing mode, or want to enter typing mode? 1 for (No), 2 for (yes): ")
            if(qit == '2'):
                current_row = 0
                current_col = 0
                show_typing_mode_menu()

        def refresh_canvas():
            """Clears the canvas and resets the char_count"""
            global char_count
            canvas.delete('all')
            char_count = 0
            draw_grid_IDE()
            last_drawn.clear()

        def undo_last():
            """Undoes the last drawing operation"""
            if last_drawn:
                square, text = last_drawn.pop()
                canvas.delete(square)
                canvas.delete(text)

        def update_canvas():
            if not paused.get():
                canvas.delete('all')
                draw_grid()
            root.after(8000, update_canvas)

        def toggle_typing_mode():
            global typing_mode, canvas

            typing_mode = not typing_mode
            if typing_mode:
                canvas.focus_set()  # Set focus to the canvas for keyboard input



        def on_canvas_click(event):
            try:
                global mode, typing_mode
                if mode == 'IDE' and not typing_mode:
                    j = event.x // square_size
                    i = event.y // square_size
                    draw_char(i, j)
                else:
                    paused.set(not paused.get())
            except:
                print("Submit an app mode ...")

        def on_key_press(event):
            global char_count, typing_mode
            if typing_mode:
                char_entry.delete(0, 'end')  # Clear the entry box
                try:
                    utf8_char = event.char.encode('utf-8').decode('utf-8')
                    char_entry.insert(0, utf8_char)  # Insert the typed character
                except UnicodeDecodeError:
                    print("Non UTF-8 character detected")
                    return
                draw_char()  # Draw the character
                char_count += 1  # Increment the count

                # If char_count exceeds the total number of squares in the grid, reset it
                if char_count >= grid_size ** 2:
                    char_count = 0




        def submit_mode():

            global char_count, mode, typing_mode
            
            mode = mode_entry.get().upper()
            
            '''
            if mode in ['editor']:

                typing_mode = False  # Start in clicking mode
                mode_entry.delete(0, 'end')  # Clear the input field
                mode_label.pack_forget()
                mode_entry.pack_forget()
                submit_button.pack_forget()
                
                draw_grid()
                char_label.pack()
                char_entry.pack()
                char_button.pack()

            '''    
                
            # Draw the initial grid
            if(mode != 'IDE'):
                print("A valid mode ...")

            '''
            if(mode == 'normal'):

                typing_mode = False  # Start in clicking mode
                mode_entry.delete(0, 'end')  # Clear the input field
                mode_label.pack_forget()
                mode_entry.pack_forget()
                submit_button.pack_forget()

                draw_grid()
                create_menu_1()

            if mode == 'normal':
                # Schedule the first update
                root.after(8000, update_canvas)
            '''
            
            if mode == 'IDE':

                typing_mode = False  # Start in clicking mode
                mode_entry.delete(0, 'end')  # Clear the input field
                mode_label.pack_forget()
                mode_entry.pack_forget()
                submit_button.pack_forget()
                
                char_count = 0
                draw_grid_IDE()
                
                control_frame.pack()
                char_label.pack()
                char_entry.pack()
                #grid_size_label.pack()
                #grid_size_entry.pack()
                #font_size_label.pack()
                #font_size_entry.pack()
                #adjust_button.pack()
                char_note_label.pack()
                char_note.pack()
                #refresh_button.pack(side="left")
                #undo_button.pack(side="left")
                #save_button = tk.Button(root, text='Save', command=save_canvas, bg="white", padx=5, pady=0)
                #save_button.pack(side="left")
                #save_Sbutton.pack(side="left")
                #load_button.pack(side="left")
                create_menu()


            return mode



        def save_canvas():
            global IC_value, xSwitch, ing
            xSwitch = 1
            ing = 1
            if(ing == 0):
                ing = 2
            ing = 1
            if(xSwitch == 1 and ing == 1):
                IC_value = 0
                ing = 0
            """Save the current state of the canvas to a .png file"""
            #filename = simpledialog.askstring("Save Canvas", "Enter filename:")
            filename = f"ImageCanvas{IC_value}_rename"
            
            if filename:  # Only save the canvas if a filename was entered
                # Get the bounding box of the canvas
                x = root.winfo_rootx() + canvas.winfo_x()
                y = root.winfo_rooty() + canvas.winfo_y()
                x1 = x + canvas.winfo_width()
                y1 = y + canvas.winfo_height()
                time.sleep(3)
                # Grab the image, crop it to the bounding box, and save it
                ImageGrab.grab().crop((x, y, x1, y1)).save(filename + ".png")


        def save_session():
            """Save the current session to a file using pickle"""
            global last_drawn
            # Ask the user to enter a filename
            filename = simpledialog.askstring("Save Session", "Enter filename:")
            if filename:  # Only save the session if a filename was entered
                session_data = [(canvas.coords(square), canvas.itemcget(square, "fill"),
                                canvas.coords(text), canvas.itemcget(text, "text"), canvas.itemcget(text, "fill"))
                                for square, text in last_drawn]
                with open(filename + ".pkl", "wb") as f:
                    pickle.dump(session_data, f)


        def load_session():
            """Load a saved session from a file using pickle"""
            global last_drawn
            # Ask the user to enter a filename
            filename = simpledialog.askstring("Load Session", "Enter filename:")
            if filename:  # Only try to load a session if a filename was entered
                try:
                    with open(filename + ".pkl", "rb") as f:
                        session_data = pickle.load(f)
                        # Clear the canvas and redraw all elements from the loaded session
                        canvas.delete('all')
                        draw_grid_IDE()
                        last_drawn = []
                        for square_coords, square_fill, text_coords, text_content, text_fill in session_data:
                            square = canvas.create_rectangle(*square_coords, fill=square_fill)
                            text = canvas.create_text(*text_coords, text=text_content, fill=text_fill, font=("Arial", font_size), anchor="center")
                            last_drawn.append((square, text))
                except FileNotFoundError:
                    print(f"No session named '{filename}' found.")

        #def exit_app():
        #    exit()

        def show_about():
            about_window = tk.Toplevel(root)
            about_window.title("About")
            about_msg = "This is a program created to learn and experiment with Tkinter. In IDE mode, you can draw characters on a grid (By typing or copying and pasting then clicking the squares you want to draw each character on), adjust the grid and font size, save and load sessions, and more, like saving the grid as an image (For example). C(num) was written with the aid of Chat GPT. Enjoy!\n\nNote: the workflow ... IDE to color_log.txt (Compiled by compile#.exe or compile#.py);\nindex_1.txt contains fields of study or research and development and\nindex_2.txt contains fields of study or research and development also ...\n\nBertotools Digital"
            tk.Message(about_window, text=about_msg, width=500).pack()
            tk.Button(about_window, text="OK", command=about_window.destroy).pack()

        def compileGOSmX():
            MAX_LINE_LENGTH = 256
            MAX_TOPICS = 256

            global index_1, index_2
            
            index_1 = [
                "Axiom",
                "Theorem",
                "Lemma",
                "Proposition",
                "Corollary",
                "Conjecture",
                "Proof",
                "Premise",
                "Conclusion",
                "Hypothesis",
                "Counterexample",
                "Direct Proof",
                "Indirect Proof",
                "Proof by Contradiction (Reductio ad absurdum)",
                "Proof by Induction",
                "Proof by Contrapositive",
                "Deductive Reasoning",
                "Inference",
                "Assumption",
                "Statement",
                "Postulate",
                "Proof by Exhaustion",
                "Syllogism",
                "Constructive Proof",
                "Non-Constructive Proof",
                "Trivial Proof",
                "Vacuous Proof",
                "Biconditional",
                "Condition",
                "Sufficiency",
                "Necessity",
                "Quantifier",
                "Universal Quantifier",
                "Existential Quantifier",
                "Bound Variable",
                "Free Variable",
                "Predicate",
                "Propositional Logic",
                "Modus Ponens",
                "Modus Tollens",
                "Discrete Mathematics",
                "Set Theory",
                "Function",
                "Bijection",
                "Injection",
                "Surjection",
                "Equivalence Relation",
                "Partial Order",
                "Total Order",
                "Well-Order",
                "Reflexivity",
                "Symmetry",
                "Transitivity",
                "Antisymmetry",
                "Completeness",
                "Compactness",
                "Connectedness",
                "Convergence",
                "Divergence",
                "Limit",
                "Sequence",
                "Series",
                "Monotonicity",
                "Cauchy Sequence",
                "Infinite Set",
                "Finite Set",
                "Cardinality",
                "Countable Set",
                "Uncountable Set",
                "Subset",
                "Superset",
                "Intersection",
                "Union",
                "Empty Set",
                "Power Set",
                "Cartesian Product",
                "Equivalence Class",
                "Partition",
                "Field",
                "Ring",
                "Group",
                "Abelian Group",
                "Non-abelian Group",
                "Matrix",
                "Vector Space",
                "Linear Transformation",
                "Eigenvalue",
                "Eigenvector",
                "Norm",
                "Inner Product",
                "Orthogonality",
                "Basis",
                "Dimension",
                "Rank",
                "Nullity",
                "Determinant",
                "Graph Theory",
                "Vertex",
                "Edge",
                "Connectivity",
                "Cycle",
                "Path",
                "Degree",
                "Subgraph",
                "Tree",
                "Forest",
                "Planar Graph",
                "Bipartite Graph",
                "Directed Graph (Digraph)",
                "Eulerian Graph",
                "Hamiltonian Graph",
                "Adjacency Matrix",
                "Incidence Matrix",
                "Isomorphism",
                "Homeomorphism",
                "Topology",
                "Open Set",
                "Closed Set",
                "Boundary",
                "Compact Space",
                "Hausdorff Space",
                "Continuity",
                "Differential",
                "Derivative",
                "Integral",
                "Partial Derivative",
                "Multivariable Calculus",
                "Laplace Transform",
                "Fourier Transform",
                "Taylor Series",
                "Maclaurin Series",
                "Conic Sections",
                "Hyperbola",
                "Ellipse",
                "Parabola",
                "Asymptote",
                "Limits at Infinity",
                "Complex Number",
                "Imaginary Unit",
                "Real Number",
                "Rational Number",
                "Irrational Number",
                "Prime Number",
                "Composite Number",
                "GCD (Greatest Common Divisor)",
                "LCM (Least Common Multiple)",
                "Permutation",
                "Combination",
                "Probability",
                "Statistics",
                "Expected Value",
                "Variance",
                "Standard Deviation",
                "Normal Distribution",
                "Poisson Distribution",
                "Binomial Distribution",
                "Hypothesis Testing",
                "Regression",
                "Correlation",
                "Matrix Algebra",
                "Linear Algebra",
                "Vector Calculus",
                "Optimization",
                "Algorithm",
                "Computational Complexity",
                "Big O Notation",
                "Pigeonhole Principle",
                "Principle of Inclusion-Exclusion",
                "Turing Machine",
                "Computability",
                "Unsolvability",
                "Parity",
                "Diophantine Equations",
                "Cryptography",
                "Fermat's Last Theorem",
                "Pythagorean Theorem",
                "Triangle Inequality",
                "Trigonometric Functions",
                "Trigonometric Identities",
                "Polar Coordinates",
                "Euler's Formula",
                "Riemann Zeta Function",
                "P vs NP Problem",
                "NP-complete Problem",
                "Stochastic Process",
                "Markov Chain",
                "Random Variable",
                "Conditional Probability",
                "Bayes' Theorem",
                "Monte Carlo Method",
                "Fractal",
                "Chaos Theory",
                "Game Theory",
                "Nash Equilibrium",
                "Zero-Sum Game",
                "Non-Zero-Sum Game",
                "Linear Programming",
                "Nonlinear Programming",
                "Quadratic Programming",
                "Dynamic Programming",
                "Integer Programming",
                "Graph Coloring",
                "Network Flow",
                "Spanning Tree",
                "Bellman-Ford Algorithm",
                "Dijkstra's Algorithm",
                "Kruskal's Algorithm",
                "Prim's Algorithm",
                "Floyd-Warshall Algorithm",
                "Euler's Method",
                "Runge-Kutta Method",
                "Numerical Integration",
                "Numerical Differentiation",
                "Bisection Method",
                "Newton's Method",
                "Secant Method",
                "Fixed Point Iteration",
                "Linear Interpolation",
                "Polynomial Interpolation",
                "Lagrange Interpolation",
                "Splines",
                "Fourier Series",
                "Laplace's Equation",
                "Heat Equation",
                "Wave Equation",
                "Schrodinger Equation",
                "Ordinary Differential Equation (ODE)",
                "Partial Differential Equation (PDE)",
                "Boundary Value Problem",
                "Initial Value Problem",
                "Green's Theorem",
                "Stoke's Theorem",
                "Divergence Theorem",
                "Curl",
                "Gradient",
                "Divergence",
                "Tensor",
                "Manifold",
                "Topological Space",
                "Measure Theory",
                "Lebesgue Integral",
                "Borel Set",
                "Hilbert Space",
                "Banach Space",
                "Category Theory",
                "Functor",
                "Natural Transformation",
                "Sheaf",
                "Homotopy",
                "Homology",
                "Cohomology",
                "Galois Theory",
                "Algebraic Geometry",
                "Topological K-Theory",
                "Knot Theory",
                "Lattice Theory"
            ]

            index_2 = [
                "Biochemistry",
                "Biophysics",
                "Molecular biology",
                "Genetics",
                "Immunology",
                "Cell biology",
                "Microbiology",
                "Neuroscience",
                "Pharmacology",
                "Bioinformatics",
                "Biotechnology",
                "Proteomics",
                "Genomics",
                "Structural biology",
                "Virology",
                "Systems biology",
                "Developmental biology",
                "Evolutionary biology",
                "Synthetic biology",
                "Metabolomics",
                "Epigenetics",
                "Tissue engineering",
                "Nanotechnology",
                "Materials science",
                "Quantum physics",
                "Condensed matter physics",
                "Particle physics",
                "Astrophysics",
                "Cosmology",
                "Optics",
                "Atomic and molecular physics",
                "Fluid mechanics",
                "Thermodynamics",
                "Environmental science",
                "Climate science",
                "Geology",
                "Oceanography",
                "Atmospheric science",
                "Ecology",
                "Conservation biology",
                "Botany",
                "Zoology",
                "Entomology",
                "Marine biology",
                "Paleontology",
                "Anthropology",
                "Archaeology",
                "Psychology",
                "Cognitive science",
                "Social psychology",
                "Linguistics",
                "Artificial intelligence",
                "Machine learning",
                "Computer vision",
                "Natural language processing",
                "Human-computer interaction",
                "Robotics",
                "Computer graphics",
                "Data science",
                "Mathematical modeling",
                "Mathematical physics",
                "Number theory",
                "Algebraic geometry",
                "Differential equations",
                "Computational physics",
                "Mathematical biology",
                "Operations research",
                "Biostatistics",
                "Epidemiology",
                "Cancer research",
                "Diabetes research",
                "Heart disease research",
                "Infectious diseases research",
                "Immunotherapy",
                "Stem cell research",
                "Gene therapy",
                "Drug discovery",
                "Precision medicine",
                "Health informatics",
                "Renewable energy",
                "Energy storage",
                "Sustainable materials",
                "Environmental engineering",
                "Water management",
                "Transportation engineering",
                "Civil engineering",
                "Chemical engineering",
                "Aerospace engineering",
                "Biomedical engineering",
                "Electrical engineering",
                "Mechanical engineering",
                "Robotics engineering",
                "Quantum computing",
                "Cryptography",
                "Cybersecurity",
                "Network engineering",
                "Telecommunications",
                "Human genetics",
                "Forensic science",
                "Space exploration and research",
                "Planetary science",
                "Astrobiology",
                "Astrochemistry",
                "Astrogeology",
                "Astroinformatics",
                "Exoplanet research",
                "Stellar evolution",
                "Galactic astronomy",
                "Observational astronomy",
                "Computational astrophysics",
                "Quantum chemistry",
                "Computational chemistry",
                "Organic chemistry",
                "Inorganic chemistry",
                "Physical chemistry",
                "Environmental chemistry",
                "Analytical chemistry",
                "Agricultural science",
                "Food science",
                "Nutritional science",
                "Exercise physiology",
                "Sports science",
                "Biomechanics",
                "Plant physiology",
                "Plant genetics",
                "Plant pathology",
                "Soil science",
                "Hydrology",
                "Geochemistry",
                "Geophysics",
                "Geomorphology",
                "Remote sensing",
                "Geotechnical engineering",
                "Petroleum engineering",
                "Aerospace materials",
                "Nanomaterials",
                "Polymer science",
                "Computational materials science",
                "Photonics",
                "Physical optics",
                "Quantum optics",
                "Neuroengineering",
                "Brain imaging",
                "Cognitive neuroscience",
                "Neuroinformatics",
                "Psychophysics",
                "Developmental psychology",
                "Personality psychology",
                "Clinical psychology",
                "Industrial-organizational psychology",
                "Educational psychology",
                "Psycholinguistics",
                "Human genetics",
                "Evolutionary genetics",
                "Population genetics",
                "Genetic engineering",
                "Genetic counseling",
                "Epigenomics",
                "Cardiovascular research",
                "Respiratory research",
                "Gastroenterology research",
                "Endocrinology research",
                "Nephrology research",
                "Hematology research",
                "Ophthalmology research",
                "Orthopedic research",
                "Dermatology research",
                "Veterinary medicine",
                "Animal behavior",
                "Conservation ecology",
                "Wildlife biology",
                "Environmental microbiology",
                "Agricultural economics",
                "Development economics",
                "Behavioral economics",
                "Econometrics",
                "Financial mathematics",
                "Operations management",
                "Supply chain management",
                "Industrial engineering",
                "Human-computer interaction",
                "Virtual reality",
                "Augmented reality",
                "Data mining",
                "Text mining",
                "Big data analytics",
                "Computational linguistics",
                "Quantum information science",
                "Quantum cryptography",
                "Biometrics",
                "Information retrieval",
                "Software engineering",
                "Computer networks",
                "Embedded systems",
                "Human-robot interaction",
                "Control systems",
                "Biopharmaceuticals",
                "Drug delivery systems",
                "Clinical trials",
                "Regenerative medicine",
                "Agricultural biotechnology",
                "Plant breeding",
                "Animal breeding",
                "Food technology",
                "Sensory science",
                "Poultry science",
                "Aquaculture",
                "Marine ecology",
                "Limnology",
                "Population ecology",
                "Landscape ecology",
                "Evolutionary ecology",
                "Environmental toxicology",
                "Environmental chemistry",
                "Environmental microbiology",
                "Ecotoxicology",
                "Green chemistry",
                "Space physics",
                "Space weather",
                "Astrostatistics",
                "Computational fluid dynamics",
                "Mathematical optimization",
                "Operations research",
                "Human genetics",
                "Functional genomics",
                "Molecular genetics",
                "Cancer genetics",
                "Psychiatric genetics",
                "Population genomics",
                "Bioengineering",
                "Biomaterials",
                "Biomechatronics",
                "Cardiovascular engineering",
                "Neural engineering",
                "Rehabilitation engineering",
                "Genetic engineering",
                "Environmental engineering",
                "Water resources engineering",
                "Structural engineering",
                "Robotics engineering",
                "Quantum information theory",
                "Quantum simulation",
                "Quantum sensing",
                "Geographical information systems (GIS)",
                "Urban planning",
                "Renewable energy systems",
                "Solar cell technology",
                "Wind energy research",
                "Energy policy and economics",
                "Computational neuroscience",
                "Neurobiology",
                "Cognitive neuroscience",
                "Systems neuroscience",
                "Human-robot interaction",
                "Evolutionary psychology",
                "Social network analysis"
            ]



            def square_print_topic_indices(r_value, g_value, b_value, file):
                index1 = r_value % len(index_1)
                index2 = g_value % len(index_1)
                index3 = b_value % len(index_1)
                '''
                file.write(f"\t\t\t{topics[index1]}\n")
                file.write(f"\t\t\t{topics[index2]}\n")
                file.write(f"\t\t\t{topics[index3]}\n")
                '''
                file.write(f"\t\t\t{index_1[index1]}\n")
                file.write(f"\t\t\t{index_1[index2]}\n")
                file.write(f"\t\t\t{index_1[index3]}\n")
                        
                squareRatio = str(index1) + ":" + str(index2) + ":" + str(index3)
                return squareRatio

            def font_print_topic_indices(r_value, g_value, b_value, file):
                index1_ = r_value % len(index_2)
                index2_ = g_value % len(index_2)
                index3_ = b_value % len(index_2)
                file.write(f"\t\t\t{index_2[index1_]}\n")
                file.write(f"\t\t\t{index_2[index2_]}\n")
                file.write(f"\t\t\t{index_2[index3_]}\n")

                fontRatio = str(index1_) + ":" + str(index2_) + ":" + str(index3_)
                return fontRatio



            def get_index(i, j, grid_size):
                return i * grid_size + j

            def extract_rgb_values(color):
                if len(color) != 7 or color[0] != '#':
                    raise ValueError('Input should be a hex color code in the format "#RRGGBB"')
                try:
                    red = int(color[1:3], 16)
                    green = int(color[3:5], 16)
                    blue = int(color[5:7], 16)
                    return red, green, blue
                except ValueError:
                    raise ValueError('Invalid color code. RGB values should be hex digits (0-9, A-F)')


            def GO():
                log_file = "color_log.txt"
                ##        topic_file = "index_1.txt"
                ##        topic2_file = "index_2.txt"  # Corrected this line to read from a different file
                gridWidth = int(input("Enter gridWidth: "))
                # Read topic files to get the topics and topic2s
                ##        with open(topic_file, "r", encoding='utf8') as file:
                ##            topics = [line.strip() for line in file]
                ##
                ##        with open(topic2_file, "r", encoding='utf8') as file:
                ##            topic2s = [line.strip() for line in file]

                numTopics = len(index_1)
                numTopic2s = len(index_2)

                # Read color log file
                with open(log_file, "r") as file:
                    lines = file.readlines()

                lineNumber = 0
                # Save output to a file
                output_file = "output.txt"
                with open(output_file, "w") as file:
                    print()
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        xcoor = int(parts[1])
                        ycoor = int(parts[0])
                        index_ = (gridWidth * ycoor) + xcoor
                        character = parts[2]
                        squareColor = parts[3]
                        fontColor = parts[4]
                        notes = parts[5]

                        # Extract RGB values from squareColor
                        red, green, blue = extract_rgb_values(squareColor)

                        # Extract RGB values from fontColor
                        fontRed, fontGreen, fontBlue = extract_rgb_values(fontColor)

                        # Calculate the grid size
                        grid_size = int(parts[0])

                        # Select topics based on RGB values from squareColor
                        topicIndices = [(red + get_index(i, j, grid_size)) % numTopics for i in range(grid_size) for j in range(grid_size)]
                        
                        lineNumber += 1

                        
                        with open(output_file, "a") as file:
                            file.write(f"Compiling Line/s: {lineNumber}\n\n")
                            file.write(f"Line({lineNumber})\n\n")
                            file.write(f"0\tLineNumber: {lineNumber}\tx-coordinate: {xcoor}\ty-coordinate: {ycoor}\t Character: {character}\tRGB: {squareColor}\tRGB: {fontColor}\t Note: {notes}\t GridDimensions: {gridWidth}x{gridWidth}\n\n")
                            #print(topicIndices)
                            file.write(f"Line/s({lineNumber}) Output:\n\n")
                            file.write(f"#define Line({lineNumber}){{\n\n")
                            # Inside the main function
                            file.write(f"\ti_1_0(squareColor){{\n\n")
                            file.write(f"\t\t{character}\n")
                            file.write(f"\t\t(R: {red}, G: {green}, B: {blue})\n")
                            s_ratio = square_print_topic_indices(red, green, blue, file)
                            #square_print_topic_indices(red, green, blue, topics, file)   # Modify this line
                            file.write("\t\t)\n")
                            file.write("\t};\n\n")
                            file.write(f"\ti_1_1(fontColor){{\n\n")
                            file.write(f"\t\t{character}\n")
                            file.write(f"\t\t(R: {fontRed}, G: {fontGreen}, B: {fontBlue})\n")
                            f_ratio = font_print_topic_indices(fontRed, fontGreen, fontBlue, file)
                            #font_print_topic_indices(fontRed, fontGreen, fontBlue, topic2s, file)   # And this line
                            file.write("\t\t)\n")
                            file.write(f"\treturn squareRatio({s_ratio}), fontRatio({f_ratio}), sqaureIndex({index_})\n")
                            #file.write(f"\treturn fontRatio({f_ratio})\n")
                            file.write("}\n\n")


            GO()


        def create_menu():
            global control_frame
            def home():
                canvas.pack_forget()
                menubar.destroy()
                control_frame.pack()
                char_entry.pack_forget()
                char_label.pack_forget()
                #grid_size_label.pack_forget()
                #grid_size_entry.pack_forget()
                #font_size_label.pack_forget()
                #font_size_entry.pack_forget()
                #adjust_button.pack_forget()
                char_note.pack_forget()
                char_note_label.pack_forget()

                root.destroy()
                switch = 1
                setup_mode(switch)
            
            # Create a menubar
            menubar = tk.Menu(root)

            # Create an options menu and add it to the menubar
            options_menu = tk.Menu(menubar, tearoff=0)
            #menubar.add_cascade(label="Options", menu=options_menu)

            # Create a dropdown menu and add it to the menubar
            dropdown = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Options", menu=dropdown) # Use a different label, e.g., "Dropdown"

            # Add commands to dropdown menu
            
            # Add checkbutton to options menu
            dropdown.add_command(label="Toggle Manual/Random Colour", command=manual_colour)

            dropdown.add_command(label="Refresh", command=refresh_canvas)
            dropdown.add_command(label="Undo", command=undo_last)
            dropdown.add_command(label="Save Session", command=save_session)
            dropdown.add_command(label="Load Session", command=load_session)
            dropdown.add_command(label="Save as Image", command=save_canvas)
            dropdown.add_command(label="Compile Canvas", command=compileGOSmX)
            # Add the new command for resizing images
            dropdown.add_command(label="Select and Resize Image", command=select_and_resize_image)
            # Add the command for selecting images
            dropdown.add_command(label="Select Images", command=select_and_add_images)
            # Add the toggle mode command
            dropdown.add_command(label="Toggle Draw Chars/Images", command=toggle_mode)
            #dropdown.add_command(label="Exit", command=exit_app)
            #dropdown.add_command(label="Toggle Type/Click Mode", command=toggle_typing_mode)
            dropdown.add_command(label="About Program", command=show_about)
            dropdown.add_command(label="Go Home", command=home)
            dropdown.add_command(label="Edit Grid Dimensions", command=adjust_grid_and_font)
            dropdown.add_command(label="Typing Mode", command=show_typing_mode_menu)


            # Set the menubar
            root.config(menu=menubar)

            

        def create_menu_1():
            global control_frame
            def home1():
                canvas.pack_forget()
                menubar1.destroy()
                root.destroy()
                switch = 1
                setup_mode(switch)
                
            
            # Create a menubar
            menubar1 = tk.Menu(root)

            # Create an options menu and add it to the menubar
            options_menu1 = tk.Menu(menubar1, tearoff=0)
            #menubar.add_cascade(label="Options", menu=options_menu)

            # Create a dropdown menu and add it to the menubar
            dropdown = tk.Menu(menubar1, tearoff=0)
            menubar1.add_cascade(label="Options", menu=dropdown) # Use a different label, e.g., "Dropdown"

            # Add commands to dropdown menu
            
            # Add checkbutton to options menu
            dropdown.add_command(label="About Program", command=show_about)
            dropdown.add_command(label="Change Mode", command=home1)

            # Set the menubar
            root.config(menu=menubar1)


        def manual_colour():
            # Toggle the value of color_mode_var
            current_value = color_mode_var.get()
            color_mode_var.set(not current_value)


        '''
        # Create a tkinter window
        root = tk.Tk()
        root.title("General Operating System")
        root.iconbitmap("logo.ico")
        '''

        def show_typing_mode_menu():
            global color_
            while True:
                print("1. Use default UTF-8 mapping")
                print("4. Exit")
                choice = input("Choose an option: ")
                
                if choice == "1":
                    # Use default UTF-8 mapping
                    print("Using default UTF-8 mapping.")
                    color_ = input("Use Default Colour Scheme (1): ")
                    if(color_ == '1'):
                        # Initialize bg_color and font_color with default values at the global scope
                        bg_color = "#FFFFFF"  # Default white background color
                        font_color = "#000000"  # Default black font color
                        break
                else:
                    print("Invalid choice. Please try again.")

            canvas.bind("<Key>", type_character)
            canvas.focus_set()





        def set_background_color():
            global color
            #bg_color = tk.colorchooser.askcolor()[1]
            color = input("Enter background color (#FFFFFF for example):")
            
        def set_font_color():
            global font_color, font_size
            #font_color = tk.colorchooser.askcolor()[1]
            font_color = input("Enter background color (#000000 for example): ")
            font_size = input("Enter font_size: ")


        def type_character(event):
            global current_row, current_col, col, font_size, font_color, color, canvas_width, square_size
            color = "#FFFFFF"
            font_color = "#000000"
            char = event.char
            if char:  # Ignore non-character events
                try:
                    
                    draw_char1(canvas, char, current_row, current_col, font_size, color)
                    current_col += 1
                    if (current_col >= canvas_width/square_size):
                        current_col = 0
                        current_row += 1
                    if(current_row >= canvas_width/square_size):
                        current_col = 0
                        current_row = 0
                except Exception as e:
                    print("Something Went Wrong...")
                    print(e)

                
                


        def setup_mode(sw):

            global mode_entry, mode_label, square_size, grid_size, char_count, last_drawn
            global root, color_mode_var, logging, paused, canvas_width, canvas_height, canvas
            global grid_size_label, grid_size_entry, font_size_label, font_size_entry, adjust_button
            global save_Sbutton, load_button, char_label, char_entry, char_note_label, char_note, char_button
            global refresh_button, undo_button, control_frame, submit_button, col, color_
            global image_selection_frame  # Use the global variable



            current_row = 0
            current_col = 0
            color_ = 1
            
            # Define the size of the squares and the grid
            #square_size = 70
            square_size = int(input("Enter sub-square size: "))
            #grid_size = 10
            grid_size = int(input("Enter grid size by the number of sub-squares: "))
            char_count = 0
            last_drawn = []

            window_height = square_size * grid_size + (square_size * 2)
            window_width = square_size * grid_size
            

            if(sw == 1):
                # Create a tkinter window
                root = tk.Tk()
                # Define the frame for displaying the image selection
                #image_selection_frame = tk.Frame(root)
                #image_selection_frame.pack(side='top')  # Adjust the side as per your layout
                root.title("C")
                #root.iconbitmap("logo.ico")
                sw = 0
                switch = 0

            ###


            # Get screen width and height
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            # Calculate position of the window
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            
            # Set the dimensions of the window and where it is placed
            root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

            ###

            # Create a BooleanVar for the color mode and set it to False initially
            color_mode_var = BooleanVar(value=False)

            # Setup logging
            logging.basicConfig(filename='logging.txt', level=logging.INFO)

            paused = tk.BooleanVar()
            paused.set(False)

            canvas_width = grid_size * square_size
            canvas_height = grid_size * square_size
            canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
            col = canvas_width
            canvas.pack()
            canvas.bind("<Button-1>", on_canvas_click)
            
            # In the function where you create the canvas...
            canvas.bind("<Key>", on_key_press)
            canvas.focus_set()
            
            # Create input fields and buttons for grid and font size input
            grid_size_label = tk.Label(root, text="Grid size:")
            grid_size_entry = tk.Entry(root, width=5)
            font_size_label = tk.Label(root, text="Font size:")
            font_size_entry = tk.Entry(root, width=5)
            adjust_button = tk.Button(root, text='Adjust Grid & Font', command=adjust_grid_and_font)

            # Create the save and load buttons
            save_Sbutton = tk.Button(root, text='Save Session', command=save_session, bg="white", padx=5, pady=0)
            load_button = tk.Button(root, text='Load Session', command=load_session, bg="white", padx=5, pady=0)

            # Create input fields and buttons for mode and character input
            mode_label = tk.Label(root, text="Enter ... 'IDE' for an\nInteractive Development Environment\nfor Learning anything!")
            mode_entry = tk.Entry(root)
            submit_button = tk.Button(root, text='LEARN', command=submit_mode)


            '''
            filename = simpledialog.askstring("Save Canvas", "Enter filename:")
            if filename:
            '''
            
            char_label = tk.Label(root, text="Enter symbol/s to draw: ")
            char_entry = tk.Entry(root, width=12)
            char_note_label = tk.Label(root, text="Enter Note: ")
            char_note = tk.Entry(root, width=12)
            #char_button = tk.Button(root, text='Draw Character', command=draw_char)

            refresh_button = tk.Button(root, text='Refresh', command=refresh_canvas, bg="white", padx=5, pady=0)
            undo_button = tk.Button(root, text='Undo', command=undo_last, bg="white", padx=5, pady=0)

            control_frame = tk.Frame(root)

            mode_label.pack()
            mode_entry.pack()
            submit_button.pack()
            # create_menu(root)

            # Run the tkinter main loop
            root.mainloop()

        global switch
        switch = 1


        setup_mode(switch)
        
    if(entrance == 4):
        #language()
        def get_subranges_from_user():
            subranges = []
            number_of_subranges = int(input("Enter the number of subranges: "))

            for i in range(number_of_subranges):
                lower_bound = int(input(f"Enter the lower bound of subrange {i + 1}: "))
                upper_bound = int(input(f"Enter the upper bound of subrange {i + 1}: "))
                subranges.append((lower_bound, upper_bound))

            return subranges

        def main():
            print("(pt) == Universal Set = Computer")

            # Read the file
            gettext = input("Enter filename of the .txt file containing single characters per line (Unicode Characters): ")
            #with open("alpha.txt", "r", encoding="utf-8") as alpha_file:
            with open(gettext, "r", encoding="utf-8") as alpha_file:
                file_characters = [line.strip() for line in alpha_file if line.strip()]

            subranges = get_subranges_from_user()
            a = []

            for subrange in subranges:
                lower_bound = max(0, subrange[0] - 1)
                upper_bound = min(len(file_characters) - 1, subrange[1] - 1)
                a.extend(file_characters[lower_bound:upper_bound + 1])

            print("Characters have been added to the array from the specified subranges.")

            choice = input("Enter a to use your subrange of characters. Else, Enter e to Exit: ")
            if choice.lower() == 'a':
                z = int(input("Enter the size of your array: "))
                k = z - 1

                noc = int(input("\nEnter n: "))
                print(f"\nNumber Of FILE Cells = {noc}")
                n = noc

                id = 0

                with open("LSC-RENAME.txt", "w", encoding="utf-8") as p:
                    ai = int(input("\nEnter nth File System (Number of Cells Per File of the nth File System). Let the value be equal to n for a progressionless session: "))

                    for n in range(n, ai + 1):
                        nbr_comb = int(math.pow(k + 1, n))

                        for row in range(nbr_comb):
                            p.write(f"\n\n{n}CF{id}\n\n")
                            id += 1
                            for col in range(n - 1, -1, -1):
                                rdiv = int(math.pow(k + 1, col))
                                cell = (row // rdiv) % (k + 1)

                                if cell < len(a):
                                    if col == 0:
                                        p.write(f"{a[cell]}")
                                    else:
                                        p.write(f"{a[cell]} ")

        if __name__ == "__main__":
            main()

    if(entrance == 5):
        text_editor()
    if(entrance == 6):
        generate_cmp()
    if(entrance == 7):
        break
    if(entrance == 8):
        class Point:
            def __init__(self, material, x, y, z, x_i, y_i, z_i, id_number):
                self.material = material
                self.x = x  # x-coordinate relative to the origin
                self.y = y  # y-coordinate relative to the origin
                self.z = z  # z-coordinate relative to the origin
                self.x_i = x_i  # x-coordinate of the origin
                self.y_i = y_i  # y-coordinate of the origin
                self.z_i = z_i  # z-coordinate of the origin
                self.id_number = id_number

            def __str__(self):
                return f"Point(ID: {self.id_number}, Material: {self.material}, Relative: ({self.x}, {self.y}, {self.z}), Origin: ({self.x_i}, {self.y_i}, {self.z_i}))"

            def log_entry(self):
                return f"{self.material} {self.x} {self.y} {self.z} {self.x_i} {self.y_i} {self.z_i} {self.id_number}\n"


        class Structure:
            def __init__(self):
                self.points = []
                self.next_id = 1
                self.load_points_from_log()

            def load_points_from_log(self):
                try:
                    with open("logs.txt", "r") as log_file:
                        for line in log_file:
                            parts = line.split()
                            if len(parts) == 8:
                                material, x, y, z, x_i, y_i, z_i, id_number = parts
                                # Convert string to appropriate types
                                point = Point(
                                    material,
                                    #int(x), int(y), int(z),
                                    #int(x_i), int(y_i), int(z_i),
                                    float(x), float(y), float(z),
                                    float(x_i), float(y_i), float(z_i),
                                    int(id_number)
                                )
                                self.points.append(point)
                                # Update the next ID to be larger than any ID already used
                                self.next_id = max(self.next_id, point.id_number + 1)
                except FileNotFoundError:
                    print("logs.txt file not found. Starting with an empty structure.")

            def add_point(self, material, x, y, z, x_i, y_i, z_i):
                point = Point(material, x, y, z, x_i, y_i, z_i, self.next_id)
                self.points.append(point)
                self.next_id += 1
                # Log the new point
                with open("logs.txt", "a") as log_file:
                    log_file.write(point.log_entry())

            '''
            def add_point(self, material, x, y, z, x_i, y_i, z_i):
                point = Point(material, x, y, z, x_i, y_i, z_i, self.next_id)
                self.points.append(point)
                with open("logs.txt", "a") as log_file:
                    log_file.write(point.log_entry())
                self.next_id += 1  # Prepare ID for the next point
            '''

            def __str__(self):
                return "\n".join(str(point) for point in self.points)

            def plot_structure(self, point_id=None):
                x_coords = [point.x + point.x_i for point in self.points]
                y_coords = [point.y + point.y_i for point in self.points]
                z_coords = [point.z + point.z_i for point in self.points]

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                scatter = ax.scatter(x_coords, y_coords, z_coords, color='red')

                if point_id is not None:
                    # If a point ID is specified, zoom in on that point
                    point = next((p for p in self.points if p.id_number == point_id), None)
                    if point:
                        ax.set_xlim(point.x + point.x_i - 5, point.x + point.x_i + 5)
                        ax.set_ylim(point.y + point.y_i - 5, point.y + point.y_i + 5)
                        ax.set_zlim(point.z + point.z_i - 5, point.z + point.z_i + 5)
                        # Highlight the selected point
                        ax.scatter([point.x + point.x_i], [point.y + point.y_i], [point.z + point.z_i], color='blue', s=100)
                    else:
                        print(f"No point found with ID {point_id}")

                # Set the axes labels
                ax.set_xlabel('X Label')
                ax.set_ylabel('Y Label')
                ax.set_zlabel('Z Label')
                plt.title('3D Plot of Points in Structure')

                # Show the plot
                plt.show()

        class Interface:
            def __init__(self):
                self.structure = Structure()

            def process_command(self, command):
                parts = command.split()
                if parts[0] == "add_point":
                    # Expecting command format: add_point material x y z x_i y_i z_i
                    if len(parts) != 8:
                        print("Invalid number of arguments for add_point. Expected format: add_point material x y z x_i y_i z_i")
                        return
                    try:
                        #self.structure.add_point(parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]), int(parts[6]), int(parts[7]))
                        self.structure.add_point(parts[1], float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7]))
                    except ValueError:
                        print("Invalid input ...")

                elif parts[0] == "plot":
                    #self.load_point_from_log()
                    self.structure.plot_structure()

                elif parts[0] == "zoom_on_point":
                    #self.load_point_from_log()
                    if len(parts) < 2 or not parts[1].isdigit():
                        print("Invalid command. Usage: zoom_on_point <point_id>")
                        return
                    point_id = int(parts[1])
                    self.structure.plot_structure(point_id=point_id)

                else:
                    print("Unknown command")

            def run(self):
                print("Available Commands:")
                print("\tadd_point material x y z x_i y_i z_i")
                print("\tplot")
                print("\tzoom_on_point <point_id>")
                print("\tprint_structure")
                print("\texit")
                while True:
                    command = input("Enter command: ")
                    if command.lower() == "exit":
                        break
                    if command.lower() == "print_structure":
                        print(self.structure)
                    else:
                        self.process_command(command)


        # Main loop
        interface = Interface()
        interface.run()
    
    if(entrance == 9):
        while(5 > 4):
            mode = get_user_input("Enter 1 to generate new circuits, 2 to generate .png from existing file, 3 to exit: ", int)

            if mode == 1:
                # Generate new circuits and save them to a file
                qbits = int(input("Enter number of qubites per circuit configuration (Positive Integer): "))
                gates = ['x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg', 'rx', 'ry', 'rz', 'cx']
                num_qubits = qbits  # Number of qubits in the circuit
                num_cells = get_user_input("Enter the number of cells (gate layers) per circuit: ")

                with open('source.txt', 'w') as file:
                    gate_combinations = product(gates, repeat=num_cells * num_qubits)

                    for idx, combo in enumerate(gate_combinations):
                        qc = QuantumCircuit(num_qubits)
                        gate_sequence = ""
                        for i, gate in enumerate(combo):
                            qubit = i % num_qubits
                            if gate in ['x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg']:
                                getattr(qc, gate)(qubit)
                                gate_sequence += f"{gate}({qubit}) "
                            elif gate == 'cx':
                                getattr(qc, gate)(qubit, (qubit + 1) % num_qubits)
                                gate_sequence += f"{gate}({qubit},{(qubit + 1) % num_qubits}) "
                            elif gate in ['rx', 'ry', 'rz']:
                                getattr(qc, gate)(np.pi/2, qubit)
                                gate_sequence += f"{gate}(pi/2,{qubit}) "

                        file.write(f"Circuit {idx}: {gate_sequence.strip()}\n")
                        print(f"Saved configuration for Circuit {idx}")

            elif mode == 2:
                # Generate .png files from an existing .txt file
                filename = get_user_input("Enter the name of the source file (including .txt extension): ", str)
                qbits = get_user_input("Enter number of qubits per circuit configuration (Positive Integer): ")
                num_qubits = qbits  # Use this for constructing QuantumCircuit instances

                print("Enter the line numbers or ranges (e.g., 1-3, 5, 7-10) to generate .png files:")
                line_numbers = input("Line numbers/ranges: ").split(',')  # Direct input call for complex string input

                with open(filename, 'r') as file:
                    lines = file.readlines()
                    for number in line_numbers:
                        if '-' in number:
                            start, end = map(int, number.split('-'))
                            for i in range(start, end + 1):
                                qc = generate_circuit_from_line(lines[i - 1], num_qubits)
                                circuit_drawer(qc, output='mpl', filename=f"circuit_{i - 1}.png")
                                plt.close()  # Close the figure after saving
                                print(f"Saved circuit_{i - 1}.png")
                        else:
                            i = int(number)
                            qc = generate_circuit_from_line(lines[i - 1], num_qubits)
                            circuit_drawer(qc, output='mpl', filename=f"circuit_{i - 1}.png")
                            plt.close()  # Close the figure after saving
                            print(f"Saved circuit_{i - 1}.png")

            elif mode == 3:
                break
    
    if(entrance == 10):
    
        while True:
            mode = request_user_input("Enter 1 to generate new circuits, 2 to generate .png from existing file, 3 to exit: ", int)

            if mode == 1:
                gates = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR']
                num_elements = request_user_input("Enter the number of elements (gates) per circuit: ")

                with open('source_classical.txt', 'w') as file:
                    gate_combinations = product(gates, repeat=num_elements)

                    for idx, combo in enumerate(gate_combinations):
                        circuit_line = ', '.join(combo)
                        file.write(f"Circuit {idx}: {circuit_line}\n")
                        print(f"Saved configuration for Circuit {idx}")

            elif mode == 2:
                filename = request_user_input("Enter the name of the source file (including .txt extension): ", str)

                print("Enter the line numbers or ranges (e.g., 1-3, 5, 7-10) to generate .png files:")
                line_numbers = input("Line numbers/ranges: ").split(',')

                with open(filename, 'r') as file:
                    lines = file.readlines()
                    for number in line_numbers:
                        if '-' in number:
                            start, end = map(int, number.split('-'))
                            for i in range(start, end + 1):
                                try:
                                    line_to_process = lines[i - 1].split(':')[-1].strip()
                                    circuit_diagram = generate_classical_circuit_from_line(line_to_process, f"circuit_{i - 1}.png")
                                    print(f"Saved circuit_{i - 1}.png")
                                except Exception as e:
                                    print(f"An error occurred while processing line {i}: {e}")
                        else:
                            i = int(number)
                            try:
                                line_to_process = lines[i - 1].split(':')[-1].strip()
                                circuit_diagram = generate_classical_circuit_from_line(line_to_process, f"circuit_{i - 1}.png")
                                print(f"Saved circuit_{i - 1}.png")
                            except Exception as e:
                                print(f"An error occurred while processing line {i}: {e}")


            elif mode == 3:
                break
    
    if(entrance == 11):
    
        # Define the path for the CSV file
        file_path = 'cell_data.csv'

        # Define the headers for the CSV file
        headers = ['x', 'y', 'z', 'function_id', 'function_word', 'function_definition']

        # Check if the file exists; if not, create it and write the headers
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

        # Start the program loop
        while True:
            # Prompt the user to enter the cell data or type 'end_program' to exit
            print("Enter the cell's data (or type 'end_program' to exit):")
            user_input = input("Format: x,y,z,function_id,function_word,function_definition\\n")
            
            # Check if the user wants to end the program
            if user_input.lower() == 'end_program':
                break
            
            # Split the input into components
            data = user_input.split(',')
            
            # Check if the input is valid
            if len(data) != 6:
                print("Invalid input format. Please try again.")
                continue
            
            # Append the data to the CSV file
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
            
            print("Data added to the file.")
    if(entrance == 12):
        main0()
    if(entrance == 13):
        countables()
    if(entrance == 14):
        # Specify the file path for the 26-bit combinations
        name_ext = input("Enter filename with .txt extension: ")
        file_path_26_bit = "llanguageMod/binary-configs/" + name_ext
        n_ = int(input("Enter bit length per binary string: "))

        # Generate and save the 26-bit combinations
        generate_and_save_n_bit_combinations(file_path_26_bit, n_)
    if(entrance == 15):
        help_print()
    if(entrance == 16):
    
        base = int(input("Enter the integer base of origin file (between 2 and 16): "))

        input_file = input("Enter origin file path: ")
        output_file = input("Enter output file path: ")

        try:
            convert_file(input_file, output_file, base)
            print(f"Successfully converted {input_file} to {output_file}")
        except FileNotFoundError:
            print(f"Error: File not found. Please check the paths for {input_file} and {output_file}")
    
    if(entrance == 17):
        while(5 > 2):
            inty = int(input("0 for main_menu, 1 to continue: "))
            if(inty == 0):
                break
            if(inty == 1):
                main2()
    if(entrance == 18):
        while(1 < 2):
            intt = int(input("0 for main_menu, 1 to continue: "))
            if(intt == 0):
                break
            if(intt == 1):
                main18()
    if(entrance == 19):
        print("""\n\nThe following is an example mapping for the font index:\n
        0 a
        1 b
        2 c
        3 d
        4 e
        5 f
        6 g
        7 h
        8 i
        9 j
        10 k
        11 l
        12 m
        13 n
        14 o
        15 p
        16 q
        17 r
        18 s
        19 t
        20 u
        21 v
        22 w
        23 x
        24 y
        25 z
        26 '
        27 ,
        28 /
        29 <
        30 >
        31 ?
        32 ;
        33 :
        34 @
        35 #
        36 ~
        37 ]
        38 [
        39 {
        40 }
        41 '
        42 ¬
        43 |
        44 ¦
        45 !
        46 "
        47 £
        48 $
        49 %
        50 ^
        51 &
        52 *
        53 (
        54 )
        55 -
        56 _
        57 +
        58 =
        59 .
        60 A
        61 B
        62 C
        63 D
        64 E
        65 F
        66 G
        67 H
        68 I
        69 J
        70 K
        71 L
        72 M
        73 N
        74 O
        75 P
        76 Q
        77 R
        78 S
        79 T
        80 U
        81 V
        82 W
        83 X
        84 Y
        85 Z
        86 0
        87 1
        88 2
        89 3
        90 4
        91 5
        92 6
        93 7
        94 8
        95 9
        96 \\
        """)
        grid_size = int(input("Enter the grid size (number of squares along one side): "))
        square_size = int(input("Enter the pixel length of each sub-square: "))
        font_size = int(input("Enter the font size for the symbols: "))
        file_name = input("Enter the name of the configuration file to save (.txt): ")

        configurations = []
        for i in range(grid_size * grid_size):
            print(f"Configuration for square {i+1}")
            symbol_index = int(input("Enter symbol index (0 to 96): "))
            square_color_index = 0 + int(16777216 / (symbol_index + 1))
            font_color_index = 16777216 - int(16777216 / (symbol_index + 1))
            configurations.append((square_color_index, symbol_index, font_color_index))
        
        save_configuration_to_file19(file_name, grid_size, square_size, font_size, configurations)
        print(f"Configuration saved to {file_name}")
    if(entrance == 21):
        while(5 > 2):
            intys = int(input("0 for main_menu, 1 to continue: "))
            if(intys == 0):
                break
            if(intys == 1):                
                # Main
                initial_a = int(input("Enter initial a (a > b): "))
                initial_b = int(input("Enter initial b (b < a): "))
                user_iterations = int(input("Enter number of additional user iterations: "))

                fsm = ProximalPrimeFSM(initial_a, initial_b, user_iterations)
                fsm.run()
                coords = prepare_coordinates21(fsm.primes)

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ani = FuncAnimation(fig, animate21, frames=len(coords), repeat=False)
                plt.show()
    if(entrance == 22):
        while(5 > 2):
            intys22 = int(input("0 for main_menu, 1 to continue: "))
            if(intys22 == 0):
                break
            if(intys22 == 1):
                main22()
    if(entrance == 23):
        while(5 > 2):
            intys23 = int(input("0 for main_menu, 1 to continue: "))
            if(intys23 == 0):
                break
            if(intys23 == 1):
                main23()
    if(entrance == 24):
        while(5 > 2):
            intys23 = int(input("0 for main_menu, 1 to continue: "))
            if(intys23 == 0):
                break
            if(intys23 == 1):
                interactive_cli()
    if(entrance == 25):
        while(5 > 2):
            intys25 = int(input("0 for main menu, 1 to continue: "))
            if(intys25 == 0):
                break
            if(intys25 == 1):
                #import tkinter as tk
                #from tkinter import simpledialog, messagebox

                class BlockDiagramApp:
                    def __init__(self, root):
                        self.root = root
                        self.root.title("Block Diagram Creator")
                        self.canvas = tk.Canvas(self.root, bg="white")
                        self.canvas.pack(fill=tk.BOTH, expand=True)

                        self.grid_size = self.get_grid_size()
                        self.draw_grid()

                        self.canvas.bind("<Button-1>", self.add_circle)
                        self.canvas.bind("<Button-3>", self.add_rectangle)
                        self.canvas.bind("<Button-2>", self.start_line)
                        self.root.bind("<Shift_L>", self.toggle_turn)

                        self.elements = []
                        self.line_start = None
                        self.current_line = None
                        self.turn_points = []
                        self.label_for_line = None
                        self.placing_line_label = False

                    def get_grid_size(self):
                        size = simpledialog.askinteger("Grid Size", "Enter the grid size (pixels):", minvalue=10, maxvalue=100)
                        if size is None:
                            size = 20  # Default grid size
                        return size

                    def snap_to_grid(self, x, y):
                        grid_size = self.grid_size
                        snapped_x = round(x / grid_size) * grid_size
                        snapped_y = round(y / grid_size) * grid_size
                        return snapped_x, snapped_y

                    def draw_grid(self):
                        self.canvas.delete("grid_line")  # Clear existing grid lines if any
                        width = self.canvas.winfo_width()
                        height = self.canvas.winfo_height()
                        grid_size = self.grid_size

                        for i in range(0, width, grid_size):
                            self.canvas.create_line([(i, 0), (i, height)], tag='grid_line', fill='lightgray')

                        for i in range(0, height, grid_size):
                            self.canvas.create_line([(0, i), (width, i)], tag='grid_line', fill='lightgray')

                        self.canvas.tag_lower("grid_line")  # Move grid lines to the background

                    def add_circle(self, event):
                        if self.placing_line_label:
                            self.place_label(event)
                            return

                        x, y = self.snap_to_grid(event.x, event.y)
                        label = self.get_label()
                        if label is not None:
                            circle = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
                            text = self.canvas.create_text(x, y, text=label)
                            self.elements.append(("circle", x, y, label, circle, text))

                    def add_rectangle(self, event):
                        if self.placing_line_label:
                            self.place_label(event)
                            return

                        x, y = self.snap_to_grid(event.x, event.y)
                        label = self.get_label()
                        if label is not None:
                            rect = self.canvas.create_rectangle(x-30, y-20, x+30, y+20, fill="lightgreen")
                            text = self.canvas.create_text(x, y, text=label)
                            self.elements.append(("rectangle", x, y, label, rect, text))

                    def start_line(self, event):
                        if self.placing_line_label:
                            self.place_label(event)
                            return

                        x, y = self.snap_to_grid(event.x, event.y)
                        if self.line_start is None:
                            self.line_start = (x, y)
                            self.current_line = []
                            self.turn_points = [(x, y)]
                        else:
                            self.add_line_segment(x, y)
                            self.turn_points.append((x, y))

                    def add_line_segment(self, x, y):
                        last_x, last_y = self.turn_points[-1]
                        if self.current_line is not None:
                            line = self.canvas.create_line(last_x, last_y, x, y, fill="black", width=2)
                            label = self.get_label()
                            if label is not None:
                                self.label_for_line = label
                                self.placing_line_label = True
                                self.canvas.bind("<Button-1>", self.place_label)
                            self.elements.append(("line", last_x, last_y, x, y, line))

                        #if len(self.turn_points) >= 2:
                        self.line_start = None
                        self.current_line = None

                    def place_label(self, event):
                        if self.label_for_line is not None:
                            x, y = event.x, event.y
                            text = self.canvas.create_text(x, y, text=self.label_for_line, fill="red")
                            self.elements.append(("line_label", x, y, self.label_for_line, text))
                            self.label_for_line = None
                            self.placing_line_label = False
                            self.canvas.unbind("<Button-1>")
                            self.canvas.bind("<Button-1>", self.add_circle)
                            self.canvas.bind("<Button-3>", self.add_rectangle)

                    def toggle_turn(self, event):
                        if self.line_start is not None and self.turn_points:
                            self.turn_points.append(self.turn_points[-1])

                    def get_label(self):
                        return simpledialog.askstring("Input", "Enter the label for the component or line:")

                    def resize_canvas(self, event):
                        self.draw_grid()

                #if __name__ == "__main__":
                root = tk.Tk()
                app = BlockDiagramApp(root)
                root.geometry("800x600")
                root.bind('<Configure>', app.resize_canvas)
                root.mainloop()
    if(entrance == 26):
        while(5 > 2):
            intys26 = int(input("0 for main menu, 1 to continue: "))
            if(intys26 == 0):
                break
            if(intys26 == 1):
                class Point:
                    def __init__(self, x, y, z):
                        self.x = x
                        self.y = y
                        self.z = z

                    def __repr__(self):
                        return f"Point(x={self.x}, y={self.y}, z={self.z})"

                class PointStructure:
                    def __init__(self, index, origin):
                        self.index = index
                        self.origin = origin
                        self.points = {}

                    def add_point(self, point_index, x, y, z):
                        self.points[point_index] = Point(x, y, z)

                    def apply_transformation(self, transformation):
                        for point in self.points.values():
                            transformation(point)

                    def __repr__(self):
                        return f"PointStructure(index={self.index}, origin={self.origin}, points={self.points})"

                class Transformation:
                    @staticmethod
                    def translate(dx, dy, dz):
                        def transformation(point):
                            point.x += dx
                            point.y += dy
                            point.z += dz
                        return transformation

                    @staticmethod
                    def scale(sx, sy, sz):
                        def transformation(point):
                            point.x *= sx
                            point.y *= sy
                            point.z *= sz
                        return transformation

                    @staticmethod
                    def rotate_x(angle):
                        def transformation(point):
                            y = point.y * math.cos(angle) - point.z * math.sin(angle)
                            z = point.y * math.sin(angle) + point.z * math.cos(angle)
                            point.y = y
                            point.z = z
                        return transformation

                    @staticmethod
                    def rotate_y(angle):
                        def transformation(point):
                            x = point.x * math.cos(angle) + point.z * math.sin(angle)
                            z = -point.x * math.sin(angle) + point.z * math.cos(angle)
                            point.x = x
                            point.z = z
                        return transformation

                    @staticmethod
                    def rotate_z(angle):
                        def transformation(point):
                            x = point.x * math.cos(angle) - point.y * math.sin(angle)
                            y = point.x * math.sin(angle) + point.y * math.cos(angle)
                            point.x = x
                            point.y = y
                        return transformation

                def get_user_input():
                    structures = []
                    
                    while True:
                        print("\nCreate a new point structure")
                        index = int(input("Enter structure index: "))
                        x0 = float(input("Enter x-coordinate of the origin: "))
                        y0 = float(input("Enter y-coordinate of the origin: "))
                        z0 = float(input("Enter z-coordinate of the origin: "))
                        origin = Point(x0, y0, z0)
                        structure = PointStructure(index, origin)
                        
                        while True:
                            point_index = int(input("Enter point index (or -1 to stop adding points): "))
                            if point_index == -1:
                                break
                            x = float(input("Enter x-coordinate of the point: "))
                            y = float(input("Enter y-coordinate of the point: "))
                            z = float(input("Enter z-coordinate of the point: "))
                            structure.add_point(point_index, x, y, z)
                        
                        structures.append(structure)
                        
                        another = input("Would you like to add another point structure? (yes/no): ").strip().lower()
                        if another != 'yes':
                            break

                    return structures

                def apply_user_transformations(structures):
                    while True:
                        structure_index = int(input("Enter the index of the point structure to transform (or -1 to stop): "))
                        if structure_index == -1:
                            break
                        structure = next((s for s in structures if s.index == structure_index), None)
                        if not structure:
                            print(f"No point structure found with index {structure_index}")
                            continue

                        print("Choose a transformation: translate, scale, rotate_x, rotate_y, rotate_z")
                        transformation_type = input("Enter the transformation type: ").strip().lower()

                        if transformation_type == 'translate':
                            dx = float(input("Enter translation along x: "))
                            dy = float(input("Enter translation along y: "))
                            dz = float(input("Enter translation along z: "))
                            transformation = Transformation.translate(dx, dy, dz)
                        
                        elif transformation_type == 'scale':
                            sx = float(input("Enter scaling factor along x: "))
                            sy = float(input("Enter scaling factor along y: "))
                            sz = float(input("Enter scaling factor along z: "))
                            transformation = Transformation.scale(sx, sy, sz)
                        
                        elif transformation_type == 'rotate_x':
                            angle = float(input("Enter rotation angle around x-axis (in radians): "))
                            transformation = Transformation.rotate_x(angle)
                        
                        elif transformation_type == 'rotate_y':
                            angle = float(input("Enter rotation angle around y-axis (in radians): "))
                            transformation = Transformation.rotate_y(angle)
                        
                        elif transformation_type == 'rotate_z':
                            angle = float(input("Enter rotation angle around z-axis (in radians): "))
                            transformation = Transformation.rotate_z(angle)
                        
                        else:
                            print("Invalid transformation type")
                            continue
                        
                        structure.apply_transformation(transformation)
                        print("\nUpdated Point Structure:")
                        print(structure)

                def main():
                    print("Welcome to the Point Structure Transformation Program")

                    structures = get_user_input()
                    
                    print("\nInitial Point Structures:")
                    for structure in structures:
                        print(structure)
                    
                    apply_user_transformations(structures)

                    print("\nFinal Point Structures:")
                    for structure in structures:
                        print(structure)

                #if __name__ == "__main__":
                main()
    if(entrance == 27):
        while(5 > 2):
            intys27 = int(input("0 for main menu, 1 to continue: "))
            if(intys27 == 0):
                break
            if(intys27 == 1):
                #import os

                def define_encodings():
                    encodings = {}
                    if os.path.exists('langc.txt'):
                        encodings = load_encodings()
                    
                    print("Enter the visual encoding for each character. Type 'done' when finished.")
                    while True:
                        char = input("Enter character (or type 'done' to finish): ").strip()
                        if char.lower() == 'done':
                            break
                        if len(char) != 1:
                            print("Please enter a single character.")
                            continue
                        encoding = input(f"Enter encoding for '{char}': ").strip()
                        encodings[char] = encoding
                    
                    # Save encodings to langc.txt
                    with open('langc.txt', 'w', encoding='utf-8') as f:
                        for char, encoding in encodings.items():
                            f.write(f"{char}:{encoding}\n")
                    
                    print("Encodings saved to langc.txt")

                def load_encodings(file_path='langc.txt'):
                    encodings = {}
                    if not os.path.exists(file_path):
                        return encodings
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            char, encoding = line.strip().split(':')
                            encodings[char] = encoding
                    return encodings

                def process_input_string(input_file='input_s.txt', output_file='encode_out.txt'):
                    if not os.path.exists(input_file):
                        print(f"Input file '{input_file}' not found.")
                        return
                    
                    encodings = load_encodings()
                    if not encodings:
                        print("No encodings found. Please define encodings first.")
                        return
                    
                    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
                        for line in infile:
                            encoded_line = []
                            for char in line:
                                if char in encodings:
                                    encoded_line.append(encodings[char])
                                else:
                                    encoded_line.append('0')  # Unrecognized character
                            outfile.write(' '.join(encoded_line) + '\n')

                    print(f"Encoded output saved to {output_file}")

                def view_encodings():
                    encodings = load_encodings()
                    if not encodings:
                        print("No encodings found.")
                        return
                    
                    print("Current encodings:")
                    for char, encoding in encodings.items():
                        print(f"'{char}': {encoding}")

                def clear_encodings():
                    if os.path.exists('langc.txt'):
                        os.remove('langc.txt')
                    print("Encodings cleared.")

                def main_menus():
                    while True:
                        print("\nMenu:")
                        print("1. Define Encodings")
                        print("2. Process Input String (input_s.txt)")
                        print("3. View Encodings")
                        print("4. Clear All Encodings")
                        print("5. Print Help Documentation")
                        print("6. Exit")
                        
                        choice = input("Enter your choice: ").strip()
                        if choice == '1':
                            define_encodings()
                        elif choice == '2':
                            input_file = input("Enter the input file name (default: input_s.txt): ").strip() or 'input_s.txt'
                            output_file = input("Enter the output file name (default: encode_out.txt): ").strip() or 'encode_out.txt'
                            process_input_string(input_file, output_file)
                        elif choice == '3':
                            view_encodings()
                        elif choice == '4':
                            clear_encodings()
                        elif choice == '6':
                            print("Exiting...")
                            break
                        elif choice == '5':
                            print("""Help Documentation ...
                            
                            Example Visual Numerical Mapping For Reading Any Language
                            via Pattern Recognition.

                            1	/
                            2	\\
                            3	|
                            4	-
                            5	.
                            6	)
                            7	(
                            8	Reading Order (Top to Bottom, Left to Right)
                            
                            """)
                        else:
                            print("Invalid choice. Please try again.")

                #if __name__ == "__main__":
                main_menus()
                
    if(entrance == 28):
            while(5 > 2):
                intys28 = int(input("0 for main menu, 1 to continue: "))
                if(intys28 == 0):
                    break
                if(intys28 == 1):
                    # Predefined color palette with 12 unique colors
                    COLOR_PALETTE = [
                        '#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD', 
                        '#1ABC9C', '#E74C3C', '#2ECC71', '#3498DB', '#9B59B6',
                        '#FF33A1', '#A1FF33'
                    ]

                    class App:
                        def __init__(self, master):
                            self.master = master
                            master.title("Hex Color Picker")

                            self.label = Label(master, text="Choose Text File")
                            self.label.pack()

                            self.open_file_button = Button(master, text="Open File", command=self.open_file)
                            self.open_file_button.pack()

                            self.close_button = Button(master, text="Generate Image", command=self.generate_image)
                            self.close_button.pack()
                            
                            self.save_pdf_button = Button(master, text="Save as PDF", command=self.save_as_pdf)
                            self.save_pdf_button.pack()

                            self.data = []
                            self.color_encoding = {}

                        def open_file(self):
                            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
                            if file_path:
                                try:
                                    with open(file_path, 'r') as file:
                                        self.data = [float(num) for num in file.read().split()]
                                        self.label.config(text="File successfully opened.")
                                except Exception as e:
                                    self.label.config(text=f"Error opening file: {e}")
                            else:
                                self.label.config(text="No file selected.")

                        def generate_image(self):
                            print("Generating ...")
                            if hasattr(self, 'data') and self.data:
                                self.label.config(text="Generating, please wait...")
                                self.master.update_idletasks()  # Force update of the GUI
                                
                                # Convert data to colors
                                color_data = [self.data_to_color(datum) for datum in self.data]

                                self.label.config(text="Data converted to colors. Creating image...")
                                self.master.update_idletasks()  # Force update of the GUI

                                create_image(color_data, self.data)
                                
                                self.label.config(text="Image successfully generated.")
                            else:
                                self.label.config(text="Please select a file first.")
                        
                        def data_to_color(self, datum):
                            # Perform the modular arithmetic-based color encoding
                            first_digit = int(str(datum)[0]) - 1
                            fractional_part = int(str(datum).split('.')[1])
                            cpoint = fractional_part % 12
                            pointer = (first_digit + cpoint) % 12
                            return COLOR_PALETTE[pointer]
                        
                        def save_as_pdf(self):
                            if hasattr(self, 'generated_image'):
                                file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF files", "*.pdf")])
                                if file_path:
                                    # A5 dimensions in pixels (previously calculated)
                                    a5_width_pixels = 1748
                                    a5_height_pixels = 2480

                                    # Call the function to save the image as a PDF
                                    save_image_as_pdf(self.generated_image, file_path, a5_width_pixels, a5_height_pixels)
                                    self.label.config(text="Saved as PDF.")
                                else:
                                    self.label.config(text="No file selected.")
                            else:
                                self.label.config(text="Generate an image first.")

                    def create_image(color_data, data):
                        # Count unique string encodings
                        unique_encodings = set(data)
                        num_unique_encodings = len(unique_encodings)
                        total_encodings = len(data)  # This will count all the encodings
                        print(f"Number of unique encodings: {num_unique_encodings}")
                        print(f"Total number of encodings: {total_encodings}")

                        # Request image dimensions and pixel size from user
                        pixel_side_length = int(input("Enter the square side length of each pixel to be created: "))
                        num_pixels_width = int(input("Enter the pixel width of the image, by number of pixels: "))
                        num_pixels_height = int(input("Enter the pixel height of the image, by number of pixels: "))
                        
                        img_width = pixel_side_length * num_pixels_width
                        img_height = pixel_side_length * num_pixels_height
                        
                        # Create an empty white canvas
                        image = Image.new('RGB', (img_width, img_height), color="white")
                        
                        # Create a drawing context for the image
                        draw = ImageDraw.Draw(image)
                        
                        # Save the image in the object for later PDF conversion
                        app.generated_image = image
                        
                        data_idx = 0  # Index to track data position
                        for i in range(num_pixels_height):
                            for j in range(num_pixels_width):
                                if data_idx < len(color_data):
                                    hex_value = color_data[data_idx]
                                    top_left = (j * pixel_side_length, i * pixel_side_length)
                                    bottom_right = ((j + 1) * pixel_side_length, (i + 1) * pixel_side_length)
                                    draw.rectangle([top_left, bottom_right], fill=hex_value)
                                    data_idx += 1

                        image.show()
                        image.save('generated_image.png')

                        return image

                    def save_image_as_pdf(image, file_path, a5_width_pixels, a5_height_pixels, margin_mm=10):
                        margin_pixels = int(margin_mm * (300 / 25.4))
                        drawable_width = a5_width_pixels - (2 * margin_pixels)
                        drawable_height = a5_height_pixels - (2 * margin_pixels)
                        num_pages_horizontal = math.ceil(image.width / drawable_width)
                        num_pages_vertical = math.ceil(image.height / drawable_height)

                        pdf_pages = []

                        for y in range(num_pages_vertical):
                            for x in range(num_pages_horizontal):
                                left = x * drawable_width
                                upper = y * drawable_height
                                right = min(left + drawable_width, image.width)
                                lower = min(upper + drawable_height, image.height)
                                crop_area = (left, upper, right, lower)

                                cropped_image = image.crop(crop_area)
                                pdf_page = Image.new('RGB', (a5_width_pixels, a5_height_pixels), 'white')

                                paste_position = (
                                    margin_pixels + max(0, (drawable_width - cropped_image.width) // 2),
                                    margin_pixels + max(0, (drawable_height - cropped_image.height) // 2)
                                )

                                pdf_page.paste(cropped_image, paste_position)
                                pdf_pages.append(pdf_page)

                        pdf_pages[0].save(file_path, save_all=True, append_images=pdf_pages[1:], resolution=100.0)

                    root = Tk()
                    app = App(root)
                    root.mainloop()
    if(entrance == 29):
            while(5 > 2):
                intys29 = int(input("0 for main menu, 1 to continue: "))
                if(intys29 == 0):
                    break
                if(intys29 == 1):

                    class MplCanvas(FigureCanvas):
                        def __init__(self, parent=None, width=5, height=4, dpi=100, projection='3d'):
                            fig = Figure(figsize=(width, height), dpi=dpi)
                            self.axes = fig.add_subplot(111, projection=projection)
                            super(MplCanvas, self).__init__(fig)

                    class ShapeManagerGUI(QtWidgets.QMainWindow):
                        def __init__(self):
                            super(ShapeManagerGUI, self).__init__()
                            self.setWindowTitle("Shape Manager")
                            self.setGeometry(100, 100, 1200, 600)
                            self.canvas = MplCanvas(self)
                            self.setCentralWidget(self.canvas)
                            self.shapes = {}
                            self.init_ui()

                        def init_ui(self):
                            self.control_panel = QtWidgets.QWidget(self)
                            self.control_layout = QtWidgets.QVBoxLayout()

                            self.control_layout.addWidget(QtWidgets.QLabel("Label:"))
                            self.label_input = QtWidgets.QLineEdit(self)
                            self.control_layout.addWidget(self.label_input)

                            self.control_layout.addWidget(QtWidgets.QLabel("Dimension (1D, 2D, 3D):"))
                            self.dimension_input = QtWidgets.QComboBox(self)
                            self.dimension_input.addItems(["1D", "2D", "3D"])
                            self.control_layout.addWidget(self.dimension_input)

                            self.control_layout.addWidget(QtWidgets.QLabel("Function:"))
                            self.function_input = QtWidgets.QLineEdit(self)
                            self.control_layout.addWidget(self.function_input)

                            self.add_shape_btn = QtWidgets.QPushButton("Add Shape", self)
                            self.add_shape_btn.clicked.connect(self.add_shape)
                            self.control_layout.addWidget(self.add_shape_btn)

                            self.draw_shape_btn = QtWidgets.QPushButton("Draw Shape", self)
                            self.draw_shape_btn.clicked.connect(self.draw_shape)
                            self.control_layout.addWidget(self.draw_shape_btn)

                            self.save_png_btn = QtWidgets.QPushButton("Save as PNG", self)
                            self.save_png_btn.clicked.connect(self.save_as_png)
                            self.control_layout.addWidget(self.save_png_btn)

                            self.layer_shape_btn = QtWidgets.QPushButton("Layer Shapes", self)
                            self.layer_shape_btn.clicked.connect(self.layer_shapes)
                            self.control_layout.addWidget(self.layer_shape_btn)

                            self.save_session_btn = QtWidgets.QPushButton("Save Session", self)
                            self.save_session_btn.clicked.connect(self.save_session)
                            self.control_layout.addWidget(self.save_session_btn)

                            self.load_session_btn = QtWidgets.QPushButton("Load Session", self)
                            self.load_session_btn.clicked.connect(self.load_session)
                            self.control_layout.addWidget(self.load_session_btn)

                            self.doc_panel = QtWidgets.QTextEdit(self)
                            self.doc_panel.setReadOnly(True)
                            self.control_layout.addWidget(self.doc_panel)

                            self.control_panel.setLayout(self.control_layout)
                            self.dock_widget = QtWidgets.QDockWidget("Control Panel", self)
                            self.dock_widget.setWidget(self.control_panel)
                            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_widget)

                            self.update_documentation()

                        def update_documentation(self):
                            doc_text = "Current State Shapes:\n\n"
                            for label, shape in self.shapes.items():
                                doc_text += f"Label: {label}\nDimension: {shape['dimension']}\nFunction: {shape['function']}\n\n"
                            self.doc_panel.setText(doc_text)

                        def add_shape(self):
                            label = self.label_input.text().strip()
                            dimension = self.dimension_input.currentText()
                            function = self.function_input.text().strip()
                            if label and function:
                                self.shapes[label] = {'dimension': dimension, 'function': function}
                                QtWidgets.QMessageBox.information(self, "Shape Added", f"Shape '{label}' added successfully.")
                                self.update_documentation()
                            else:
                                QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please ensure all fields are filled correctly.")

                        def draw_shape(self):
                            label = self.label_input.text().strip()
                            if label in self.shapes:
                                shape = self.shapes[label]
                                dimension = shape['dimension']
                                function = shape['function']
                                try:
                                    self.canvas.axes.clear()
                                    if dimension == '1D':
                                        self.draw_1d(function)
                                    elif dimension == '2D':
                                        self.draw_2d(function)
                                    elif dimension == '3D':
                                        self.draw_3d(function)
                                    self.canvas.draw()
                                except Exception as e:
                                    QtWidgets.QMessageBox.critical(self, "Error", "Failed to draw shape: " + str(e))
                            else:
                                QtWidgets.QMessageBox.warning(self, "Shape Not Found", "No shape found with label: " + label)

                        def draw_1d(self, function):
                            x = np.linspace(-10, 10, 400)
                            y = eval(function, {'x': x, 'np': np})
                            self.canvas.axes.plot(x, y)
                            self.canvas.axes.set_title("1D Plot")

                        def draw_2d(self, function):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            self.canvas.axes.contourf(X, Y, Z, cmap='viridis')
                            self.canvas.axes.set_title("2D Contour Plot")

                        def draw_3d(self, function):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            self.canvas.axes.plot_surface(X, Y, Z, cmap='viridis')
                            self.canvas.axes.set_title("3D Surface Plot")

                        def layer_shapes(self):
                            # First, explore the current state shapes
                            self.explore_state_shapes(list(self.shapes.keys()))

                            # After exploring, prompt the user to enter the layering sequence
                            labels, okPressed = QtWidgets.QInputDialog.getText(self, "Layer Shapes", "Enter labels to layer (separated by space):")
                            if okPressed and labels:
                                new_label, okPressed = QtWidgets.QInputDialog.getText(self, "New Label", "Enter new label for the layered shape:")
                                if okPressed and new_label:
                                    try:
                                        # Check that all shapes to be layered are of the same dimension
                                        dimensions = [self.shapes[label.strip()]['dimension'] for label in labels.split() if label.strip() in self.shapes]
                                        if len(set(dimensions)) > 1:
                                            QtWidgets.QMessageBox.critical(self, "Error", "All shapes must have the same dimension to be layered.")
                                            return

                                        dimension = dimensions[0]
                                        layered_function = ' + '.join(['('+self.shapes[label.strip()]['function']+')' for label in labels.split() if label.strip() in self.shapes])
                                        self.shapes[new_label] = {'dimension': dimension, 'function': layered_function}
                                        QtWidgets.QMessageBox.information(self, "Layered Shape Created", f"Layered shape '{new_label}' created.")
                                        self.update_documentation()
                                    except Exception as e:
                                        QtWidgets.QMessageBox.critical(self, "Error", str(e))

                                # Draw the layered shapes on a single plot
                                self.draw_layered_shapes(labels.split())

                        def draw_layered_shapes(self, labels):
                            if labels:
                                dimensions = [self.shapes[label.strip()]['dimension'] for label in labels if label.strip() in self.shapes]
                                if len(set(dimensions)) > 1:
                                    QtWidgets.QMessageBox.critical(self, "Error", "All shapes must have the same dimension to be layered.")
                                    return

                                dimension = dimensions[0]
                                self.canvas.axes.clear()
                                for label in labels:
                                    if label.strip() in self.shapes:
                                        shape = self.shapes[label.strip()]
                                        function = shape['function']
                                        try:
                                            if dimension == '1D':
                                                self.draw_1d_layered(function)
                                            elif dimension == '2D':
                                                self.draw_2d_layered(function)
                                            elif dimension == '3D':
                                                self.draw_3d_layered(function)
                                        except Exception as e:
                                            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to draw shape '{label.strip()}': " + str(e))
                                self.canvas.draw()

                        def draw_1d_layered(self, function):
                            x = np.linspace(-10, 10, 400)
                            y = eval(function, {'x': x, 'np': np})
                            self.canvas.axes.plot(x, y)

                        def draw_2d_layered(self, function):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            self.canvas.axes.contour(X, Y, Z, cmap='viridis')

                        def draw_3d_layered(self, function):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            self.canvas.axes.plot_surface(X, Y, Z, cmap='viridis')

                        def explore_state_shapes(self, labels):
                            explorer_window = QtWidgets.QWidget()
                            explorer_window.setWindowTitle("State Shape Explorer")
                            explorer_layout = QtWidgets.QVBoxLayout()

                            for label in labels:
                                if label.strip() in self.shapes:
                                    shape = self.shapes[label.strip()]
                                    dimension = shape['dimension']
                                    function = shape['function']
                                    canvas = MplCanvas(explorer_window, width=5, height=4, dpi=100, projection='3d' if dimension == '3D' else None)
                                    try:
                                        if dimension == '1D':
                                            self.draw_1d_explorer(function, canvas)
                                        elif dimension == '2D':
                                            self.draw_2d_explorer(function, canvas)
                                        elif dimension == '3D':
                                            self.draw_3d_explorer(function, canvas)
                                        explorer_layout.addWidget(canvas)
                                    except Exception as e:
                                        QtWidgets.QMessageBox.critical(self, "Error", f"Failed to draw shape '{label.strip()}': " + str(e))

                            explorer_window.setLayout(explorer_layout)
                            explorer_window.show()

                        def draw_1d_explorer(self, function, canvas):
                            x = np.linspace(-10, 10, 400)
                            y = eval(function, {'x': x, 'np': np})
                            canvas.axes.plot(x, y)
                            canvas.axes.set_title("1D Plot")

                        def draw_2d_explorer(self, function, canvas):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            canvas.axes.contourf(X, Y, Z, cmap='viridis')
                            canvas.axes.set_title("2D Contour Plot")

                        def draw_3d_explorer(self, function, canvas):
                            x = np.linspace(-5, 5, 100)
                            y = np.linspace(-5, 5, 100)
                            X, Y = np.meshgrid(x, y)
                            Z = eval(function, {'X': X, 'Y': Y, 'np': np})
                            canvas.axes.plot_surface(X, Y, Z, cmap='viridis')
                            canvas.axes.set_title("3D Surface Plot")

                        def save_as_png(self):
                            label = self.label_input.text().strip()
                            if label in self.shapes and self.canvas.figure:
                                options = QtWidgets.QFileDialog.Options()
                                fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Shape as PNG", "", "PNG Files (*.png);;All Files (*)", options=options)
                                if fileName:
                                    self.canvas.figure.savefig(fileName)
                                    QtWidgets.QMessageBox.information(self, "Export Successful", f"Shape saved as PNG: {fileName}")
                            else:
                                QtWidgets.QMessageBox.warning(self, "Shape Not Found", "No shape found with label: " + label)

                        def save_session(self):
                            options = QtWidgets.QFileDialog.Options()
                            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Session", "", "Session Files (*.pkl);;All Files (*)", options=options)
                            if fileName:
                                with open(fileName, 'wb') as f:
                                    pickle.dump(self.shapes, f)
                                QtWidgets.QMessageBox.information(self, "Session Saved", "Session saved successfully.")

                        def load_session(self):
                            options = QtWidgets.QFileDialog.Options()
                            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Session", "", "Session Files (*.pkl);;All Files (*)", options=options)
                            if fileName:
                                try:
                                    with open(fileName, 'rb') as f:
                                        self.shapes = pickle.load(f)
                                    QtWidgets.QMessageBox.information(self, "Session Loaded", "Session loaded successfully.")
                                    self.update_documentation()
                                except FileNotFoundError:
                                    QtWidgets.QMessageBox.warning(self, "Session Not Found", "No session found.")

                    def main():
                        app = QtWidgets.QApplication(sys.argv)
                        main_window = ShapeManagerGUI()
                        main_window.show()
                        sys.exit(app.exec_())

                    #if __name__ == "__main__":
                    main()

        

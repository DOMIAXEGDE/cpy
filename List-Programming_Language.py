import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Menu, filedialog
import json
import subprocess

class MemorySlotManager:
    def __init__(self, memory_dir="memory_slots", no_duplicates=False):
        self.memory_dir = memory_dir
        self.no_duplicates = no_duplicates
        os.makedirs(self.memory_dir, exist_ok=True)
        self.memory_slots = []
        self.load_memory_slots()

    def load_memory_slots(self):
        self.memory_slots = []
        for file_name in os.listdir(self.memory_dir):
            file_path = os.path.join(self.memory_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    slot, value = line.split(maxsplit=1)
                    self.memory_slots.append((file_name, slot, value.strip()))

    def write_memory_slot(self, file_number, slot_number, value):
        file_path = os.path.join(self.memory_dir, f"{file_number}.txt")
        with open(file_path, 'a') as file:
            file.write(f"{slot_number}\t\t\t\t{value}\n")
        # Update memory_slots
        file_name = f"{file_number}.txt"
        slot_str = str(slot_number)
        # Check if the slot already exists
        for idx, (fname, s, val) in enumerate(self.memory_slots):
            if fname == file_name and s == slot_str:
                # Update the value
                self.memory_slots[idx] = (fname, s, value)
                break
        else:
            # Add new slot
            self.memory_slots.append((file_name, slot_str, value))

    def read_memory_slot(self, file_number, slot_number):
        file_name = f"{file_number}.txt"
        slot_str = str(slot_number)
        for fname, s, value in self.memory_slots:
            if fname == file_name and s == slot_str:
                return value
        raise ValueError(f"Slot {slot_number} not found in file {file_number}.txt.")

    def seek_read_memory_slot(self, file_name, slot_number):
        slot_str = str(slot_number)
        for fname, s, value in self.memory_slots:
            if fname == file_name and s == slot_str:
                return value
        return None

    def get_last_slot_number(self, file_number):
        file_name = f"{file_number}.txt"
        slot_numbers = [int(s) for fname, s, val in self.memory_slots if fname == file_name]
        if slot_numbers:
            return max(slot_numbers)
        else:
            raise ValueError(f"No slots found in file {file_number}.txt.")

    def check_duplicate_assignment(self, file_number, slot_number, value):
        file_name = f"{file_number}.txt"
        slot_str = str(slot_number)
        for fname, s, val in self.memory_slots:
            if fname == file_name and s == slot_str and val == value:
                return True
        return False

    def check_value_exists(self, value):
        for fname, s, val in self.memory_slots:
            if val == value:
                return int(fname.split('.')[0])
        return None

    def request_check_value_exists(self, value):
        for fname, s, val in self.memory_slots:
            if val == value:
                return fname.strip('.txt'), s
        return None

    def execute_sequence(self, sequence):
        tokens = sequence.split(maxsplit=3)
        if not tokens:
            return "Invalid sequence"
        command = tokens[0]
        if command == 'assign':
            current_file = int(tokens[1])
            slot_number = int(tokens[2])
            value_or_reference = tokens[3]
            if '.' in value_or_reference:
                ref_file, ref_slot = map(int, value_or_reference.split('.'))
                value = self.read_memory_slot(ref_file, ref_slot)
            else:
                value = value_or_reference
            if self.no_duplicates and self.check_value_exists(value):
                return f"Error: Value '{value}' already exists in the memory slots."
            elif self.check_duplicate_assignment(current_file, slot_number, value):
                return f"Duplicate assignment detected: {value} is already assigned to slot {slot_number} in file {current_file}."
            else:
                self.write_memory_slot(current_file, slot_number, value)
                return f"Assigned '{value}' to slot {slot_number} in file {current_file}."
        elif '.' in command:
            file_number, slot_number = map(int, command.split('.'))
            value = self.read_memory_slot(file_number, slot_number)
            return value
        elif command == 'last_slot':
            file_number = int(tokens[1])
            last_slot_number = self.get_last_slot_number(file_number)
            return f"The last slot number in file {file_number}.txt is {last_slot_number}"
        elif command == 'check_duplicate':
            file_number = int(tokens[1])
            slot_number = int(tokens[2])
            value = tokens[3]
            if self.check_duplicate_assignment(file_number, slot_number, value):
                return f"Duplicate: {value} is already assigned to slot {slot_number} in file {file_number}."
            else:
                return f"No duplicate found: {value} is not assigned to slot {slot_number} in file {file_number}."
        elif command == 'help_command':
            return self.get_help_text()
        elif command == 'value_exists' and int(tokens[1]) == 0 and int(tokens[2]) == 0:
            value_or_reference = tokens[3]
            result = self.request_check_value_exists(value_or_reference)
            if result:
                file_name, slot = result
                return f"Value '{value_or_reference}' exists in file {file_name}, slot {slot}."
            else:
                return "Value not found in file base."
        else:
            return "Invalid sequence"

    def get_help_text(self):
        help_text = """
        Memory Slot Language Help Documentation
        =======================================

        Command Structure:
        - assign <target_file_number> <slot_number> <reference_or_value>
            Assigns the value from the reference (another slot) or a direct value to the specified slot in the current file.
            If the target file number does not exist, it will be created.
            Examples: 
                assign 3 1 1.1    # Assigns the value from slot 1 in file 1 to slot 1 in file 3
                assign 3 1 hello  # Assigns the value 'hello' directly to slot 1 in file 3

        - <file_number>.<slot_number>
            Retrieves and prints the value from the specified slot in the specified file.
            Example: 3.1

        - last_slot <file_number>
            Displays the last memory slot number in the specified file.
            Example: last_slot 3

        - check_duplicate <file_number> <slot_number> <value>
            Checks if the specified value is already assigned to the given slot in the specified file.
            Example: check_duplicate 1 2 hello

        - value_exists 0 0 <reference_or_value>
            Checks if a specified reference or value exists within the file base with the
            provision of details.

        - help_command
            Prints this help documentation.

        Usage Examples:
        1. Write values to memory slots:
            write_memory_slot(1, 1, "hello")
            write_memory_slot(2, 1, "world")

        2. Assign and retrieve values dynamically:
            assign 3 1 1.1  # Assigns the value from slot 1 in file 1 to slot 1 in file 3
            3.1            # Retrieves and prints the value from slot 1 in file 3

        3. Assign direct values:
            assign 1 2 new_value  # Directly assigns 'new_value' to slot 2 in file 1

        4. Display last slot number:
            last_slot 1  # Displays the last slot number in file 1

        5. Check for duplicate assignments:
            check_duplicate 1 2 hello  # Checks if 'hello' is already assigned to slot 2 in file 1

        6. Check if value exists in any file:
            assign <current_file> <slot_number> <value>
            This will prevent assigning if value exists in any slot of any file.

        7. Check if value exists in any file:
            value_exists 0 0 <value>
            This will prevent assigning if value exists in any slot of any file.

        Notes:
        - Ensure the file paths are correct and the files exist.
        - Use integer values for file numbers and slot numbers.
        - The values assigned and retrieved can be any string.
        """
        return help_text

class Calculator(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Advanced Calculator")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        self.result_var = tk.StringVar()
        result_entry = tk.Entry(self, textvariable=self.result_var, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
        result_entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2)
        ]

        for (text, row, column) in buttons:
            button = tk.Button(self, text=text, padx=20, pady=20, font=("Arial", 18),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column, sticky="nsew")

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "=":
            try:
                result = str(eval(self.result_var.get()))
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Error")
        elif char == "C":
            self.result_var.set("")
        else:
            current_text = self.result_var.get()
            new_text = current_text + char
            self.result_var.set(new_text)

class Terminal(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Terminal Emulator")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.command_var = tk.StringVar()
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, width=80)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        command_entry = tk.Entry(self, textvariable=self.command_var, font=("Arial", 14), bd=2)
        command_entry.pack(fill=tk.X, padx=5, pady=5)
        command_entry.bind('<Return>', self.execute_command)

    def execute_command(self, event=None):
        command = self.command_var.get()
        if command.strip():
            try:
                result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"$ {command}\n{result}\n")
            except subprocess.CalledProcessError as e:
                self.output_text.insert(tk.END, f"$ {command}\n{e.output}\n")
            self.command_var.set("")

def save_session(manager):
    session_data = {
        'memory_slots': manager.memory_slots
    }
    session_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if session_file:
        with open(session_file, 'w') as f:
            json.dump(session_data, f)
        messagebox.showinfo("Success", "Session saved successfully.")

def load_session(manager, memory_tree):
    session_file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if session_file:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        manager.memory_slots = session_data['memory_slots']
        # Update the memory slots on disk
        for file_name, slot, value in manager.memory_slots:
            file_path = os.path.join(manager.memory_dir, file_name)
            with open(file_path, 'a') as file:
                file.write(f"{slot}\t\t\t\t{value}\n")
        # Refresh Memory Explorer
        update_memory_explorer(manager, memory_tree)
        messagebox.showinfo("Success", "Session loaded successfully.")

def delete_session(manager):
    session_file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if session_file:
        os.remove(session_file)
        messagebox.showinfo("Success", "Session deleted successfully.")

def update_memory_explorer(manager, tree):
    for item in tree.get_children():
        tree.delete(item)
    for file_name, slot, value in manager.memory_slots:
        tree.insert("", "end", values=(file_name, slot, value))

def search_memory_explorer(manager, tree, search_entry):
    search_value = search_entry.get().strip()
    if not search_value:
        messagebox.showinfo("Search", "Please enter a value to search for.")
        return
    found = False
    for item in tree.get_children():
        tree.delete(item)
    for file_name, slot, value in manager.memory_slots:
        if search_value in value:
            tree.insert("", "end", values=(file_name, slot, value))
            found = True
    if not found:
        response = messagebox.showinfo("Search", f"Value '{search_value}' not found. You can make the entry addition using the Command Widget on the left of the GUI.")

def main():
    mode = input("Select mode of operation (1: Console, 2: GUI): ").strip()
    allow_duplicates = input("Allow duplicate values in memory slots? (yes/no): ").strip().lower() != 'no'
    manager = MemorySlotManager(no_duplicates=not allow_duplicates)
    
    if mode == '1':
        print("Enter help_command or a command (or 'exit' to quit).")
        while True:
            try:
                user_input = input("__> ").strip()
                if user_input.lower() == 'exit':
                    break
                result = manager.execute_sequence(user_input)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
    elif mode == '2':
        run_gui(manager)

def run_gui(manager):
    def execute_command():
        command = command_entry.get()
        try:
            result = manager.execute_sequence(command)
            output_text.set(result)
            update_memory_explorer(manager, memory_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_output():
        output_text.set("")

    def open_calculator():
        Calculator(root)

    def open_terminal():
        Terminal(root)

    def toggle_widget(widget):
        if widget.winfo_viewable():
            widget.grid_remove()
        else:
            widget.grid()

    root = tk.Tk()
    root.title("Memory Slot Manager")
    root.geometry("1200x700")
    root.attributes('-fullscreen', True)  # Start in full screen mode
    
    primary_color = "#FFFFFF"
    secondary_color = "#000000"
    tertiary_color = "#ADD8E6"
    
    root.configure(bg=primary_color)

    style = ttk.Style()
    style.configure('TLabel', background=primary_color, foreground=secondary_color, font=('Arial', 10))
    style.configure('TButton', background=tertiary_color, font=('Arial', 10, 'bold'))

    command_frame = tk.Frame(root, bg=primary_color, pady=10)
    command_frame.grid(row=0, column=0, columnspan=4, sticky='nsew')

    command_label = ttk.Label(command_frame, text="Command:")
    command_label.grid(row=0, column=0, padx=5)
    
    command_entry = tk.Entry(command_frame, width=50)
    command_entry.grid(row=0, column=1, padx=5)
    
    execute_button = ttk.Button(command_frame, text="Execute", command=execute_command)
    execute_button.grid(row=0, column=2, padx=5)
    
    clear_button = ttk.Button(command_frame, text="Clear Output", command=clear_output)
    clear_button.grid(row=0, column=3, padx=5)
    
    output_frame = tk.Frame(root, bg=primary_color, pady=10)
    output_frame.grid(row=1, column=0, columnspan=4, sticky='nsew')

    output_text = tk.StringVar()
    output_label = ttk.Label(output_frame, textvariable=output_text, background=primary_color, foreground=secondary_color, wraplength=500)
    output_label.pack(fill=tk.X)

    help_frame = tk.Frame(root, bg=primary_color, pady=10)
    help_frame.grid(row=2, column=0, columnspan=4, sticky='nsew')
    
    help_label = ttk.Label(help_frame, text="Help Documentation:")
    help_label.pack(pady=5)
    
    help_text_widget = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, height=10, bg=primary_color, fg=secondary_color)
    help_text_widget.insert(tk.END, manager.get_help_text())
    help_text_widget.config(state=tk.DISABLED)
    help_text_widget.pack(pady=10, fill=tk.BOTH, expand=True)

    explorer_frame = tk.Frame(root, bg=tertiary_color, pady=10)
    explorer_frame.grid(row=0, column=4, rowspan=9, sticky='nsew')
    
    search_label = ttk.Label(explorer_frame, text="Search Slot Value:")
    search_label.pack(pady=5)
    
    search_entry = tk.Entry(explorer_frame, width=20)
    search_entry.pack(pady=5)
    
    search_button = ttk.Button(explorer_frame, text="Search", command=lambda: search_memory_explorer(manager, memory_tree, search_entry))
    search_button.pack(pady=5)

    memory_tree = ttk.Treeview(explorer_frame, columns=("File", "Slot", "Value"), show='headings')
    memory_tree.heading("File", text="File")
    memory_tree.heading("Slot", text="Slot")
    memory_tree.heading("Value", text="Value")
    memory_tree.pack(pady=10, fill=tk.BOTH, expand=True)
    update_memory_explorer(manager, memory_tree)

    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Session", command=lambda: save_session(manager))
    file_menu.add_command(label="Load Session", command=lambda: load_session(manager, memory_tree))
    file_menu.add_command(label="Delete Session", command=lambda: delete_session(manager))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    view_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Toggle Command Frame", command=lambda: toggle_widget(command_frame))
    view_menu.add_command(label="Toggle Output Frame", command=lambda: toggle_widget(output_frame))
    view_menu.add_command(label="Toggle Help Frame", command=lambda: toggle_widget(help_frame))
    view_menu.add_command(label="Toggle Explorer Frame", command=lambda: toggle_widget(explorer_frame))

    tools_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tools", menu=tools_menu)
    tools_menu.add_command(label="Calculator", command=open_calculator)
    tools_menu.add_command(label="Terminal", command=open_terminal)

    root.mainloop()

if __name__ == "__main__":
    main()

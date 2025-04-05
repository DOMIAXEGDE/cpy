import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import re
import zipfile
from io import BytesIO

class DataBankManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Bank Manager")
        self.root.geometry("800x600")
        
        # Application state
        self.app = {
            "maxRegisters": 10,
            "maxAddresses": 20,
            "readingMode": "raw",  # 'raw' or 'resolve'
            "banks": {},
            "currentBankId": None,
            "editMode": {}
        }
        
        # Create UI components
        self.create_ui()
        
        # Load configuration from storage
        self.load_config_from_storage()
    
    def create_ui(self):
        # Create main layout
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create configuration section
        self.create_config_section()
        
        # Create data banks section
        self.create_banks_section()
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="DATA BANK MANAGER", font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Manage and query multi-level reference data files")
        subtitle_label.pack()
    
    def create_config_section(self):
        # Configuration frame
        config_frame = ttk.LabelFrame(self.main_frame, text="BANK CONFIGURATION")
        config_frame.pack(fill=tk.X, pady=5)
        
        # Create grid for form elements
        config_grid = ttk.Frame(config_frame)
        config_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Max Registers
        ttk.Label(config_grid, text="Max Registers Per Bank").grid(row=0, column=0, sticky=tk.W)
        self.max_registers_var = tk.IntVar(value=self.app["maxRegisters"])
        ttk.Spinbox(config_grid, from_=1, to=100, textvariable=self.max_registers_var, 
                    command=self.update_config, width=10).grid(row=0, column=1, padx=5)
        
        # Max Addresses
        ttk.Label(config_grid, text="Max Addresses Per Register").grid(row=0, column=2, sticky=tk.W)
        self.max_addresses_var = tk.IntVar(value=self.app["maxAddresses"])
        ttk.Spinbox(config_grid, from_=1, to=100, textvariable=self.max_addresses_var, 
                    command=self.update_config, width=10).grid(row=0, column=3, padx=5)
        
        # Reading Mode
        ttk.Label(config_grid, text="Reading Mode").grid(row=0, column=4, sticky=tk.W)
        self.reading_mode_var = tk.StringVar(value=self.app["readingMode"])
        reading_mode_combo = ttk.Combobox(config_grid, textvariable=self.reading_mode_var, width=15)
        reading_mode_combo['values'] = ('raw', 'resolve')
        reading_mode_combo.grid(row=0, column=5, padx=5)
        reading_mode_combo.bind('<<ComboboxSelected>>', self.update_reading_mode)
        
        # File actions
        file_frame = ttk.Frame(config_frame)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text="Bank Files").pack(side=tk.LEFT)
        ttk.Button(file_frame, text="UPLOAD FILES", command=self.handle_file_upload).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="CREATE NEW BANK", command=self.show_new_bank_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="DOWNLOAD ALL", command=self.download_all_banks).pack(side=tk.LEFT, padx=5)
    
    def create_banks_section(self):
        # Banks frame
        self.banks_frame = ttk.LabelFrame(self.main_frame, text="DATA BANKS")
        self.banks_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create notebook for bank tabs
        self.bank_tabs = ttk.Notebook(self.banks_frame)
        self.bank_tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind tab change event
        self.bank_tabs.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Add button for new bank (as a tab)
        self.add_bank_button = ttk.Button(self.bank_tabs, text="+ ADD BANK", 
                                          command=self.show_new_bank_modal)
        self.bank_tabs.add(self.add_bank_button, text="+ Add")
    
    def create_status_bar(self):
        self.status_var = tk.StringVar(value="READY")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Configuration methods
    def load_config_from_storage(self):
        try:
            # Try to load from a json file
            if os.path.exists("databank_config.json"):
                with open("databank_config.json", "r") as f:
                    config = json.load(f)
                    self.app["maxRegisters"] = config.get("maxRegisters", 10)
                    self.app["maxAddresses"] = config.get("maxAddresses", 20)
                    self.app["readingMode"] = config.get("readingMode", "raw")
                    
                    # Update UI controls
                    self.max_registers_var.set(self.app["maxRegisters"])
                    self.max_addresses_var.set(self.app["maxAddresses"])
                    self.reading_mode_var.set(self.app["readingMode"])
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config_to_storage(self):
        try:
            with open("databank_config.json", "w") as f:
                json.dump({
                    "maxRegisters": self.app["maxRegisters"],
                    "maxAddresses": self.app["maxAddresses"],
                    "readingMode": self.app["readingMode"]
                }, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def update_config(self):
        try:
            self.app["maxRegisters"] = self.max_registers_var.get()
            self.app["maxAddresses"] = self.max_addresses_var.get()
            self.save_config_to_storage()
            self.show_toast("Configuration updated")
        except Exception as e:
            self.show_toast(f"Error updating config: {e}")
    
    def update_reading_mode(self, event=None):
        previous_mode = self.app["readingMode"]
        self.app["readingMode"] = self.reading_mode_var.get()
        
        if previous_mode != self.app["readingMode"]:
            self.save_config_to_storage()
            self.refresh_all_banks()
            self.show_toast(f"Reading mode changed to: {self.app['readingMode']}")

    # File handling methods
    def handle_file_upload(self):
        files = filedialog.askopenfilenames(
            title="Select Bank Files",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not files:
            return
        
        self.set_status_message("Processing files...")
        
        processed_count = 0
        error_count = 0
        
        for file_path in files:
            # Check filename format (should be number.txt)
            filename = os.path.basename(file_path)
            match = re.match(r'^(\d+)\.txt$', filename)
            
            if not match:
                self.show_toast(f"Skipped {filename} - Invalid filename format. Should be 'number.txt'")
                error_count += 1
                continue
            
            bank_id = int(match.group(1))
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.process_file_content(bank_id, content)
                    processed_count += 1
            except Exception as e:
                error_count += 1
                self.show_toast(f"Failed to read file: {filename} - {str(e)}")
        
        if processed_count + error_count > 0:
            self.set_status_message("File processing complete")
            self.show_toast(f"Processed {processed_count} bank files, {error_count} errors")
    
    def process_file_content(self, bank_id, content):
        try:
            bank = self.parse_bank_data(bank_id, content)
            self.app["banks"][bank_id] = bank
            
            # Create or update the bank tab
            self.create_bank_tab(bank_id)
            
            # If this is the first bank, select it
            if self.app["currentBankId"] is None:
                self.select_bank(bank_id)
            
            self.show_toast(f"Bank {bank_id} loaded successfully")
        except Exception as e:
            self.show_toast(f"Error processing Bank {bank_id}: {str(e)}")
            print(f"Error processing Bank {bank_id}: {e}")
    
    def parse_bank_data(self, bank_id, content):
        lines = content.split('\n')
        bank = {
            "id": bank_id,
            "registers": {}
        }
        
        current_register = None
        
        # Process each line
        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                continue
            
            # Check if it's a register line (no tab at the beginning)
            if not line.startswith('\t'):
                # It's a register number
                try:
                    current_register = int(line.strip())
                except ValueError:
                    raise ValueError(f"Invalid register number at line {i + 1}")
                
                # Initialize register if not exists
                if current_register not in bank["registers"]:
                    bank["registers"][current_register] = {
                        "addresses": {}
                    }
            else:
                # It's an address line (starts with tab)
                if current_register is None:
                    raise ValueError(f"Address found before any register at line {i + 1}")
                
                # Extract the content after the tab
                address_line = line.lstrip('\t')
                
                # Split into address ID and value using the first tab as delimiter
                parts = address_line.split('\t', 1)
                
                # If there's only one part, it might be an empty value
                if len(parts) == 1:
                    try:
                        address_id = int(parts[0].strip())
                    except ValueError:
                        raise ValueError(f"Invalid address format at line {i + 1}")
                    
                    bank["registers"][current_register]["addresses"][address_id] = ""
                else:
                    try:
                        address_id = int(parts[0].strip())
                    except ValueError:
                        raise ValueError(f"Invalid address number at line {i + 1}")
                    
                    # Value is the second part
                    value = parts[1]
                    
                    # Store the address
                    bank["registers"][current_register]["addresses"][address_id] = value
        
        return bank
    
    def create_bank_tab(self, bank_id):
        # Create a new frame for this bank
        bank_frame = ttk.Frame(self.bank_tabs)
        
        # Check if tab already exists
        for i in range(self.bank_tabs.index('end')):
            if self.bank_tabs.tab(i, "text") == f"Bank {bank_id}":
                # Update existing tab
                self.bank_tabs.forget(i)
                self.bank_tabs.insert(i, bank_frame, text=f"Bank {bank_id}")
                return
        
        # Add the new tab before the "+" tab
        add_tab_index = self.bank_tabs.index('end') - 1  # Index of the "+" tab
        self.bank_tabs.insert(add_tab_index, bank_frame, text=f"Bank {bank_id}")
        
        # Store the bank_frame for later reference
        if not hasattr(self, 'bank_frames'):
            self.bank_frames = {}
        self.bank_frames[bank_id] = bank_frame
    
    def select_bank(self, bank_id):
        # Find the tab index for this bank
        for i in range(self.bank_tabs.index('end')):
            if self.bank_tabs.tab(i, "text") == f"Bank {bank_id}":
                self.bank_tabs.select(i)
                self.app["currentBankId"] = bank_id
                self.display_bank_data(bank_id)
                return
    
    def on_tab_changed(self, event):
        selected_tab = self.bank_tabs.select()
        if not selected_tab:
            return
        
        tab_text = self.bank_tabs.tab(selected_tab, "text")
        
        # If it's the "+" tab, don't do anything special
        if tab_text == "+ Add":
            return
        
        # Extract bank ID from tab text
        match = re.match(r'^Bank (\d+)$', tab_text)
        if match:
            bank_id = int(match.group(1))
            self.app["currentBankId"] = bank_id
            self.display_bank_data(bank_id)
    
    def display_bank_data(self, bank_id):
        # Get the bank data
        bank = self.app["banks"].get(bank_id)
        if not bank:
            return
        
        # Get the frame for this bank
        bank_frame = self.bank_frames.get(bank_id)
        if not bank_frame:
            return
        
        # Clear the frame
        for widget in bank_frame.winfo_children():
            widget.destroy()
        
        # Check if in edit mode
        if self.app["editMode"].get(bank_id, False):
            self.display_edit_mode(bank_id, bank_frame)
        else:
            self.display_view_mode(bank_id, bank_frame)
    
    def display_edit_mode(self, bank_id, container):
        bank = self.app["banks"].get(bank_id)
        
        # Create edit control toolbar
        toolbar = ttk.Frame(container)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(toolbar, text=f"Editing Bank {bank_id}").pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Save", command=lambda: self.save_bank_edits(bank_id)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(toolbar, text="Cancel", command=lambda: self.cancel_bank_edits(bank_id)).pack(side=tk.RIGHT, padx=5)
        
        # Create text editor for raw bank data
        text_frame = ttk.Frame(container)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        v_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        
        # Create text widget with scrollbars
        text_editor = tk.Text(text_frame, wrap=tk.NONE, 
                             yscrollcommand=v_scroll.set,
                             xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=text_editor.yview)
        h_scroll.config(command=text_editor.xview)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Generate bank text content
        bank_text = self.generate_bank_text(bank)
        text_editor.insert("1.0", bank_text)
        
        # Save the text editor reference
        if not hasattr(self, 'text_editors'):
            self.text_editors = {}
        self.text_editors[bank_id] = text_editor
    
    def display_view_mode(self, bank_id, container):
        bank = self.app["banks"].get(bank_id)
        
        # Create toolbar
        toolbar = ttk.Frame(container)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(toolbar, text=f"Bank {bank_id}").pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Edit Bank", 
                  command=lambda: self.start_edit_mode(bank_id)).pack(side=tk.RIGHT, padx=5)
        
        # Create a canvas with scrollbar for bank display
        canvas_frame = ttk.Frame(container)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbars
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        
        # Create canvas
        canvas = tk.Canvas(canvas_frame, yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=canvas.yview)
        h_scroll.config(command=canvas.xview)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas for bank content
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)
        
        # Sort registers by ID
        register_ids = sorted([int(r) for r in bank["registers"].keys()])
        
        # Create UI for each register
        for row, register_id in enumerate(register_ids):
            register = bank["registers"][register_id]
            
            # Register frame
            register_frame = ttk.LabelFrame(inner_frame, text=f"Register {register_id}")
            register_frame.grid(row=row, column=0, sticky=tk.W+tk.E, padx=5, pady=5)
            
            # Address list
            addresses_frame = ttk.Frame(register_frame)
            addresses_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Headers for address table
            ttk.Label(addresses_frame, text="Address", width=10).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(addresses_frame, text="Value", width=40).grid(row=0, column=1, sticky=tk.W)
            
            # Sort addresses by ID
            address_ids = sorted([int(a) for a in register["addresses"].keys()])
            
            # Create rows for each address
            for addr_row, address_id in enumerate(address_ids):
                value = register["addresses"][address_id]
                
                # Address ID
                ttk.Label(addresses_frame, text=str(address_id)).grid(row=addr_row+1, column=0, sticky=tk.W)
                
                # Value with or without reference resolution
                if self.app["readingMode"] == "resolve" and self.contains_references(value):
                    # Create a frame for the address to hold both raw and resolved values
                    addr_frame = ttk.Frame(addresses_frame)
                    addr_frame.grid(row=addr_row+1, column=1, sticky=tk.W)
                    
                    # Raw value with reference highlighting
                    raw_text = self.format_value_with_references(addr_frame, value, bank_id, register_id, address_id)
                    
                    # Resolved value
                    resolved_text = self.resolve_value(value)
                    ttk.Label(addr_frame, text=f"→ {resolved_text}", 
                             foreground="blue").pack(anchor=tk.W)
                else:
                    # Just show raw value
                    ttk.Label(addresses_frame, text=value).grid(row=addr_row+1, column=1, sticky=tk.W)
        
        # Update canvas scrollregion
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
    
    def contains_references(self, value):
        if not value:
            return False
        
        # Regular expression to find references (e.g., 1.2.3)
        ref_regex = r'\d+\.\d+\.\d+'
        return bool(re.search(ref_regex, value))
    
    def format_value_with_references(self, parent, value, bank_id, register_id, address_id):
        if not value:
            return
        
        # Create a frame to hold the text with reference buttons
        frame = ttk.Frame(parent)
        frame.pack(anchor=tk.W)
        
        # Regular expression to find references
        ref_regex = r'(\d+\.\d+\.\d+)'
        
        # Split the text by references
        parts = re.split(ref_regex, value)
        
        # Add each part to the frame
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Regular text
                if part:
                    ttk.Label(frame, text=part).pack(side=tk.LEFT)
            else:
                # Reference - make it a button
                ref_btn = ttk.Button(frame, text=part, style='Reference.TButton',
                                    command=lambda p=part: self.handle_reference_click(p))
                ref_btn.pack(side=tk.LEFT)
        
        return frame
    
    def handle_reference_click(self, ref_path):
        # Parse the reference path (e.g., "1.2.3")
        try:
            bank_id, register_id, address_id = map(int, ref_path.split('.'))
            
            # Check if we need to switch banks
            if self.app["currentBankId"] != bank_id and bank_id in self.app["banks"]:
                self.select_bank(bank_id)
            
            # TODO: Highlight the referenced address
            self.show_toast(f"Reference: Bank {bank_id}, Register {register_id}, Address {address_id}")
            
        except Exception as e:
            self.show_toast(f"Invalid reference format: {ref_path}")
    
    def resolve_value(self, value, visited=None):
        if visited is None:
            visited = set()
        
        if not value:
            return ""
        
        # Regular expression to find references
        ref_regex = r'(\d+)\.(\d+)\.(\d+)'
        
        def replace_ref(match):
            b_id = int(match.group(1))
            r_id = int(match.group(2))
            a_id = int(match.group(3))
            
            # Check for circular references
            ref_key = f"{b_id}.{r_id}.{a_id}"
            if ref_key in visited:
                return f"[Circular Ref: {match.group(0)}]"
            
            # Get referenced value
            referenced_value = self.get_referenced_value(b_id, r_id, a_id)
            
            # Handle errors
            if not referenced_value["success"]:
                return f"[{referenced_value['error']}]"
            
            # Check for nested references
            if '.' in referenced_value["value"]:
                new_visited = visited.copy()
                new_visited.add(ref_key)
                return self.resolve_value(referenced_value["value"], new_visited)
            
            return referenced_value["value"]
        
        # Replace references
        return re.sub(ref_regex, replace_ref, value)
    
    def get_referenced_value(self, bank_id, register_id, address_id):
        # Check if bank exists
        if bank_id not in self.app["banks"]:
            return {"success": False, "error": f"Bank {bank_id} not found"}
        
        # Check if register exists
        if register_id not in self.app["banks"][bank_id]["registers"]:
            return {"success": False, "error": f"Register {register_id} not found in Bank {bank_id}"}
        
        # Check if address exists
        if address_id not in self.app["banks"][bank_id]["registers"][register_id]["addresses"]:
            return {"success": False, "error": f"Address {address_id} not found in Bank {bank_id}, Register {register_id}"}
        
        # Return the value
        return {
            "success": True,
            "value": self.app["banks"][bank_id]["registers"][register_id]["addresses"][address_id]
        }

    def start_edit_mode(self, bank_id):
        self.app["editMode"][bank_id] = True
        self.display_bank_data(bank_id)
    
    def save_bank_edits(self, bank_id):
        if bank_id not in self.text_editors:
            return
        
        text_editor = self.text_editors[bank_id]
        bank_text = text_editor.get("1.0", tk.END)
        
        try:
            # Parse the edited text
            updated_bank = self.parse_bank_data(bank_id, bank_text)
            
            # Update the bank
            self.app["banks"][bank_id] = updated_bank
            
            # Exit edit mode
            self.app["editMode"][bank_id] = False
            
            # Refresh display
            self.display_bank_data(bank_id)
            
            self.show_toast(f"Bank {bank_id} saved successfully")
        except Exception as e:
            self.show_toast(f"Error saving bank: {str(e)}")
            print(f"Error saving bank: {e}")
    
    def cancel_bank_edits(self, bank_id):
        self.app["editMode"][bank_id] = False
        self.display_bank_data(bank_id)
    
    def generate_bank_text(self, bank):
        text = ""
        
        # Sort registers by ID
        register_ids = sorted([int(r) for r in bank["registers"].keys()])
        
        for register_id in register_ids:
            register = bank["registers"][register_id]
            
            # Add register header
            text += f"{register_id}\n"
            
            # Sort addresses by ID
            address_ids = sorted([int(a) for a in register["addresses"].keys()])
            
            # Add each address
            for address_id in address_ids:
                value = register["addresses"][address_id]
                text += f"\t{address_id}\t{value}\n"
            
            # Add a blank line between registers
            text += "\n"
        
        return text
    
    def show_new_bank_modal(self):
        # Create a new top-level window
        modal = tk.Toplevel(self.root)
        modal.title("Create New Bank")
        modal.geometry("300x200")
        modal.transient(self.root)  # Make it a child of the main window
        modal.grab_set()  # Make it modal
        
        # Frame for form
        form_frame = ttk.Frame(modal, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Find next available bank ID
        bank_ids = [int(b) for b in self.app["banks"].keys()]
        next_id = 1 if not bank_ids else max(bank_ids) + 1
        
        # Bank ID field
        ttk.Label(form_frame, text="Bank ID Number").grid(row=0, column=0, sticky=tk.W, pady=5)
        bank_id_var = tk.IntVar(value=next_id)
        ttk.Spinbox(form_frame, from_=1, to=9999, textvariable=bank_id_var).grid(row=0, column=1, pady=5)
        
        # Number of registers
        ttk.Label(form_frame, text="Number of Registers").grid(row=1, column=0, sticky=tk.W, pady=5)
        registers_var = tk.IntVar(value=3)
        ttk.Spinbox(form_frame, from_=1, to=self.app["maxRegisters"], 
                   textvariable=registers_var).grid(row=1, column=1, pady=5)
        
        # Addresses per register
        ttk.Label(form_frame, text="Addresses Per Register").grid(row=2, column=0, sticky=tk.W, pady=5)
        addresses_var = tk.IntVar(value=5)
        ttk.Spinbox(form_frame, from_=1, to=self.app["maxAddresses"], 
                   textvariable=addresses_var).grid(row=2, column=1, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Create and Cancel buttons
        ttk.Button(btn_frame, text="Cancel", 
                  command=modal.destroy).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Create", 
                  command=lambda: self.create_new_bank(
                      bank_id_var.get(), 
                      registers_var.get(), 
                      addresses_var.get(), 
                      modal)).pack(side=tk.LEFT, padx=5)
    
    def create_new_bank(self, bank_id, num_registers, num_addresses, modal):
        # Validate inputs
        if bank_id < 1:
            self.show_toast("Bank ID must be a positive number")
            return
        
        if num_registers < 1 or num_registers > self.app["maxRegisters"]:
            self.show_toast(f"Number of registers must be between 1 and {self.app['maxRegisters']}")
            return
        
        if num_addresses < 1 or num_addresses > self.app["maxAddresses"]:
            self.show_toast(f"Number of addresses must be between 1 and {self.app['maxAddresses']}")
            return
        
        # Check if bank already exists
        if bank_id in self.app["banks"]:
            if not messagebox.askyesno("Confirm Overwrite", 
                                     f"Bank {bank_id} already exists. Overwrite?"):
                return
        
        # Create empty bank
        bank = {
            "id": bank_id,
            "registers": {}
        }
        
        # Create registers and addresses
        for r in range(1, num_registers + 1):
            bank["registers"][r] = {
                "addresses": {}
            }
            
            for a in range(1, num_addresses + 1):
                bank["registers"][r]["addresses"][a] = f"Value {r}.{a}"
        
        # Add to app state
        self.app["banks"][bank_id] = bank
        
        # Create tab and select it
        self.create_bank_tab(bank_id)
        self.select_bank(bank_id)
        
        # Enter edit mode
        self.app["editMode"][bank_id] = True
        self.display_bank_data(bank_id)
        
        # Close modal
        modal.destroy()
        
        self.show_toast(f"Bank {bank_id} created successfully")
    
    def download_all_banks(self):
        bank_ids = list(self.app["banks"].keys())
        if not bank_ids:
            self.show_toast("No banks to download")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
            title="Save All Banks As ZIP"
        )
        
        if not file_path:
            return
        
        self.set_status_message("Creating ZIP file...")
        
        try:
            # Create ZIP file
            with zipfile.ZipFile(file_path, 'w') as zip_file:
                for bank_id in bank_ids:
                    bank = self.app["banks"][bank_id]
                    content = self.generate_bank_text(bank)
                    zip_file.writestr(f"{bank_id}.txt", content)
            
            self.set_status_message("ZIP file downloaded")
            self.show_toast(f"{len(bank_ids)} banks downloaded as ZIP")
            
        except Exception as e:
            self.set_status_message("Error creating ZIP file")
            self.show_toast(f"Failed to create ZIP file: {str(e)}")
            print(f"Error creating ZIP: {e}")
    
    def refresh_all_banks(self):
        # Refresh the current bank display if any
        if self.app["currentBankId"] is not None:
            self.display_bank_data(self.app["currentBankId"])
    
    # Utility methods
    def set_status_message(self, message):
        self.status_var.set(message)
    
    def show_toast(self, message):
        # Simple implementation - just show as a messagebox for now
        # In a full implementation, this could be a temporary pop-up
        messagebox.showinfo("Notification", message)

def main():
    root = tk.Tk()
    app = DataBankManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import json
import os
import zipfile
import re
from datetime import datetime

class MemorySlotManager:
    def __init__(self):
        self.memory_slots = {}  # Structure: memory_slots[file_number][slot_number] = value
        
    def assign_slot(self, file_number, slot_number, value):
        """Assigns a multi-line value to a specific slot in a file."""
        if not file_number or not slot_number or not value:
            return 'Error: Invalid input parameters.'
        
        if self.value_exists(value):
            return f'Error: The value already exists in another memory slot.'
        
        if file_number not in self.memory_slots:
            self.memory_slots[file_number] = {}
            
        self.memory_slots[file_number][slot_number] = value
        return f'Assigned value to slot {slot_number} in file {file_number}.'
    
    def read_slot(self, file_number, slot_number):
        """Reads the value from a specific slot in a file."""
        if file_number in self.memory_slots and slot_number in self.memory_slots[file_number]:
            return self.memory_slots[file_number][slot_number]
        return f'Slot {slot_number} not found in file {file_number}.'
    
    def get_last_slot_number(self, file_number):
        """Gets the last slot number in a specific file."""
        if file_number in self.memory_slots and self.memory_slots[file_number]:
            try:
                slots = [int(slot) for slot in self.memory_slots[file_number].keys() if slot.isdigit()]
                if slots:
                    return max(slots)
            except:
                pass
        return None
    
    def search_value(self, value):
        """Searches for a value across all memory slots (case-insensitive)."""
        results = []
        search_value_lower = value.lower()
        
        for file, slots in self.memory_slots.items():
            for slot, val in slots.items():
                if search_value_lower in val.lower():
                    results.append({"file": file, "slot": slot, "value": val})
        
        return results
    
    def value_exists(self, value):
        """Checks if a value exists in any memory slot (case-insensitive)."""
        value_lower = value.lower()
        
        for slots in self.memory_slots.values():
            for val in slots.values():
                if val.lower() == value_lower:
                    return True
        
        return False
    
    def call_slot_range(self, file_number, start_slot, end_slot):
        """Calls values from a specific slot or a range of slots in a file."""
        if file_number not in self.memory_slots:
            return f'File {file_number} not found.'
        
        results = []
        for slot in range(start_slot, end_slot + 1):
            slot_str = str(slot)
            if slot_str in self.memory_slots[file_number]:
                results.append(f'Slot {slot}:\n{self.memory_slots[file_number][slot_str]}')
            else:
                results.append(f'Slot {slot} not found.')
        
        return '\n\n'.join(results)
    
    def export_to_text_file(self, file_number, file_path):
        """Exports a specific file's memory slots to a text file."""
        if file_number not in self.memory_slots:
            return f"Error: File {file_number} not found."
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                slots = self.memory_slots[file_number]
                # Sort the slots numerically if possible
                try:
                    slot_keys = sorted([int(key) for key in slots.keys() if key.isdigit()])
                    slot_keys = [str(key) for key in slot_keys]
                except:
                    slot_keys = sorted(slots.keys())
                
                for slot in slot_keys:
                    value = slots[slot]
                    # Format: SLOT <number>
                    f.write(f"SLOT {slot}\n")
                    # Then the value, indented with tabs or spaces
                    for line in value.split('\n'):
                        f.write(f"{line}\n")
                    # Add a separator between slots
                    f.write("--------------------\n")
            
            return f"Exported file {file_number} to {os.path.basename(file_path)}"
        except Exception as e:
            return f"Error exporting to text file: {str(e)}"
    
    def parse_text_file(self, file_path):
        """Parses a text file containing memory slots and returns the file number and slots."""
        try:
            # Extract file number from filename (e.g., "file1.txt" -> "1")
            file_name = os.path.basename(file_path)
            file_number_match = re.search(r'(\d+)', file_name)
            file_number = file_number_match.group(1) if file_number_match else "1"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content by the SLOT marker
            slot_sections = re.split(r'SLOT\s+(\d+)', content)
            
            # The first element will be any text before the first SLOT marker
            if slot_sections and not slot_sections[0].strip():
                slot_sections = slot_sections[1:]
            
            slots = {}
            slot_number = None
            
            # Process each section (alternating between slot number and content)
            for i, section in enumerate(slot_sections):
                if i % 2 == 0:  # This is a slot number
                    slot_number = section.strip()
                else:  # This is slot content
                    # Clean up the content by removing the separator
                    cleaned_content = re.sub(r'--------------------\s*$', '', section, flags=re.MULTILINE).strip()
                    slots[slot_number] = cleaned_content
            
            return file_number, slots
        except Exception as e:
            raise Exception(f"Error parsing text file: {str(e)}")

class CyberMemoryConsoleApp:
    def __init__(self):
        self.memory_manager = MemorySlotManager()
        self.running = True
        self.show_welcome_message()
        
    def show_welcome_message(self):
        """Shows the welcome message when the application starts."""
        print("\n" + "=" * 60)
        print("      CYBER MEMORY SLOT MANAGER v1.0 (CONSOLE EDITION)")
        print("=" * 60)
        print(f"SYSTEM INITIALIZED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("MEMORY MANAGER LOADED")
        print("READY FOR INPUT")
        print("=" * 60)
        print('Type "help" for a list of commands.\n')
        
    def show_help(self):
        """Displays the help information."""
        help_text = """
AVAILABLE COMMANDS:
------------------
assign <fileNumber> <slotNumber>
  <value>             : Assign a multi-line value to a slot
                        (Enter your multi-line value after the first line)
                        Type 'END' on a line by itself to finish input

read <fileNumber> <slotNumber>
                     : Read the value from a slot

last_slot <fileNumber>
                     : Get the last slot number in a file

search
  <value>             : Search for a multi-line value across all slots
                        (Type 'END' on a line by itself to finish input)

call <fileNumber> <startSlot> <endSlot>
                     : Call values from a range of slots

export <fileNumber> <filePath>
                     : Export a file's memory slots to a text file

display               : Show all memory slots
clear                 : Clear the screen
help                  : Display this help message
exit                  : Exit the application

load_json <filePath>  : Load memory slots from a JSON file
load_txt <filePath>   : Load memory slots from a text file
save_json <filePath>  : Save all memory slots to a JSON file
save_txt <fileNumber> <filePath>
                     : Save a file's memory slots to a text file
save_zip <filePath>   : Save all memory slots to a ZIP archive
export_all_txt <dirPath>
                     : Export all files as separate text files

FILE FORMATS:
------------------
JSON                 : Standard format with nested objects
                       {fileNumber: {slotNumber: value, ...}, ...}
                       
TXT                  : Text format with SLOT markers
                       SLOT <number>
                       <value content>
                       --------------------
"""
        print(help_text)
        
    def execute_command(self, command_input):
        """Executes a command from user input."""
        if not command_input:
            return

        # Split the command input into lines to handle multi-line values
        command_lines = command_input.strip().split('\n')
        tokens = command_lines[0].strip().split()
        
        if not tokens:
            return
        
        command = tokens[0].lower()
        output = ""
        
        try:
            if command == "assign":
                if len(tokens) < 3:
                    output = "Error: Missing arguments for assign command."
                else:
                    file_number, slot_number = tokens[1:3]
                    value = '\n'.join(command_lines[1:])
                    if not value:
                        output = "Error: No value provided for assign command."
                    else:
                        output = self.memory_manager.assign_slot(file_number, slot_number, value)
            
            elif command == "read":
                if len(tokens) < 3:
                    output = "Error: Missing arguments for read command."
                else:
                    output = self.memory_manager.read_slot(tokens[1], tokens[2])
            
            elif command == "last_slot":
                if len(tokens) < 2:
                    output = "Error: Missing file number for last_slot command."
                else:
                    last_slot = self.memory_manager.get_last_slot_number(tokens[1])
                    if last_slot is not None:
                        output = f"Last slot number in file {tokens[1]} is {last_slot}."
                    else:
                        output = f"No slots found in file {tokens[1]}."
            
            elif command == "search":
                if len(tokens) < 2 and len(command_lines) < 2:
                    output = "Error: Missing search value."
                else:
                    # For search, we need to handle multi-line input correctly
                    # If the first line contains just "search", use the rest as the search value
                    # Otherwise, use everything after "search" in the first line
                    if len(tokens) == 1:
                        search_value = '\n'.join(command_lines[1:])
                    else:
                        first_line_value = ' '.join(tokens[1:])
                        if len(command_lines) > 1:
                            search_value = first_line_value + '\n' + '\n'.join(command_lines[1:])
                        else:
                            search_value = first_line_value
                    
                    search_results = self.memory_manager.search_value(search_value)
                    if search_results:
                        output = "Search Results:\n"
                        for result in search_results:
                            output += f"File: {result['file']}, Slot: {result['slot']}, Value:\n{result['value']}\n\n"
                    else:
                        output = "No results found."
            
            elif command == "call":
                if len(tokens) < 4:
                    output = "Error: Missing arguments for call command."
                else:
                    try:
                        file_number = tokens[1]
                        start_slot = int(tokens[2])
                        end_slot = int(tokens[3])
                        output = self.memory_manager.call_slot_range(file_number, start_slot, end_slot)
                    except ValueError:
                        output = "Error: Slot numbers must be integers."
            
            elif command == "export":
                if len(tokens) < 3:
                    output = "Error: Missing arguments for export command."
                else:
                    file_number = tokens[1]
                    file_path = tokens[2]
                    output = self.memory_manager.export_to_text_file(file_number, file_path)
            
            elif command == "help":
                self.show_help()
                return
            
            elif command == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                return
            
            elif command == "display" or command == "show":
                self.display_all_memory()
                return
                
            elif command == "exit" or command == "quit":
                self.running = False
                print("Exiting Cyber Memory Slot Manager. Goodbye!")
                return
                
            elif command == "load_json":
                if len(tokens) < 2:
                    output = "Error: Missing file path for load_json command."
                else:
                    file_path = tokens[1]
                    output = self.load_json_file(file_path)
                    
            elif command == "load_txt":
                if len(tokens) < 2:
                    output = "Error: Missing file path for load_txt command."
                else:
                    file_path = tokens[1]
                    output = self.load_txt_file(file_path)
                    
            elif command == "save_json":
                if len(tokens) < 2:
                    output = "Error: Missing file path for save_json command."
                else:
                    file_path = tokens[1]
                    output = self.save_json_file(file_path)
                    
            elif command == "save_txt":
                if len(tokens) < 3:
                    output = "Error: Missing arguments for save_txt command."
                else:
                    file_number = tokens[1]
                    file_path = tokens[2]
                    output = self.save_txt_file(file_number, file_path)
                    
            elif command == "save_zip":
                if len(tokens) < 2:
                    output = "Error: Missing file path for save_zip command."
                else:
                    file_path = tokens[1]
                    output = self.save_zip_file(file_path)
                    
            elif command == "export_all_txt":
                if len(tokens) < 2:
                    output = "Error: Missing directory path for export_all_txt command."
                else:
                    directory_path = tokens[1]
                    output = self.export_all_txt(directory_path)
                    
            else:
                output = f"Unknown command: {command}\nType 'help' for a list of commands."
                
        except Exception as e:
            output = f"Error: {str(e)}"
        
        print(f"\n>>> {output}\n")
        
    def display_all_memory(self):
        """Displays all memory slots."""
        if not self.memory_manager.memory_slots:
            print("\n>>> No memory slots available.\n")
            return
            
        print("\n" + "=" * 60)
        print("MEMORY SLOT CONTENTS")
        print("=" * 60)
        
        for file_number, slots in self.memory_manager.memory_slots.items():
            print(f"\nFILE {file_number}:")
            print("-" * 40)
            
            # Sort slots numerically if possible
            try:
                slot_numbers = sorted([int(slot) for slot in slots.keys() if slot.isdigit()])
                slot_numbers = [str(num) for num in slot_numbers]
            except:
                slot_numbers = sorted(slots.keys())
                
            for slot in slot_numbers:
                value = slots[slot]
                # Truncate long values for display
                display_value = value
                if len(display_value) > 100:
                    display_value = display_value[:97] + "..."
                
                # Replace newlines with visible indicator for console display
                display_value = display_value.replace("\n", " ⏎ ")
                
                print(f"Slot {slot}: {display_value}")
        
        print("\n" + "=" * 60)
        
    def load_json_file(self, file_path):
        """Loads memory slots from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                
                # Get a file number from the filename
                file_name = os.path.basename(file_path)
                file_number_match = re.search(r'(\d+)', file_name)
                file_number = file_number_match.group(1) if file_number_match else "1"
                
                if isinstance(content, dict):
                    # Check if this is already in our expected format {file: {slot: value}}
                    if any(isinstance(v, dict) for v in content.values()):
                        # It's our full structure
                        for file_key, slots in content.items():
                            if file_key not in self.memory_manager.memory_slots:
                                self.memory_manager.memory_slots[file_key] = {}
                            
                            for slot_number, value in slots.items():
                                if isinstance(value, str):
                                    self.memory_manager.memory_slots[file_key][str(slot_number)] = value
                                elif isinstance(value, (dict, list)):
                                    self.memory_manager.memory_slots[file_key][str(slot_number)] = json.dumps(value, indent=2)
                                else:
                                    self.memory_manager.memory_slots[file_key][str(slot_number)] = str(value)
                    else:
                        # It's a single file's slots {slot: value}
                        if file_number not in self.memory_manager.memory_slots:
                            self.memory_manager.memory_slots[file_number] = {}
                        
                        for slot_number, value in content.items():
                            if isinstance(value, str):
                                self.memory_manager.memory_slots[file_number][str(slot_number)] = value
                            elif isinstance(value, (dict, list)):
                                self.memory_manager.memory_slots[file_number][str(slot_number)] = json.dumps(value, indent=2)
                            else:
                                self.memory_manager.memory_slots[file_number][str(slot_number)] = str(value)
            
            return f"Loaded JSON file: {os.path.basename(file_path)}"
        except Exception as e:
            return f"Error loading {os.path.basename(file_path)}: {str(e)}"
        
    def load_txt_file(self, file_path):
        """Loads memory slots from a text file."""
        try:
            file_number, slots = self.memory_manager.parse_text_file(file_path)
            
            if file_number not in self.memory_manager.memory_slots:
                self.memory_manager.memory_slots[file_number] = {}
            
            # Add the loaded slots to our memory
            for slot_number, value in slots.items():
                self.memory_manager.memory_slots[file_number][slot_number] = value
            
            return f"Loaded text file: {os.path.basename(file_path)} as file {file_number}"
        except Exception as e:
            return f"Error loading {os.path.basename(file_path)}: {str(e)}"
        
    def save_json_file(self, file_path):
        """Saves memory slots to a JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.memory_manager.memory_slots, file, indent=2, ensure_ascii=False)
            
            return f"Memory slots saved to JSON: {os.path.basename(file_path)}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
        
    def save_txt_file(self, file_number, file_path):
        """Saves a specific file's memory slots to a text file."""
        try:
            result = self.memory_manager.export_to_text_file(file_number, file_path)
            return result
        except Exception as e:
            return f"Error exporting to text file: {str(e)}"
        
    def save_zip_file(self, file_path):
        """Saves all memory slots as separate JSON and text files in a zip archive."""
        try:
            with zipfile.ZipFile(file_path, 'w') as zip_file:
                # Add JSON files
                for file_number, slots in self.memory_manager.memory_slots.items():
                    # Create a JSON string for this file's slots
                    json_data = json.dumps(slots, indent=2, ensure_ascii=False)
                    
                    # Add the JSON data to the zip file
                    zip_file.writestr(f"json/file_{file_number}.json", json_data.encode('utf-8'))
                    
                    # Also create a text file version
                    txt_data = ""
                    for slot, value in slots.items():
                        txt_data += f"SLOT {slot}\n{value}\n--------------------\n"
                    
                    zip_file.writestr(f"txt/file_{file_number}.txt", txt_data.encode('utf-8'))
                
                # Also save the complete structure as one JSON file
                complete_json = json.dumps(self.memory_manager.memory_slots, indent=2, ensure_ascii=False)
                zip_file.writestr(f"all_memory_slots.json", complete_json.encode('utf-8'))
            
            return f"Memory slots saved to zip archive: {os.path.basename(file_path)}"
        except Exception as e:
            return f"Error creating zip archive: {str(e)}"
        
    def export_all_txt(self, export_dir):
        """Exports all files as separate text files."""
        if not self.memory_manager.memory_slots:
            return "No memory slots available to export."
        
        if not os.path.exists(export_dir):
            try:
                os.makedirs(export_dir)
            except Exception as e:
                return f"Error creating directory: {str(e)}"
        
        success_count = 0
        error_count = 0
        errors = []
        
        for file_number in self.memory_manager.memory_slots.keys():
            file_path = os.path.join(export_dir, f"file{file_number}.txt")
            try:
                self.memory_manager.export_to_text_file(file_number, file_path)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Error exporting file {file_number}: {str(e)}")
        
        result = f"Exported {success_count} files as text files"
        if error_count > 0:
            result += f", {error_count} files had errors."
            for error in errors:
                result += f"\n{error}"
        else:
            result += "."
            
        return result
        
    def run(self):
        """Main application loop."""
        while self.running:
            try:
                print(f"{datetime.now().strftime('%H:%M:%S')} > ", end="")
                cmd = input()
                
                # Handle multi-line input for assign and search commands
                if cmd.lower().startswith("assign ") or cmd.lower() == "search" or cmd.lower().startswith("search "):
                    print("Enter multi-line value (type 'END' on a line by itself to finish):")
                    lines = [cmd]
                    while True:
                        line = input()
                        if line.strip() == "END":
                            break
                        lines.append(line)
                    
                    # Process the multi-line command
                    self.execute_command("\n".join(lines))
                else:
                    # Process a single-line command
                    self.execute_command(cmd)
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled. Type 'exit' to quit the application.")
            except EOFError:
                print("\nExiting Cyber Memory Slot Manager. Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\n>>> Error: {str(e)}\n")

if __name__ == "__main__":
    app = CyberMemoryConsoleApp()
    app.run()

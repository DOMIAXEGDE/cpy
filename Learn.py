import os

class MemorySlotManager:
    def __init__(self, memory_dir="memory_slots", no_duplicates=False):
        self.memory_dir = memory_dir
        self.no_duplicates = no_duplicates
        os.makedirs(self.memory_dir, exist_ok=True)

    def write_memory_slot(self, file_number, slot_number, value):
        file_path = self._get_file_path(file_number)
        with open(file_path, 'a') as file:
            file.write(f"{slot_number}\t\t\t\t{value.replace('\n', '\\n').replace('\t', '\\t')}\n")

    def read_memory_slot(self, file_number, slot_number, entry_id=None):
        file_path = self._get_file_path(file_number)
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_number}.txt does not exist.")
        entries = []
        with open(file_path, 'r') as file:
            for idx, line in enumerate(file, start=1):
                slot, value = line.split('\t\t\t\t', 1)
                if int(slot) == slot_number:
                    entries.append((idx, value.replace('\\n', '\n').replace('\\t', '\t').strip()))
        if entry_id is not None:
            return entries[entry_id - 1][1]
        return entries

    def seek_read_memory_slot(self, file_name, slot_number):
        file_path = os.path.join(self.memory_dir, file_name)
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_name} does not exist.")
        with open(file_path, 'r') as file:
            for line in file:
                slot, value = line.split('\t\t\t\t', 1)
                if slot == str(slot_number):
                    return value.replace('\\n', '\n').replace('\\t', '\t').strip()
        return None

    def get_last_slot_number(self, file_number):
        file_path = self._get_file_path(file_number)
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_number}.txt does not exist.")
        last_slot_number = None
        with open(file_path, 'r') as file:
            for line in file:
                slot, _ = line.split('\t\t\t\t', 1)
                last_slot_number = int(slot)
        if last_slot_number is None:
            raise ValueError(f"No slots found in file {file_number}.txt.")
        return last_slot_number

    def check_duplicate_assignment(self, file_number, slot_number, value):
        file_path = self._get_file_path(file_number)
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as file:
            for line in file:
                slot, existing_value = line.split('\t\t\t\t', 1)
                if int(slot) == slot_number and existing_value.strip() == value.replace('\n', '\\n').replace('\t', '\\t'):
                    return True
        return False

    def check_value_exists(self, value):
        for file_name in os.listdir(self.memory_dir):
            file_path = os.path.join(self.memory_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    _, existing_value = line.split('\t\t\t\t', 1)
                    if existing_value.strip() == value.replace('\n', '\\n').replace('\t', '\\t'):
                        return int(file_name.split('.')[0])
        return None

    def request_check_value_exists(self, value):
        for file_name in os.listdir(self.memory_dir):
            file_path = os.path.join(self.memory_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    slot, existing_value = line.split('\t\t\t\t', 1)
                    if existing_value.strip() == value.replace('\n', '\\n').replace('\t', '\\t'):
                        slot = self.seek_read_memory_slot(file_name, slot)
                        return file_name.strip('.txt'), slot
        return None

    def execute_sequence(self, sequence):
        try:
            tokens = sequence.split(maxsplit=3)
            command = tokens[0]

            if command == 'assign':
                current_file, slot_number, value_or_reference = self._parse_assign_command(tokens)
                value = self._resolve_value(value_or_reference)
                return self._handle_assign(current_file, slot_number, value)

            elif '.' in command:
                if len(tokens) == 2:
                    return self._handle_read_slot(command, entry_id=int(tokens[1]))
                return self._handle_read_slot(command)

            elif command == 'last_slot':
                file_number = int(tokens[1])
                return self._handle_last_slot(file_number)

            elif command == 'check_duplicate':
                return self._handle_check_duplicate(tokens)

            elif command == 'help_command':
                return self.get_help_text()

            elif command == 'value_exists':
                return self._handle_value_exists(tokens)

            else:
                return "Invalid sequence"
        except Exception as e:
            return f"Error: {e}"

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
        
        - <file_number>.<slot_number> <entry_id>
            Retrieves and prints the specific entry from the specified slot in the specified file.
            Example: 3.1 2

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

    def _get_file_path(self, file_number):
        return os.path.join(self.memory_dir, f"{file_number}.txt")

    def _parse_assign_command(self, tokens):
        current_file = int(tokens[1])
        slot_number = int(tokens[2])
        value_or_reference = tokens[3]
        return current_file, slot_number, value_or_reference

    def _resolve_value(self, value_or_reference):
        if '.' in value_or_reference:
            ref_file, ref_slot = map(int, value_or_reference.split('.'))
            return self.read_memory_slot(ref_file, ref_slot)
        return value_or_reference

    def _handle_assign(self, current_file, slot_number, value):
        if self.no_duplicates and self.check_value_exists(value):
            return f"Error: Value '{value}' already exists in the memory slots."
        if self.check_duplicate_assignment(current_file, slot_number, value):
            return f"Duplicate assignment detected: {value} is already assigned to slot {slot_number} in file {current_file}."
        self.write_memory_slot(current_file, slot_number, value)
        return f"Assigned '{value}' to slot {slot_number} in file {current_file}."

    def _handle_read_slot(self, command, entry_id=None):
        file_number, slot_number = map(int, command.split('.'))
        entries = self.read_memory_slot(file_number, slot_number)
        if entry_id is not None:
            return entries[entry_id - 1][1]
        return "\n".join([f"{idx}. {entry[1]}" for idx, entry in entries])

    def _handle_last_slot(self, file_number):
        last_slot_number = self.get_last_slot_number(file_number)
        return f"The last slot number in file {file_number}.txt is {last_slot_number}"

    def _handle_check_duplicate(self, tokens):
        file_number = int(tokens[1])
        slot_number = int(tokens[2])
        value = tokens[3]
        if self.check_duplicate_assignment(file_number, slot_number, value):
            return f"Duplicate: {value} is already assigned to slot {slot_number} in file {file_number}."
        return f"No duplicate found: {value} is not assigned to slot {slot_number} in file {file_number}."

    def _handle_value_exists(self, tokens):
        value_or_reference = tokens[3]
        result = self.request_check_value_exists(value_or_reference)
        if result:
            file_name, slot = result
            return f"Value '{value_or_reference}' exists in file {file_name}, slot {slot}."
        return "Value not found in file base."

def main():
    print("\n\n\tWelcome to Learn\n\n")
    allow_duplicates = input("Allow duplicate values in memory slots? (yes/no): ").strip().lower() != 'no'
    mode = input("Select mode of operation (1: Console, 2: quit): ").strip()
    
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
        exit()

if __name__ == "__main__":
    main()

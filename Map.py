import os
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from concurrent.futures import ThreadPoolExecutor

# Function to load custom charset from configuration file
def load_custom_charset(config_file):
    custom_charset = []
    if not os.path.exists(config_file):
        print(f"Error opening configuration file: {config_file}")
        return custom_charset
    with open(config_file, 'r', encoding='utf-8') as file:
        custom_charset = list(file.read())
    return custom_charset

# Function to save custom charset to configuration file
def save_custom_charset(custom_charset, config_file):
    with open(config_file, 'w', encoding='utf-8') as file:
        file.write(''.join(custom_charset))

# Function to validate charset
def validate_charset(charset):
    if len(charset) < 2:
        raise ValueError("Charset must contain at least two characters.")

# Function to generate combinations and write to individual files
def generate_combinations(charset, n, output_file, use_multithreading=False):
    validate_charset(charset)
    k = len(charset) - 1
    nbr_comb = int(math.pow(k + 1, n))

    def write_combination(row):
        id = row + 1
        combination = f"{id}\t"
        for col in range(n - 1, -1, -1):
            rdiv = int(math.pow(k + 1, col))
            cell = (row // rdiv) % (k + 1)
            combination += charset[cell]
        return combination + "\n"

    with open(output_file, 'w', encoding='utf-8') as file:
        if use_multithreading:
            with ThreadPoolExecutor() as executor:
                combinations = executor.map(write_combination, range(nbr_comb))
                for combination in combinations:
                    file.write(combination)
        else:
            for row in range(nbr_comb):
                file.write(write_combination(row))

# Function to calculate string ID
def calculate_string_id(input_string, charset):
    char_map = {c: i for i, c in enumerate(charset)}
    id = 0
    k = len(charset)
    for c in input_string:
        id = id * k + char_map[c]
    return id

# Function to decode ID back to string
def decode_id(id, charset):
    k = len(charset)
    chars = []
    while id > 0:
        chars.append(charset[id % k])
        id //= k
    return ''.join(reversed(chars)) if chars else charset[0]

# Function to append content to a file
def append_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content + "\n")

# Function to read content from a file
def read_file(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return ""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Function to list all files in the current directory
def list_files():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    if files:
        print("Available files:")
        for file in files:
            print(file)
    else:
        print("No files found.")

# Function to delete a file
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' deleted.")
    else:
        print(f"File '{filename}' not found.")

# Function to rename a file
def rename_file(old_name, new_name):
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"File '{old_name}' renamed to '{new_name}'.")
    else:
        print(f"File '{old_name}' not found.")

# Function to encode a text file to unique IDs character-by-character
def encode_file(input_file, output_file, charset):
    content = read_file(input_file)
    if not content:
        return
    with open(output_file, 'w', encoding='utf-8') as file:
        for char in content:
            id = calculate_string_id(char, charset)
            file.write(f"{id} ")
        file.write("\n")
    print(f"Encoded content saved to {output_file}")

# Function to decode a file of IDs back to text
def decode_file(input_file, output_file, charset):
    content = read_file(input_file)
    if not content:
        return
    ids = content.split()
    with open(output_file, 'w', encoding='utf-8') as file:
        for id_str in ids:
            try:
                id = int(id_str)
                decoded_string = decode_id(id, charset)
                file.write(decoded_string)
            except ValueError:
                print(f"Invalid ID '{id_str}' in {input_file}")
    print(f"Decoded content saved to {output_file}")

class CharsetApp(App):

    def build(self):
        self.charset = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            ' ', '\n', '\t', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
            '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', 
            '¦', '#', '%'
        ]

        extended_charset = [chr(i) for i in range(128, 256)]
        self.charset.extend(extended_charset)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.input_file = TextInput(hint_text='Enter the name of the input file', size_hint_y=None, height=40)
        layout.add_widget(self.input_file)

        self.output_file = TextInput(hint_text='Enter the name of the output file', size_hint_y=None, height=40)
        layout.add_widget(self.output_file)

        self.charset_file = TextInput(hint_text='Enter the name of the charset file', size_hint_y=None, height=40)
        layout.add_widget(self.charset_file)

        load_charset_button = Button(text="Load Charset", size_hint_y=None, height=40, background_color=(0.2, 0.6, 0.8, 1))
        load_charset_button.bind(on_press=self.load_charset)
        layout.add_widget(load_charset_button)

        encode_button = Button(text="Encode File", size_hint_y=None, height=40, background_color=(0.2, 0.8, 0.2, 1))
        encode_button.bind(on_press=self.encode_file)
        layout.add_widget(encode_button)

        decode_button = Button(text="Decode File", size_hint_y=None, height=40, background_color=(0.8, 0.2, 0.2, 1))
        decode_button.bind(on_press=self.decode_file)
        layout.add_widget(decode_button)

        generate_combinations_button = Button(text="Generate Combinations", size_hint_y=None, height=40, background_color=(0.8, 0.6, 0.2, 1))
        generate_combinations_button.bind(on_press=self.show_generate_combinations_popup)
        layout.add_widget(generate_combinations_button)

        self.custom_string_input = TextInput(hint_text='Enter your custom string', size_hint_y=None, height=40)
        layout.add_widget(self.custom_string_input)

        calculate_id_button = Button(text="Calculate String ID", size_hint_y=None, height=40, background_color=(0.6, 0.3, 0.8, 1))
        calculate_id_button.bind(on_press=self.calculate_string_id_action)
        layout.add_widget(calculate_id_button)

        save_checkbox_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=10, spacing=10)
        save_checkbox_label = Label(text="Auto-save to file", size_hint=(0.8, 1))
        self.save_checkbox = CheckBox(size_hint=(0.2, 1))
        save_checkbox_layout.add_widget(save_checkbox_label)
        save_checkbox_layout.add_widget(self.save_checkbox)
        layout.add_widget(save_checkbox_layout)

        self.output_label = Label(size_hint_y=None, height=40)
        layout.add_widget(self.output_label)

        return layout

    def show_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message, size_hint_y=None, height=40)
        close_button = Button(text="Close", size_hint_y=None, height=40)
        layout.add_widget(label)
        layout.add_widget(close_button)
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_generate_combinations_popup(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.n_input = TextInput(hint_text='Enter the size of combinations (n)', size_hint_y=None, height=40)
        layout.add_widget(self.n_input)

        self.output_file_input = TextInput(hint_text='Enter the name of the output file', size_hint_y=None, height=40)
        layout.add_widget(self.output_file_input)

        self.multithreading_spinner = Spinner(
            text='Use Multithreading',
            values=('Yes', 'No'),
            size_hint_y=None, height=40
        )
        layout.add_widget(self.multithreading_spinner)

        generate_button = Button(text="Generate", size_hint_y=None, height=40, background_color=(0.6, 0.3, 0.8, 1))
        layout.add_widget(generate_button)

        self.popup = Popup(title="Generate Combinations", content=layout, size_hint=(0.8, 0.6))
        generate_button.bind(on_press=self.generate_combinations_action)
        self.popup.open()

    def load_charset(self, instance):
        charset_file = self.charset_file.text
        if charset_file:
            if os.path.exists(charset_file):
                with open(charset_file, 'r', encoding='utf-8') as file:
                    for line in file:
                        char = line.strip()
                        if char and char not in self.charset:
                            self.charset.append(char)
                self.show_popup("Charset Loaded", f"Charset loaded from {charset_file}")
            else:
                self.show_popup("Error", f"Charset file {charset_file} not found.")
        else:
            self.show_popup("Error", "Please provide the charset file name.")

    def encode_file(self, instance):
        input_file = self.input_file.text
        output_file = self.output_file.text
        if input_file and output_file:
            content = self.read_file(input_file)
            if not content:
                self.show_popup("Error", "Input file not found.")
                return

            with open(output_file, 'w', encoding='utf-8') as file:
                for char in content:
                    id = self.calculate_string_id(char, self.charset)
                    file.write(f"{id} ")
                file.write("\n")
            self.show_popup("Success", f"Encoded content saved to {output_file}")
        else:
            self.show_popup("Error", "Please provide input and output file names.")

    def decode_file(self, instance):
        input_file = self.input_file.text
        output_file = self.output_file.text
        if input_file and output_file:
            content = self.read_file(input_file)
            if not content:
                self.show_popup("Error", "Input file not found.")
                return

            ids = content.split()
            with open(output_file, 'w', encoding='utf-8') as file:
                for id_str in ids:
                    try:
                        id = int(id_str)
                        decoded_string = self.decode_id(id, self.charset)
                        file.write(decoded_string)
                    except ValueError:
                        self.show_popup("Error", f"Invalid ID '{id_str}' in {input_file}")
            self.show_popup("Success", f"Decoded content saved to {output_file}")
        else:
            self.show_popup("Error", "Please provide input and output file names.")

    def generate_combinations_action(self, instance):
        try:
            n = int(self.n_input.text)
            output_file = self.output_file_input.text
            use_multithreading = self.multithreading_spinner.text == 'Yes'

            if not output_file:
                self.show_popup("Error", "Please provide an output file name.")
                return

            generate_combinations(self.charset, n, output_file, use_multithreading)
            self.show_popup("Success", f"Combinations saved to {output_file}")
            self.popup.dismiss()
        except ValueError as e:
            self.show_popup("Error", f"Error: {e}")

    def calculate_string_id_action(self, instance):
        custom_string = self.custom_string_input.text
        if custom_string:
            try:
                string_id = calculate_string_id(custom_string, self.charset)
                self.show_popup("String ID", f"The ID for the string is: {string_id}")

                if self.save_checkbox.active:
                    filename = f"{len(custom_string)}.txt"
                    append_to_file(filename, f"{string_id}\t{custom_string}")

            except ValueError as e:
                self.show_popup("Error", f"Error: {e}")
        else:
            self.show_popup("Error", "Please provide a custom string.")

    def read_file(self, filename):
        if not os.path.exists(filename):
            return ""
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def calculate_string_id(self, input_string, charset):
        char_map = {c: i for i, c in enumerate(charset)}
        id = 0
        k = len(charset)
        for c in input_string:
            id = id * k + char_map[c]
        return id

    def decode_id(self, id, charset):
        k = len(charset)
        chars = []
        while id > 0:
            chars.append(charset[id % k])
            id //= k
        return ''.join(reversed(chars)) if chars else charset[0]

if __name__ == '__main__':
    CharsetApp().run()

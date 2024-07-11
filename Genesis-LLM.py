import os
import math
import json

# Function to load custom charset from configuration file
def load_custom_charset(config_file):
    custom_charset = []
    if not os.path.exists(config_file):
        print(f"Error opening configuration file: {config_file}")
        return custom_charset
    with open(config_file, 'r') as file:
        custom_charset = list(file.read())
    return custom_charset

# Function to save custom charset to configuration file
def save_custom_charset(custom_charset, config_file):
    with open(config_file, 'w') as file:
        file.write(''.join(custom_charset))

# Function to generate combinations and write to individual files
def generate_combinations(charset, n):
    k = len(charset) - 1
    nbr_comb = int(math.pow(k + 1, n))
    id = 0

    for row in range(nbr_comb):
        id += 1
        filename = f"{n}.txt"
        with open(filename, 'a') as file:
            file.write(f"{id}\t")
            for col in range(n - 1, -1, -1):
                rdiv = int(math.pow(k + 1, col))
                cell = (row // rdiv) % (k + 1)
                file.write(charset[cell])
            file.write("\n")

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
    return ''.join(reversed(chars))

def main():
    # Define the default character set
    default_charset = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        ' ', '\n', '\t', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', 
        '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', 
        '$', '#', '%'
    ]

    charset = default_charset
    config_file = "charset_config.txt"

    # Check if custom charset config file exists and load it
    if os.path.exists(config_file):
        charset = load_custom_charset(config_file)

    # User input mode selection
    mode = int(input("Select mode: (1) Generate combinations, (2) Enter custom string, (3) Decode ID to string: "))

    if mode == 1:
        array_size = int(input("Enter the size of your array: "))

        use_custom_array = int(input("Do you want to create a custom array? (1 for Yes, 0 for No): "))

        if use_custom_array == 1:
            charset = []
            print(f"\nEnter the {array_size} characters of your array:")
            for i in range(array_size):
                c = input()
                charset.append(c)
            save_custom_charset(charset, config_file)

        n = int(input("\nEnter the number of cells (n): "))
        print(f"\nNumber of FILE Cells = {n}")

        generate_combinations(charset, n)
    elif mode == 2:
        print("Enter your string (type 'EOF' on a new line to end input):")
        input_string = ""
        while True:
            line = input()
            if line == "EOF":
                break
            input_string += line + "\n"

        if input_string.endswith("\n"):
            input_string = input_string[:-1]

        id = calculate_string_id(input_string, charset)
        string_length = len(input_string)

        filename = f"{string_length}.txt"
        with open(filename, 'a') as file:
            file.write(f"{id}\t{input_string}\n")

        print(f"String ID: {id}")
        print(f"String length: {string_length}")
    elif mode == 3:
        id_to_decode = int(input("Enter the ID to decode: "))
        decoded_string = decode_id(id_to_decode, charset)
        print(f"Decoded string: {decoded_string}")
    else:
        print("Invalid mode selected!")

if __name__ == "__main__":
    main()

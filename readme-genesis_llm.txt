
# Python Script for Charset Management and Combination Generation

## Overview

This Python script provides functionalities to manage a custom character set, generate combinations of characters, and calculate unique IDs for text strings. The script includes the following main features:

1. Load and save a custom character set from/to a configuration file.
2. Generate all possible combinations of characters from a given character set and save them to files.
3. Calculate a unique ID for a given input string based on the character set.

## Applications and Capabilities

### Custom Charset Management

- **Load Custom Charset**: The script can load a custom character set from a configuration file (`charset_config.txt`). If the file exists, the script reads the characters from the file and uses them as the character set.
- **Save Custom Charset**: Users can save a custom character set to the configuration file for future use. This allows for consistent usage of the same character set across multiple runs of the script.

### Combination Generation

- **Generate Combinations**: The script can generate all possible combinations of characters from the character set for a specified length (`n`). Each combination is written to a file named `n.txt`, where `n` is the length of the combinations. Each line in the file contains a unique combination and its corresponding ID.

### String ID Calculation

- **Calculate String ID**: The script can calculate a unique numerical ID for any given input string. This ID is derived based on the position of each character in the custom or default character set. This feature can be useful for applications requiring unique identifiers for text strings, such as database indexing, content addressing, and cryptographic applications.

## Script Usage

1. **Load Default or Custom Charset**: By default, the script uses a predefined character set containing common programming symbols. If a `charset_config.txt` file exists, the script will load the custom character set from this file.

2. **Mode Selection**:
    - **Mode 1 (Generate Combinations)**:
        - The user is prompted to enter the size of the character array and whether to use a custom array.
        - If a custom array is used, the user inputs the characters, which are then saved to the configuration file.
        - The user specifies the number of cells (`n`) for the combinations.
        - The script generates all possible combinations of length `n` and writes them to a file.

    - **Mode 2 (Enter Custom String)**:
        - The user inputs a custom string (terminated by entering `EOF` on a new line).
        - The script calculates the unique ID for the input string and writes the string along with its ID to a file named with the length of the string.

3. **Output**:
    - Combination files are named based on the length of the combinations (e.g., `n.txt`).
    - Custom string ID and the string are written to a file named based on the length of the string.

## Example Usage

### Generating Combinations
```
Select mode: (1) Generate combinations, (2) Enter custom string: 1
Enter the size of your array: 5
Do you want to create a custom array? (1 for Yes, 0 for No): 1

Enter the 5 characters of your array:
a
b
c
d
e

Enter the number of cells (n): 3
Number of FILE Cells = 3
```

### Calculating String ID
```
Select mode: (1) Generate combinations, (2) Enter custom string: 2
Enter your string (type 'EOF' on a new line to end input):
Hello
EOF

String ID: 12345678
String length: 5
```

## Requirements

- Python 3.12 or later
- Standard Python libraries: `os`, `math`, `json`

## Execution

Run the script using the following command:
```
python script_name.py
```

Make sure to replace `script_name.py` with the actual name of your Python script file.

## Conclusion

This script provides a versatile tool for charset management, combination generation, and string ID calculation. It can be used in various applications including data processing, cryptography, and content management.

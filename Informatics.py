import tkinter as tk
from tkinter import Canvas, Tk
from PIL import Image, ImageDraw, ImageFont
import time
import sys
import os
import io
import colorsys
import unicodedata
import imageio

# Constants
CHAR_LIST = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    ' ', '\n', '\t', '\\', '\'', ',', '/', '<', '>', '?', ':', ';', '@', '#', '~', ']', '[', '{', '}', '`', '¬', '|', '¦', '!', '"', 
    '£', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

def get_input(prompt):
    return input(prompt)

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def write_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def append_to_file(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data)

def normalize_text(text):
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return normalized_text

def rgb_to_hsv(r, g, b):
    """Convert RGB values to HSV."""
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

def load_mapping(filename):
    with open(filename, "r", encoding="utf-8") as file:
        mapping = file.readlines()
    mapping = [line.strip() for line in mapping]
    if len(mapping) != 256:
        raise ValueError("Mapping file must contain exactly 256 lines.")
    return mapping

def create_gif(sequence, img_width, img_height, block_size, gif_filename, fps=24):
    cols, rows = img_width // block_size, img_height // block_size
    grid_size = cols * rows

    # Colors for the active squares
    colors = [(255, 215, 0), (128, 0, 128), (255, 0, 0), (0, 128, 0)]  # Gold, Purple, Red, Green

    # Initialize the grid with white squares
    grid = [(255, 255, 255)] * grid_size

    # Open a GIF writer
    with imageio.get_writer(gif_filename, mode='I', duration=1/fps) as writer:
        # Create frames based on the sequence
        for frame_num in range(0, len(sequence), 100):
            # Dictionary to count occurrences
            occurrences = {}
            
            # Set colors for up to 500 active squares in this frame
            for i in range(500):
                if frame_num + i < len(sequence):
                    idx = sequence[frame_num + i]
                    if 0 <= idx < grid_size:
                        occurrences[idx] = occurrences.get(idx, 0) + 1
                        grid[idx] = colors[i % 4]  # Cycle through the 4 colors

            # Create an image for the current frame
            image = Image.new('RGB', (img_width, img_height), (255, 255, 255))
            draw = ImageDraw.Draw(image)

            # Load a font
            font = ImageFont.load_default()

            for j in range(grid_size):
                x = (j % cols) * block_size
                y = (j // cols) * block_size
                draw.rectangle([x, y, x + block_size, y + block_size], fill=grid[j], outline=(0, 0, 0))

                # Draw the occurrence count if it exists and is greater than 1
                if j in occurrences and occurrences[j] > 1:
                    count = str(occurrences[j])
                    bbox = draw.textbbox((0, 0), count, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    text_x = x + (block_size - text_width) / 2
                    text_y = y + (block_size - text_height) / 2
                    draw.text((text_x, text_y), count, fill=(0, 0, 0), font=font)

            writer.append_data(imageio.core.util.asarray(image))

            # Reset the squares to white for the next frame
            for i in range(500):
                if frame_num + i < len(sequence):
                    idx = sequence[frame_num + i]
                    if 0 <= idx < grid_size:
                        grid[idx] = (255, 255, 255)

def process_statement():
    statement_file = get_input("Input 'statement_id.txt': ")

    statement = read_file(statement_file)
    statement = normalize_text(statement)

    # Save the normalized text back to the file
    write_to_file(statement_file, statement)

    print(f"Normalized text saved to {statement_file}")

def create_sequence():
    statement_file = get_input("Input 'statement_id.txt': ")
    sequence_file = get_input("Input 'sequence_id.txt': ")

    # Ensure sequence file is cleared
    write_to_file(sequence_file, "")

    statement = read_file(statement_file)

    statement_list = list(statement)

    character_count = int(get_input("Number of Characters in your Language:"))

    # Create sequence file content
    sequence = []
    for char in statement_list:
        try:
            index = CHAR_LIST.index(char) + 1
            sequence.append(index)
            append_to_file(sequence_file, f"{index} ")
        except ValueError:
            print(f"Character '{char}' not in CHAR_LIST. Skipping this character.")
            continue

    print(f"Sequence saved to {sequence_file}")

def generate_gif():
    sequence_file = get_input("Input 'sequence_id.txt': ")
    image_id = get_input("Input Image 'id': ")

    sequence = read_file(sequence_file).strip().split()
    sequence = [int(x) - 1 for x in sequence]  # Convert to 0-based index

    block_size = int(get_input("Enter side length of image block:  "))
    img_width = int(get_input("Enter width of image: "))
    img_height = int(get_input("Enter height of image: "))

    gif_filename = f'M{image_id}.gif'
    create_gif(sequence, img_width, img_height, block_size, gif_filename)
    print(f"GIF created and saved as {gif_filename}")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Normalize Text in Statement File")
        print("2. Create Sequence from Statement File")
        print("3. Generate GIF from Sequence File")
        print("4. Exit")

        choice = get_input("Choose an option: ")

        if choice == '1':
            process_statement()
        elif choice == '2':
            create_sequence()
        elif choice == '3':
            generate_gif()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main_menu()

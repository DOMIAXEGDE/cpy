#!/usr/bin/env python3

import random
import string
import json
import os
import sys
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

print("A BertoTools Product\n\n")

def create_empty_grid(size):
    """Creates a 2D list representing an empty grid of the given size."""
    return [[' ' for _ in range(size)] for _ in range(size)]

def get_direction_offsets(direction):
    """
    Returns the row and column offsets for a given direction.
    (dr, dc)
    """
    if direction == 'H-R': return (0, 1)
    if direction == 'H-L': return (0, -1)
    if direction == 'V-D': return (1, 0)
    if direction == 'V-U': return (-1, 0)
    if direction == 'D-R': return (1, 1)
    if direction == 'D-L': return (1, -1)
    if direction == 'U-R': return (-1, 1)
    if direction == 'U-L': return (-1, -1)
    return (0, 0)

def can_place_word(grid, word, row, col, direction):
    """
    Checks if a word can be placed at a specific position and direction
    without conflicting with existing letters.
    """
    word_len = len(word)
    grid_size = len(grid)
    dr, dc = get_direction_offsets(direction)
    
    # Check for out-of-bounds at the start and end of the word
    if not (0 <= row < grid_size and 0 <= col < grid_size): return False
    end_row, end_col = row + dr * (word_len - 1), col + dc * (word_len - 1)
    if not (0 <= end_row < grid_size and 0 <= end_col < grid_size): return False

    # Check for conflicts with existing letters, ensuring case consistency
    for i in range(word_len):
        current_row, current_col = row + dr * i, col + dc * i
        if grid[current_row][current_col] not in (' ', word[i]):
            return False
    return True

def place_word(grid, word, row, col, direction):
    """Places a word on the grid and returns the coordinates of its letters."""
    # Note: Word is already uppercase when this function is called
    positions = []
    dr, dc = get_direction_offsets(direction)
    for i, char in enumerate(word):
        current_row, current_col = row + dr * i, col + dc * i
        grid[current_row][current_col] = char
        positions.append((current_row, current_col))
    return positions

def find_best_fit(grid, word):
    """
    Finds the best position to place a word on the grid, prioritizing
    positions with letter overlaps. Returns the best fit and its overlap score.
    """
    best_fit = None
    directions = ['H-R', 'H-L', 'V-D', 'V-U', 'D-R', 'D-L', 'U-R', 'U-L']
    size = len(grid)
    max_overlap = -1

    for _ in range(500):
        direction = random.choice(directions)
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        # Convert word to uppercase before checking for placement
        word_upper = word.upper()
        if can_place_word(grid, word_upper, row, col, direction):
            overlap = 0
            dr, dc = get_direction_offsets(direction)
            for i, char in enumerate(word_upper):
                current_row, current_col = row + dr * i, col + dc * i
                if grid[current_row][current_col] == char:
                    overlap += 1
            
            if overlap > max_overlap:
                max_overlap = overlap
                best_fit = (row, col, direction)

    if best_fit:
        return best_fit, max_overlap
    return None, None

def word_search(words):
    """
    Generates a word search grid for a list of words using a random-based,
    intersection-prioritizing placement strategy.
    """
    words_upper = [word.upper() for word in words]
    initial_size = max((len(word) for word in words_upper), default=0) + 5
    
    while True:
        grid = create_empty_grid(initial_size)
        word_positions = {}
        all_placed = True
        
        # Sort words by length in descending order to place longer words first
        sorted_words_upper = sorted(words_upper, key=len, reverse=True)
        
        for word in sorted_words_upper:
            best_fit, overlap_score = find_best_fit(grid, word)
            if best_fit:
                row, col, direction = best_fit
                positions = place_word(grid, word, row, col, direction)
                word_positions[word] = positions
            else:
                all_placed = False
                break
        
        if all_placed:
            print(f"Final grid size: {initial_size}, Total Overlap Score: {sum(1 for w in word_positions if word_positions[w]) - len(words_upper) + sum(len(p) for p in word_positions.values())}")
            fill_grid(grid)
            return grid, word_positions
        else:
            print(f"Could not place all words in a grid of size {initial_size}. Increasing size.")
            initial_size += 1

def fill_grid(grid):
    """Fills the empty spaces of the grid with random uppercase letters."""
    letters = string.ascii_uppercase
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(letters)

def draw_footer(c, width, height):
    """Draws a footer with a copyright notice on the PDF page."""
    footer_text = "© 2024 bertotools.com"
    c.setFont("Helvetica", 8)
    c.setFillColor("black")
    c.drawRightString(width - 10, 10, footer_text)

def save_grid_to_pdf(grid, words, title, subtitle, filename):
    """Generates a PDF for a single word search puzzle."""
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5
    margin = 25
    
    # Draw title and subtitle
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2.0, height - 30, title)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2.0, height - 45, subtitle)
    
    # Calculate positions for centering the grid and the word list
    cell_size = min(width - 2 * margin, height - 2 * margin) // (len(grid) + 2)
    grid_width = len(grid) * cell_size
    grid_start_x = (width - grid_width) / 2
    grid_start_y = height - 80
    
    # Draw grid
    c.setFont("Helvetica", 10)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            letter_text = grid[row][col]
            
            # Calculate the center position for the cell
            cell_center_x = grid_start_x + col * cell_size + (cell_size / 2)
            cell_center_y = grid_start_y - row * cell_size - (cell_size / 2)
            
            # Draw the letter centered in the cell
            c.drawCentredString(cell_center_x, cell_center_y - 3, letter_text) # -3 offset to center vertically
            

    # Draw word list beneath the grid
    c.setFont("Helvetica", 10)
    text_x_position = grid_start_x
    text_y_position = grid_start_y - len(grid) * cell_size - 20
    column_width = 80
    words_per_column = 5

    for i, word in enumerate(words):
        if i % words_per_column == 0 and i != 0:
            text_x_position += column_width
            text_y_position = grid_start_y - len(grid) * cell_size - 20

        c.drawString(text_x_position, text_y_position, word.upper())
        text_y_position -= 12

    # Draw footer
    draw_footer(c, width, height)
    c.save()

def merge_pdfs(pdf_files, output):
    """Merges a list of PDF files into a single output PDF."""
    pdf_merger = PdfMerger()
    for pdf in pdf_files:
        try:
            pdf_merger.append(pdf)
        except Exception as e:
            print(f"Error merging file {pdf}: {e}")
            continue
    pdf_merger.write(output)
    pdf_merger.close()

def create_solutions_document(config_data):
    """Generates PDF documents containing the solutions for the word searches."""
    h_space = 18
    v_space = 18

    colors = [
        "red", "blue", "green", "orange", "purple", "brown", "pink", "cyan", 
        "magenta", "gray", "black", "violet", "indigo", "lime", "gold", 
        "silver", "navy", "coral", "teal", "salmon"
    ]

    for i in range(0, len(config_data), 4):
        c = canvas.Canvas(f"solution_{i//4 + 1}.pdf", pagesize=A5)
        width, height = A5
        margin = 25

        max_grid_size = max(len(config_data[j][3]) for j in range(i, min(i + 4, len(config_data))))
        max_cell_size = min((width - 2 * margin - h_space) // (2 * max_grid_size), (height - 2 * margin - v_space) // (2 * max_grid_size))
        
        for j, (title, _, word_positions, grid) in enumerate(config_data[i:i+4]):
            quadrant = j % 4
            grid_size = len(grid)
            grid_width = grid_size * max_cell_size
            grid_height = grid_size * max_cell_size
            
            if quadrant == 0: # Top-left
                start_x = margin + (width / 4 - grid_width / 2) - h_space / 2
                start_y = height - margin - (height / 4 - grid_height / 2)
            elif quadrant == 1: # Top-right
                start_x = width - margin - (width / 4 + grid_width / 2) + h_space / 2
                start_y = height - margin - (height / 4 - grid_height / 2)
            elif quadrant == 2: # Bottom-left
                start_x = margin + (width / 4 - grid_width / 2) - h_space / 2
                start_y = margin + (height / 4 + grid_height / 2)
            elif quadrant == 3: # Bottom-right
                start_x = width - margin - (width / 4 + grid_width / 2) + h_space / 2
                start_y = margin + (height / 4 + grid_height / 2)

            c.setFont("Helvetica-Bold", 7)
            c.setFillColor("black")
            c.drawCentredString(start_x + grid_width / 2, start_y, title)

            c.setFont("Helvetica", 5)
            word_colors = {word: colors[idx % len(colors)] for idx, word in enumerate(word_positions.keys())}
            for word, positions in word_colors.items():
                c.setFillColor(word_colors[word])
                for (row, col) in word_positions[word]:
                    letter_text = grid[row][col]
                    cell_center_x = start_x + col * max_cell_size + (max_cell_size / 2)
                    cell_center_y = start_y - row * max_cell_size - (max_cell_size / 2)
                    c.drawCentredString(cell_center_x, cell_center_y - 2, letter_text) # -2 offset for vertical centering
        
        draw_footer(c, width, height)
        c.save()


if __name__ == "__main__":
    try:
        with open("titles.txt") as titles_file:
            titles = [line.strip() for line in titles_file.readlines()]
    except FileNotFoundError:
        print("Error: 'titles.txt' not found.")
        sys.exit(1)
        
    try:
        with open("subtitles.txt") as subtitles_file:
            subtitles = [line.strip() for line in subtitles_file.readlines()]
    except FileNotFoundError:
        print("Error: 'subtitles.txt' not found.")
        sys.exit(1)

    try:
        with open("word-list.txt") as words_file:
            all_words = []
            current_words = []
            for line in words_file.readlines():
                line = line.strip()
                if line == '...':
                    all_words.append(current_words)
                    current_words = []
                else:
                    current_words.append(line)
            if current_words:
                all_words.append(current_words)
    except FileNotFoundError:
        print("Error: 'word-list.txt' not found.")
        sys.exit(1)


    try:
        assert len(titles) == len(all_words), "The number of titles must match the number of word lists"
        assert len(titles) == len(subtitles), "The number of titles must match the number of subtitles"
    except AssertionError as e:
        print(f"Error: {e}")
        sys.exit(1)


    pdf_files = []
    config_data = []
    for i, (title, subtitle, words) in enumerate(zip(titles, subtitles, all_words)):
        filename = f"word_search_{i + 1}.pdf"
        grid, word_positions = word_search(words)
        
        save_grid_to_pdf(grid, words, title, subtitle, filename)
        
        config_data.append((title, f"solution_{i + 1}.pdf", word_positions, grid))
        
        print(f"Word search saved as {filename}")

    with open('config.txt', 'w') as config_file:
        json.dump(config_data, config_file)

    pdf_files = [f"word_search_{i + 1}.pdf" for i in range(len(titles))]
    merge_pdfs(pdf_files, "output.pdf")
    create_solutions_document(config_data)
    
    solution_pdfs = [f"solution_{i//4 + 1}.pdf" for i in range(0, len(config_data), 4)]
    merge_pdfs(["output.pdf"] + solution_pdfs, "puzzle.pdf")
    print("All word searches and solutions have been merged into puzzle.pdf")


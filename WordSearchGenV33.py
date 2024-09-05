import random
import string
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger
import json
import os

print("A BertoTools Product\n\n")

def create_empty_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def can_place_word(grid, word, row, col, direction):
    for i, char in enumerate(word):
        if direction == 'H' and (col + i >= len(grid) or grid[row][col + i] not in (' ', char)):
            return False
        elif direction == 'V' and (row + i >= len(grid) or grid[row + i][col] not in (' ', char)):
            return False
        elif direction == 'D' and (row + i >= len(grid) or col + i >= len(grid) or grid[row + i][col + i] not in (' ', char)):
            return False
        elif direction == 'U' and (row - i < 0 or col + i >= len(grid) or grid[row - i][col + i] not in (' ', char)):
            return False
    return True

def place_word(grid, word, row, col, direction):
    word = word.upper()  # Ensure the word is in uppercase
    positions = []
    for i, char in enumerate(word):
        if direction == 'H':
            grid[row][col + i] = char
            positions.append((row, col + i))
        elif direction == 'V':
            grid[row + i][col] = char
            positions.append((row + i, col))
        elif direction == 'D':
            grid[row + i][col + i] = char
            positions.append((row + i, col + i))
        elif direction == 'U':
            grid[row - i][col + i] = char
            positions.append((row - i, col + i))
    return positions

def find_best_fit(grid, word):
    best_fit = None
    directions = ['H', 'V', 'D', 'U']
    size = len(grid)
    max_overlap = -1

    for _ in range(100):  # Attempt 100 random placements
        direction = random.choice(directions)
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if can_place_word(grid, word, row, col, direction):
            overlap = sum(1 for i, char in enumerate(word) if (direction == 'H' and grid[row][col + i] == char) or 
                          (direction == 'V' and grid[row + i][col] == char) or 
                          (direction == 'D' and grid[row + i][col + i] == char) or 
                          (direction == 'U' and grid[row - i][col + i] == char))
            if overlap > max_overlap:
                max_overlap = overlap
                best_fit = (row, col, direction)

    return best_fit

def word_search(words):
    size = max(len(word) for word in words) + 5
    while True:
        grid = create_empty_grid(size)
        all_placed = True
        word_positions = {}
        for word in words:
            best_fit = find_best_fit(grid, word)
            if best_fit:
                row, col, direction = best_fit
                positions = place_word(grid, word, row, col, direction)
                word_positions[word] = positions
            else:
                all_placed = False
                break
        if all_placed:
            break
        size += 1  # Increase grid size if not all words can be placed
    fill_grid(grid)
    return grid, word_positions

def fill_grid(grid):
    letters = string.ascii_uppercase  # Use uppercase letters
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(letters)

def draw_footer(c, width, height):
    footer_text = "© 2024 bertotools.com"
    c.setFont("Helvetica", 8)
    c.setFillColor("black")
    c.drawRightString(width - 10, 10, footer_text)

def save_grid_to_pdf(grid, words, title, subtitle, filename):
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5
    margin = 25  # Define the margin
    cell_size = min(width - 2 * margin, height - 2 * margin) // (len(grid) + 2)
    
    # Draw title and subtitle
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2.0, height - 30, title)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2.0, height - 45, subtitle)
    
    # Calculate positions for centering the grid and the word list
    grid_width = len(grid) * cell_size
    grid_start_x = (width - grid_width) / 2
    grid_start_y = height - 80
    
    # Draw grid
    c.setFont("Helvetica", 10)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            c.drawString(grid_start_x + col * cell_size + 2, grid_start_y - row * cell_size - 12, grid[row][col])

    # Draw word list beneath the grid
    c.setFont("Helvetica", 10)
    text_x_position = grid_start_x
    text_y_position = grid_start_y - len(grid) * cell_size - 20
    column_width = 80  # Width for each column
    words_per_column = 5  # Maximum of 5 words per column

    for i, word in enumerate(words):
        if i % words_per_column == 0 and i != 0:
            text_x_position += column_width
            text_y_position = grid_start_y - len(grid) * cell_size - 20

        c.drawString(text_x_position, text_y_position, word)
        text_y_position -= 12

    # Draw footer
    draw_footer(c, width, height)

    c.save()

def merge_pdfs(pdf_files, output):
    pdf_merger = PdfMerger()
    for pdf in pdf_files:
        pdf_merger.append(pdf)
    pdf_merger.write(output)
    pdf_merger.close()

def create_solutions_document(config_data):
    h_space = 18
    v_space = 18

    # List of distinguishable colors
    colors = [
        "red", "blue", "green", "orange", "purple", "brown", "pink", "cyan", 
        "magenta", "red", "gray", "black", "violet", "indigo", "lime", "gold", 
        "silver", "navy", "coral", "teal"
    ]

    for i in range(0, len(config_data), 4):
        c = canvas.Canvas(f"solution_{i//4 + 1}.pdf", pagesize=A5)
        width, height = A5
        margin = 25  # Increase margin size

        # Determine the largest grid size among the four puzzles on the page
        max_grid_size = max(len(config_data[j][3]) for j in range(i, min(i + 4, len(config_data))))
        max_cell_size = min((width - 2 * margin - h_space) // (2 * max_grid_size), (height - 2 * margin - v_space) // (2 * max_grid_size))
        
        for j, (title, _, word_positions, grid) in enumerate(config_data[i:i+4]):
            quadrant = j % 4
            grid_size = len(grid)
            grid_width = grid_size * max_cell_size
            grid_height = grid_size * max_cell_size
            
            if quadrant == 0:
                start_x = margin + (width / 4 - grid_width / 2) - h_space / 2
                start_y = height - margin - (height / 4 - grid_height / 2)
            elif quadrant == 1:
                start_x = width - margin - (width / 4 + grid_width / 2) + h_space / 2
                start_y = height - margin - (height / 4 - grid_height / 2)
            elif quadrant == 2:
                start_x = margin + (width / 4 - grid_width / 2) - h_space / 2
                start_y = margin + (height / 4 + grid_height / 2)
            elif quadrant == 3:
                start_x = width - margin - (width / 4 + grid_width / 2) + h_space / 2
                start_y = margin + (height / 4 + grid_height / 2)

            # Draw title
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor("black")
            c.drawCentredString(start_x + grid_width / 2, start_y, title)

            # Draw grid
            c.setFont("Helvetica", 5)
            word_colors = {word: colors[i % len(colors)] for i, word in enumerate(word_positions.keys())}
            for word, positions in word_positions.items():
                c.setFillColor(word_colors[word])
                for (row, col) in positions:
                    c.drawString(start_x + col * max_cell_size + 2, start_y - row * max_cell_size - 12, grid[row][col])

            # Draw footer on each page
            draw_footer(c, width, height)

        c.save()

if __name__ == "__main__":
    with open("titles.txt") as titles_file:
        titles = [line.strip() for line in titles_file.readlines()]

    with open("subtitles.txt") as subtitles_file:
        subtitles = [line.strip() for line in subtitles_file.readlines()]

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

    assert len(titles) == len(all_words), "The number of titles must match the number of word lists"
    assert len(titles) == len(subtitles), "The number of titles must match the number of subtitles"

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

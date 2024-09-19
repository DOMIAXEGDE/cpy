import random
from collections import defaultdict
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from PyPDF2 import PdfMerger
import os

print("A BertoTools Product - Crossword Generator\n\n")

def create_empty_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def get_word_positions(grid, word, row, col, direction):
    positions = []
    if direction == 'H':
        for i, letter in enumerate(word):
            positions.append((row, col + i))
    elif direction == 'V':
        for i, letter in enumerate(word):
            positions.append((row + i, col))
    return positions

def can_place_word_at(grid, word, row, col, direction):
    positions = get_word_positions(grid, word, row, col, direction)
    for idx, (r, c) in enumerate(positions):
        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
            return False
        cell = grid[r][c]
        if cell == ' ' or cell == word[idx]:
            continue
        else:
            return False
    return True

def find_intersections(word, grid, placed_words):
    intersections = []
    for placed_word, (positions, _) in placed_words.items():
        for idx_p, (r_p, c_p) in enumerate(positions):
            for idx_w, letter in enumerate(word):
                if placed_word[idx_p] == letter:
                    # Try horizontal and vertical positions
                    possible_positions = []
                    # Horizontal
                    row = r_p - idx_w
                    col = c_p
                    direction = 'V'
                    if can_place_word_at(grid, word, row, col, direction):
                        possible_positions.append((row, col, direction))
                    # Vertical
                    row = r_p
                    col = c_p - idx_w
                    direction = 'H'
                    if can_place_word_at(grid, word, row, col, direction):
                        possible_positions.append((row, col, direction))
                    intersections.extend(possible_positions)
    return intersections

def place_word(grid, word, row, col, direction):
    positions = get_word_positions(grid, word, row, col, direction)
    for idx, (r, c) in enumerate(positions):
        grid[r][c] = word[idx]
    return positions

def remove_word(grid, positions):
    for r, c in positions:
        grid[r][c] = ' '

def generate_crossword(words):
    size = max(len(word) for word in words) * 2  # Increase grid size for more space
    grid = create_empty_grid(size)
    placed_words = {}

    def place_words(index):
        if index == len(words):
            return True
        word = words[index]
        possible_positions = []
        if not placed_words:
            # Place the first word in the center
            row = size // 2
            col = (size - len(word)) // 2
            directions = ['H', 'V']
            for direction in directions:
                if can_place_word_at(grid, word, row, col, direction):
                    possible_positions.append((row, col, direction))
        else:
            # Find intersections with already placed words
            intersections = find_intersections(word, grid, placed_words)
            possible_positions.extend(intersections)

        random.shuffle(possible_positions)
        for row, col, direction in possible_positions:
            if can_place_word_at(grid, word, row, col, direction):
                positions = place_word(grid, word, row, col, direction)
                placed_words[word] = (positions, direction)
                if place_words(index + 1):
                    return True
                # Backtrack
                remove_word(grid, positions)
                del placed_words[word]
        return False

    words = sorted(words, key=lambda w: -len(w))  # Start with longest words
    success = place_words(0)
    if not success:
        print("Failed to generate crossword with the given words.")
    return grid, placed_words

def trim_grid(grid):
    rows = [i for i, row in enumerate(grid) if any(cell != ' ' for cell in row)]
    cols = [i for i, col in enumerate(zip(*grid)) if any(cell != ' ' for cell in col)]
    if rows and cols:
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        trimmed_grid = [row[min_col:max_col+1] for row in grid[min_row:max_row+1]]
        return trimmed_grid, min_row, min_col
    else:
        return grid, 0, 0

def save_crossword_to_pdf(grid, word_positions, clues_dict, title, filename):
    """Save the crossword puzzle to a PDF."""
    grid, offset_row, offset_col = trim_grid(grid)
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5
    margin = 25

    # Estimate available space for grid and clues
    grid_area_height = height * 0.6
    clues_area_height = height - grid_area_height - margin * 2

    # Adjust cell size based on grid dimensions
    max_grid_width = width - 2 * margin
    max_grid_height = grid_area_height - margin
    cell_size = min(max_grid_width / len(grid[0]), max_grid_height / len(grid))

    # Draw title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, height - margin, title)

    # Draw the grid
    grid_start_x = (width - cell_size * len(grid[0])) / 2
    grid_start_y = height - margin - 20  # Adjust as needed

    c.setFont("Helvetica", 8)
    clue_number = 1
    clue_numbers = {}  # Map cell positions to clue numbers

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            x = grid_start_x + col * cell_size
            y = grid_start_y - row * cell_size
            cell = grid[row][col]
            if cell == ' ':
                # Draw black cell
                c.setFillColorRGB(0, 0, 0)
                c.rect(x, y - cell_size, cell_size, cell_size, stroke=1, fill=1)
                c.setFillColorRGB(0, 0, 0)  # Reset color
            else:
                # Draw empty cell
                c.rect(x, y - cell_size, cell_size, cell_size, stroke=1, fill=0)
                # Check if this cell is the start of a word
                is_start = False
                for word, (positions, direction) in word_positions.items():
                    pos_row, pos_col = positions[0]
                    pos_row -= offset_row
                    pos_col -= offset_col
                    if pos_row == row and pos_col == col:
                        is_start = True
                        clue_numbers[(row, col)] = clue_number
                        # Draw clue number
                        c.drawString(x + 2, y - cell_size + 2, str(clue_number))
                        clue_number += 1
                        break

    # Prepare clues
    c.setFont("Helvetica", 10)
    text_x_position = margin
    text_y_position = grid_start_y - cell_size * len(grid) - 20  # Start below the grid
    clues_area_width = width - 2 * margin

    across_clues = []
    down_clues = []

    for word, (positions, direction) in word_positions.items():
        pos_row, pos_col = positions[0]
        pos_row -= offset_row
        pos_col -= offset_col
        number = clue_numbers.get((pos_row, pos_col), '')
        clue = clues_dict.get(word.lower(), 'No clue provided')
        clue_text = f"{number}. {clue}"
        if direction == 'H':
            across_clues.append(clue_text)
        else:
            down_clues.append(clue_text)

    # Draw clues dynamically to prevent overlap
    def draw_clues(clues_list, title_text, start_x, start_y, area_width, area_height):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(start_x, start_y, title_text)
        c.setFont("Helvetica", 10)
        y = start_y - 15
        line_height = 12
        col_width = area_width / 2  # Adjust number of columns if needed
        clues_per_column = int(area_height / line_height)
        num_columns = max(1, len(clues_list) // clues_per_column + 1)
        col_width = area_width / num_columns
        for col_index in range(num_columns):
            x = start_x + col_index * col_width
            y = start_y - 15
            for i in range(clues_per_column):
                clue_index = col_index * clues_per_column + i
                if clue_index >= len(clues_list):
                    break
                clue = clues_list[clue_index]
                wrapped_text = simpleSplit(clue, 'Helvetica', 10, col_width)
                for line in wrapped_text:
                    if y < margin:
                        # Not enough space
                        break
                    c.drawString(x, y, line)
                    y -= line_height
                y -= line_height / 2  # Extra space between clues

    # Calculate available space for clues
    clues_start_y = text_y_position
    clues_area_height = clues_start_y - margin

    # Draw Across clues
    draw_clues(across_clues, "Across", margin, clues_start_y, clues_area_width, clues_area_height / 2)

    # Draw Down clues
    draw_clues(down_clues, "Down", margin, clues_start_y - clues_area_height / 2, clues_area_width, clues_area_height / 2)

    # Save the PDF
    c.save()

def save_solution_to_pdf(grid, word_positions, clues_dict, title, filename):
    """Save the crossword solution to a PDF."""
    grid, offset_row, offset_col = trim_grid(grid)
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5
    margin = 25

    # Adjust cell size based on grid dimensions
    max_grid_width = width - 2 * margin
    max_grid_height = height - 2 * margin
    cell_size = min(max_grid_width / len(grid[0]), max_grid_height / len(grid))

    # Draw title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, height - margin, f"Solution: {title}")

    # Draw the grid
    grid_start_x = (width - cell_size * len(grid[0])) / 2
    grid_start_y = height - margin - 20  # Adjust as needed

    c.setFont("Helvetica", 8)
    clue_number = 1
    clue_numbers = {}

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            x = grid_start_x + col * cell_size
            y = grid_start_y - row * cell_size
            cell = grid[row][col]
            if cell == ' ':
                # Draw black cell
                c.setFillColorRGB(0, 0, 0)
                c.rect(x, y - cell_size, cell_size, cell_size, stroke=1, fill=1)
                c.setFillColorRGB(0, 0, 0)  # Reset color
            else:
                # Draw cell with letter
                c.rect(x, y - cell_size, cell_size, cell_size, stroke=1, fill=0)
                c.drawCentredString(x + cell_size / 2, y - cell_size + 5, cell)
                # Check if this cell is the start of a word
                is_start = False
                for word, (positions, direction) in word_positions.items():
                    pos_row, pos_col = positions[0]
                    pos_row -= offset_row
                    pos_col -= offset_col
                    if pos_row == row and pos_col == col:
                        is_start = True
                        clue_numbers[(row, col)] = clue_number
                        # Draw clue number
                        c.drawString(x + 2, y - cell_size + 2, str(clue_number))
                        clue_number += 1
                        break
    # Save the PDF
    c.save()

def merge_pdfs(puzzle_pdfs, solution_pdfs, output):
    """Merge puzzles and solutions into a single PDF, with solutions at the end."""
    pdf_merger = PdfMerger()
    # Append all puzzles first
    for pdf in puzzle_pdfs:
        pdf_merger.append(pdf)
    # Then append all solutions
    for pdf in solution_pdfs:
        pdf_merger.append(pdf)
    pdf_merger.write(output)
    pdf_merger.close()

if __name__ == "__main__":
    with open("crossword_titles.txt") as titles_file:
        titles = [line.strip() for line in titles_file.readlines() if line.strip()]

    with open("crossword_word_list.txt") as words_file:
        all_words = []
        current_words = []
        for line in words_file.readlines():
            line = line.strip()
            if line == '...':
                all_words.append(current_words)
                current_words = []
            elif line:
                current_words.append(line)
        if current_words:
            all_words.append(current_words)

    with open("clues.txt") as clues_file:
        all_clues = []
        current_clues = []
        for line in clues_file.readlines():
            line = line.strip()
            if line == '...':
                all_clues.append(current_clues)
                current_clues = []
            elif line:
                current_clues.append(line)
        if current_clues:
            all_clues.append(current_clues)

    assert len(titles) == len(all_words) == len(all_clues), "The number of titles, word lists, and clue lists must match"

    puzzle_pdfs = []
    solution_pdfs = []
    for i, (title, words, clues) in enumerate(zip(titles, all_words, all_clues)):
        if len(words) != len(clues):
            raise ValueError(f"The number of words and clues must match for puzzle '{title}'")

        # Create a dictionary mapping words to clues
        clues_dict = dict(zip([word.lower() for word in words], clues))

        filename = f"crossword_{i + 1}.pdf"
        grid, word_positions = generate_crossword(words)
        save_crossword_to_pdf(grid, word_positions, clues_dict, title, filename)

        solution_filename = f"solution_{i + 1}.pdf"
        save_solution_to_pdf(grid, word_positions, clues_dict, title, solution_filename)

        puzzle_pdfs.append(filename)
        solution_pdfs.append(solution_filename)

        print(f"Crossword puzzle saved as {filename} and solution saved as {solution_filename}")

    # Merge all puzzles and then all solutions into one PDF
    merge_pdfs(puzzle_pdfs, solution_pdfs, "crossword_puzzles.pdf")
    print("All crosswords and solutions have been merged into crossword_puzzles.pdf")

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import tempfile
import random
import itertools

def draw_board(n, pieces):
    """Draws an n x n board with pieces using matplotlib and returns the file path."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(n + 1))
    ax.grid(True)
    
    for piece, position in pieces.items():
        row, col = position
        ax.text(col + 0.5, n - row - 0.5, piece, 
                horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='black')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()

    # Save to a temporary file and return the file path
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(temp_file.name, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    return temp_file.name

def generate_possible_maneuvers(n, start_pos, can_jump):
    """Generate a dictionary of all possible maneuvers based on the board size and jumping rule."""
    maneuvers = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    x, y = start_pos
    
    for direction in directions:
        step = 1
        while True:
            new_x = x + direction[0] * step
            new_y = y + direction[1] * step

            # Check if the new position is within the board bounds
            if 0 <= new_x < n and 0 <= new_y < n:
                maneuvers.append((new_x, new_y))
                if not can_jump:
                    break  # If the piece cannot jump, it can only move one step in each direction
            else:
                break  # Stop if the move is out of bounds

            step += 1
    
    return maneuvers

def create_pdf(n, m, max_pieces, max_pages, game_name, player_names):
    """Generate a PDF document with all possible games up to max_pieces and max_pages."""
    pdf_filename = f"{game_name.replace(' ', '_').lower()}_game.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    current_page = 1
    configurations = []

    def add_game_to_pdf(pieces, maneuvers, current_page, configuration_id):
        # Title for each game
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2.0, height - 2 * cm, f"Game {current_page} (Config {configuration_id}): {game_name} ({n}x{n} Board)")

        # Game Description
        c.setFont("Helvetica", 12)
        text = f"Grid Size: {n}x{n}\nSub-Square Size: {m}x{m}\n"
        text += f"Player 1: {player_names[0]}\nPlayer 2: {player_names[1]}\n"
        c.drawString(2 * cm, height - 5 * cm, text)

        # Draw the board with matplotlib and insert it into the PDF
        board_image_path = draw_board(n, pieces)
        
        # Calculate optimal size for the board image within the PDF
        image_width = min(width - 4 * cm, 15 * cm)
        image_height = image_width
        x_offset = (width - image_width) / 2
        y_offset = height / 2 - image_height / 2
        
        c.drawImage(board_image_path, x_offset, y_offset, width=image_width, height=image_height)

        # Piece-specific Maneuvers
        c.setFont("Helvetica", 10)
        y_position = height / 2 - image_height / 2 - 2 * cm
        for piece, piece_maneuvers in maneuvers.items():
            maneuver_text = f"{piece}: Possible Moves: {piece_maneuvers['moves']}, Can Jump: {piece_maneuvers['can_jump']}"
            c.drawString(2 * cm, y_position, maneuver_text)
            y_position -= 1 * cm

        # Finalize page
        c.showPage()

    # Generate all possible games
    positions = [(i, j) for i in range(n) for j in range(n)]
    total_combinations = list(itertools.combinations(positions, max_pieces * 2))

    for idx, position_set in enumerate(total_combinations):
        if current_page > max_pages:
            break

        pieces = {}
        maneuvers = {}

        for i in range(max_pieces):
            pieces[f'P1_{i+1}'] = position_set[i]
            pieces[f'P2_{i+1}'] = position_set[i + max_pieces]

            can_jump_p1 = random.choice([True, False])
            can_jump_p2 = random.choice([True, False])

            maneuvers[f'P1_{i+1}'] = {
                'moves': generate_possible_maneuvers(n, position_set[i], can_jump_p1),
                'can_jump': can_jump_p1
            }
            maneuvers[f'P2_{i+1}'] = {
                'moves': generate_possible_maneuvers(n, position_set[i + max_pieces], can_jump_p2),
                'can_jump': can_jump_p2
            }

        # Track the configuration details
        configuration_id = idx + 1
        configurations.append({
            'id': configuration_id,
            'pieces': pieces,
            'maneuvers': maneuvers
        })

        # Add this game configuration to the PDF
        add_game_to_pdf(pieces, maneuvers, current_page, configuration_id)
        current_page += 1

    # Save the PDF
    c.save()

    print(f"PDF generated: {pdf_filename}")
    print(f"Total configurations generated: {len(configurations)}")

    # Optionally save configurations to a log file (if needed)
    with open(f"{game_name.replace(' ', '_').lower()}_configurations.txt", "w") as log_file:
        for config in configurations:
            log_file.write(f"Configuration ID: {config['id']}\n")
            log_file.write("Pieces:\n")
            for piece, position in config['pieces'].items():
                log_file.write(f"  {piece}: {position}\n")
            log_file.write("Maneuvers and Rules:\n")
            for piece, piece_maneuvers in config['maneuvers'].items():
                log_file.write(f"  {piece}: Possible Moves: {piece_maneuvers['moves']}, Can Jump: {piece_maneuvers['can_jump']}\n")
            log_file.write("\n")

if __name__ == "__main__":
    # User inputs
    game_name = input("Enter the name of the game: ")
    n = int(input("Enter the board size (n x n): "))
    m = int(input("Enter the sub-square size (m x m): "))
    max_pieces = int(input("Enter the maximum number of pieces per player: "))
    max_pages = int(input("Enter the maximum number of pages (up to 800): "))
    max_pages = min(max_pages, 800)  # Cap the maximum pages to 800
    player_names = [input("Enter Player 1's name: "), input("Enter Player 2's name: ")]

    # Create the PDF document with all possible games up to the specified limits
    create_pdf(n, m, max_pieces, max_pages, game_name, player_names)

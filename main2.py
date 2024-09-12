from raylibpy import *
import os
import threading

# Constants
GRID_ROWS = 5
GRID_COLS = 5
BUTTON_SIZE = 100
MAX_SCRIPTS = 25
MAX_TEXT_LENGTH = 512
MAX_GRIDS = 200
GAME_FILES_PATH = "gameFiles/"

# Modes and corresponding colors
MODES = ['Python', 'C', 'HTML', 'CSS', 'JavaScript', 'PHP', 'C++']
MODE_EXTENSIONS = ['py', 'c', 'html', 'css', 'js', 'php', 'cpp']
MODE_COLORS = [PURPLE, YELLOW, BLUE, GREEN, ORANGE, PINK, LIGHTGRAY]

# Script and ScriptGrid Classes
class Script:
    def __init__(self):
        self.text = ""
        self.isEditing = False
        self.filename = ""
        self.fileType = 0  # 0: Python, 1: C, 2: HTML, 3: CSS, 4: JavaScript, 5: PHP, 6: C++

class ScriptGrid:
    def __init__(self):
        self.scripts = [Script() for _ in range(MAX_SCRIPTS)]
        self.gridID = 0

# Global variables
grids = [ScriptGrid() for _ in range(MAX_GRIDS)]
currentGridIndex = 0
selectedScriptIndex = -1
currentModeIndex = 0  # Index for MODES
isEditingMode = True
showHelpMenu = False

# Function Definitions
def save_script_to_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)

def load_script_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

def does_file_exist(filename):
    return os.path.exists(filename)

def execute_command(command):
    os.system(command)

def run_command_async(command):
    thread = threading.Thread(target=execute_command, args=(command,))
    thread.start()

def open_script_in_notepad(filename):
    run_command_async(f"notepad {filename}")

def execute_python_script(filename):
    run_command_async(f"python {filename}")

def compile_and_execute_c_file(filename):
    output_file = f"output_{currentGridIndex}.exe"
    compile_command = f"gcc {filename} -o {output_file} 2> compile_errors.txt"
    run_command_async(compile_command)
    if does_file_exist("compile_errors.txt"):
        with open("compile_errors.txt", "r") as file:
            errors = file.read()
            if not errors.strip():
                run_command_async(output_file)
            else:
                print("Compilation failed. Check 'compile_errors.txt' for details.")

def create_new_script(gridIndex, scriptIndex):
    global selectedScriptIndex, currentModeIndex
    selectedScriptIndex = scriptIndex
    grids[gridIndex].scripts[scriptIndex].isEditing = True
    file_extension = MODE_EXTENSIONS[currentModeIndex]
    grids[gridIndex].scripts[scriptIndex].filename = f"{GAME_FILES_PATH}script{gridIndex * MAX_SCRIPTS + scriptIndex + 1}.{file_extension}"
    grids[gridIndex].scripts[scriptIndex].fileType = currentModeIndex
    if not does_file_exist(grids[gridIndex].scripts[scriptIndex].filename):
        save_script_to_file(grids[gridIndex].scripts[scriptIndex].filename, "")
    else:
        grids[gridIndex].scripts[scriptIndex].text = load_script_from_file(grids[gridIndex].scripts[scriptIndex].filename)

def create_description_file(scriptFilename):
    descriptionFilename = f"{scriptFilename}_description.txt"
    if not does_file_exist(descriptionFilename):
        with open(descriptionFilename, "w") as file:
            file.write(f"Description for {scriptFilename}")

def switch_grid(gridID):
    global currentGridIndex, selectedScriptIndex
    if 0 <= gridID < MAX_GRIDS:
        currentGridIndex = gridID
        selectedScriptIndex = -1

def toggle_script_mode():
    global currentModeIndex
    currentModeIndex = (currentModeIndex + 1) % len(MODES)
    for i in range(MAX_GRIDS):
        for j in range(MAX_SCRIPTS):
            file_extension = MODE_EXTENSIONS[currentModeIndex]
            grids[i].scripts[j].filename = f"{GAME_FILES_PATH}script{i * MAX_SCRIPTS + j + 1}.{file_extension}"
            grids[i].scripts[j].fileType = currentModeIndex

def toggle_edit_mode():
    global isEditingMode
    isEditingMode = not isEditingMode

def draw_help_menu():
    helpX = 20
    helpY = 100
    draw_rectangle(10, 90, 780, 400, LIGHTGRAY)
    draw_text("HELP MENU", helpX, helpY, 30, DARKGRAY)
    help_items = [
        "1. Grid Navigation: Use LEFT and RIGHT arrow keys to switch grids.",
        "2. File Mode Toggle: Press '1' to switch between file types.",
        "3. Edit/Execute Mode Toggle: Press '2' to toggle between Editing and Executing modes.",
        "4. Creating Scripts: Click on a grid button to create a new script in the selected mode.",
        "5. Editing Scripts: Click on an existing script button to edit the script in Notepad.",
        "6. Saving Scripts: Press 'S' to save the currently opened script.",
        "7. Executing Scripts: Press 'E' to execute the current script (Python or compile C).",
        "8. Creating Descriptions: Right-click a script button to create a description file.",
        "9. Existing Scripts: Green buttons indicate scripts that exist in 'gameFiles'.",
        "10. Toggle Help Menu: Press 'H' to show or hide this help menu."
    ]
    for i, item in enumerate(help_items):
        draw_text(item, helpX, helpY + 40 + i * 30, 20, DARKGRAY)

def draw_feedback_panel():
    panelX = 620
    panelY = 10
    draw_rectangle(panelX - 10, panelY - 10, 190, 150, LIGHTGRAY)
    draw_text("FEEDBACK PANEL", panelX, panelY, 20, DARKGRAY)
    draw_text(f"Current Grid: {currentGridIndex + 1}", panelX, panelY + 30, 20, DARKGRAY)
    draw_text(f"Mode: {MODES[currentModeIndex]}", panelX, panelY + 50, 20, DARKGRAY)
    draw_text(f"Edit Mode: {'Editing' if isEditingMode else 'Executing'}", panelX, panelY + 70, 20, DARKGRAY)
    if selectedScriptIndex != -1:
        draw_text(f"Selected Script: {grids[currentGridIndex].scripts[selectedScriptIndex].filename}", panelX, panelY + 90, 20, DARKGRAY)
        if does_file_exist(grids[currentGridIndex].scripts[selectedScriptIndex].filename):
            draw_text("File Status: Exists", panelX, panelY + 110, 20, GREEN)
        else:
            draw_text("File Status: New", panelX, panelY + 110, 20, RED)

def initialize_and_load_existing_scripts():
    for i in range(MAX_GRIDS):
        grids[i].gridID = i
        for j in range(MAX_SCRIPTS):
            grids[i].scripts[j].isEditing = False
            grids[i].scripts[j].text = ""
            grids[i].scripts[j].filename = ""
            grids[i].scripts[j].fileType = 0
            filename = f"{GAME_FILES_PATH}script{i * MAX_SCRIPTS + j + 1}.{'py'}"
            if does_file_exist(filename):
                grids[i].scripts[j].filename = filename
                grids[i].scripts[j].fileType = 0
                grids[i].scripts[j].text = load_script_from_file(filename)

def main():
    global currentGridIndex, selectedScriptIndex, currentModeIndex, isEditingMode, showHelpMenu

    # Initialize window
    set_config_flags(FLAG_WINDOW_RESIZABLE)
    init_window(800, 600, "Script Editor - press h for Help Menu")
    maximize_window()
    set_target_fps(60)

    # Ensure the game files directory exists
    os.makedirs(GAME_FILES_PATH, exist_ok=True)

    # Initialize grids and scripts
    initialize_and_load_existing_scripts()

    while not window_should_close():
        mouse_position = get_mouse_position()

        # Handle grid navigation with arrow keys
        if is_key_pressed(KEY_RIGHT):
            switch_grid((currentGridIndex + 1) % MAX_GRIDS)
        if is_key_pressed(KEY_LEFT):
            switch_grid((currentGridIndex - 1 + MAX_GRIDS) % MAX_GRIDS)

        # Toggle file mode
        if is_key_pressed(KEY_ONE):
            toggle_script_mode()

        # Toggle Edit/Execute mode
        if is_key_pressed(KEY_TWO):
            toggle_edit_mode()

        # Toggle Help Menu
        if is_key_pressed(KEY_H):
            showHelpMenu = not showHelpMenu

        # Check for button clicks to create or edit scripts
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            xIndex = int(mouse_position.x // BUTTON_SIZE)
            yIndex = int(mouse_position.y // BUTTON_SIZE)
            index = yIndex * GRID_COLS + xIndex
            if xIndex < GRID_COLS and yIndex < GRID_ROWS and index < MAX_SCRIPTS:
                if not does_file_exist(grids[currentGridIndex].scripts[index].filename):
                    create_new_script(currentGridIndex, index)
                elif isEditingMode:
                    selectedScriptIndex = index
                    grids[currentGridIndex].scripts[index].isEditing = True
                    open_script_in_notepad(grids[currentGridIndex].scripts[index].filename)

        # Handle right-click to create a description file
        if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            xIndex = int(mouse_position.x // BUTTON_SIZE)
            yIndex = int(mouse_position.y // BUTTON_SIZE)
            index = yIndex * GRID_COLS + xIndex
            if xIndex < GRID_COLS and yIndex < GRID_ROWS and index < MAX_SCRIPTS:
                if does_file_exist(grids[currentGridIndex].scripts[index].filename):
                    create_description_file(grids[currentGridIndex].scripts[index].filename)

        # Handle save and execute operations using hotkeys
        if selectedScriptIndex != -1:
            if isEditingMode and is_key_pressed(KEY_S):
                save_script_to_file(grids[currentGridIndex].scripts[selectedScriptIndex].filename, grids[currentGridIndex].scripts[selectedScriptIndex].text)
            if not isEditingMode and is_key_pressed(KEY_E):
                if grids[currentGridIndex].scripts[selectedScriptIndex].fileType == 1:  # C file type
                    compile_and_execute_c_file(grids[currentGridIndex].scripts[selectedScriptIndex].filename)
                elif grids[currentGridIndex].scripts[selectedScriptIndex].fileType == 0:  # Python file type
                    execute_python_script(grids[currentGridIndex].scripts[selectedScriptIndex].filename)

        # Draw grid and UI
        begin_drawing()
        clear_background(RAYWHITE)

        if showHelpMenu:
            draw_help_menu()
        else:
            draw_text(f"Grid ID: {grids[currentGridIndex].gridID}", 10, 10, 20, DARKGRAY)

            for y in range(GRID_ROWS):
                for x in range(GRID_COLS):
                    index = y * GRID_COLS + x
                    button = Rectangle(x * BUTTON_SIZE, y * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)

                    # Default button color is light gray
                    buttonColor = LIGHTGRAY

                    # If the corresponding script file exists, set the color based on the current mode
                    if does_file_exist(grids[currentGridIndex].scripts[index].filename):
                        buttonColor = MODE_COLORS[grids[currentGridIndex].scripts[index].fileType]

                    # Draw button with the determined color
                    draw_rectangle_rec(button, buttonColor)
                    draw_rectangle_lines_ex(button, 2, DARKGRAY)

                    scriptNumber = currentGridIndex * MAX_SCRIPTS + index + 1
                    if index == selectedScriptIndex:
                        draw_rectangle_rec(button, YELLOW)
                        draw_text("Editing...", button.x + 5, button.y + 5, 20, DARKGRAY)
                    else:
                        draw_text(str(scriptNumber), button.x + 5, button.y + 5, 20, DARKGRAY)

            draw_feedback_panel()

        end_drawing()

    close_window()

if __name__ == "__main__":
    main()

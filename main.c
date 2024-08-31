//gcc main.c -o homeGame -I"C:/Users/dacoo/raylib/src" -L"C:/Users/dacoo/raylib/src" -lraylib -lopengl32 -lgdi32 -lwinmm -lm -lpthread
#include "raylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <pthread.h>

#ifdef _WIN32
#include <direct.h>
#define mkdir _mkdir  // Windows-specific mkdir alias
#endif

#define GRID_ROWS 5
#define GRID_COLS 5
#define BUTTON_SIZE 100
#define MAX_SCRIPTS 25
#define MAX_TEXT_LENGTH 512
#define MAX_GRIDS 200
#define GAME_FILES_PATH "gameFiles/"

// Function declarations
void SaveScriptToFile(const char* filename, const char* text);
void LoadScriptFromFile(const char* filename, char* textBuffer, int bufferSize);
bool DoesFileExist(const char* filename);
void* ExecuteCommand(void* arg);
void RunCommandAsync(const char* command);
void OpenScriptInNotepad(const char* filename);
void ExecutePythonScript(const char* filename);
void CompileAndExecuteCFile(const char* filename);
void CreateNewScript(int gridIndex, int scriptIndex);
void CreateDescriptionFile(const char* scriptFilename);
void SwitchGrid(int gridID);
void ToggleScriptMode();
void ToggleEditMode();
void DrawHelpMenu();
void DrawFeedbackPanel();
void InitializeAndLoadExistingScripts();

// Define the structures and variables
typedef struct {
    char text[MAX_TEXT_LENGTH];
    bool isEditing;
    char filename[50];
    bool isCFile;
} Script;

typedef struct {
    Script scripts[MAX_SCRIPTS];
    int gridID;
} ScriptGrid;

ScriptGrid grids[MAX_GRIDS];
int currentGridIndex = 0;
int selectedScriptIndex = -1;
bool isCFile = false;
bool isEditingMode = true;
bool showHelpMenu = false;

// Function definitions
void SaveScriptToFile(const char* filename, const char* text) {
    FILE* file = fopen(filename, "w");
    if (file) {
        fprintf(file, "%s", text);
        fclose(file);
    }
}

void LoadScriptFromFile(const char* filename, char* textBuffer, int bufferSize) {
    FILE* file = fopen(filename, "r");
    if (file) {
        fgets(textBuffer, bufferSize, file);
        fclose(file);
    }
}

bool DoesFileExist(const char* filename) {
    struct stat buffer;
    return (stat(filename, &buffer) == 0);
}

void* ExecuteCommand(void* arg) {
    char* command = (char*)arg;
    system(command);
    free(command);
    return NULL;
}

void RunCommandAsync(const char* command) {
    pthread_t thread;
    char* commandCopy = strdup(command);
    pthread_create(&thread, NULL, ExecuteCommand, commandCopy);
    pthread_detach(thread);
}

void OpenScriptInNotepad(const char* filename) {
    char command[256];
    snprintf(command, sizeof(command), "notepad %s", filename);
    RunCommandAsync(command);
}

void ExecutePythonScript(const char* filename) {
    char command[256];
    snprintf(command, sizeof(command), "python %s", filename);
    RunCommandAsync(command);
}

void CompileAndExecuteCFile(const char* filename) {
    // Compile the C file into an executable named 'output.exe'
    char command[512];
    
    // Create the output file path based on the input file
    char outputFile[256];
    snprintf(outputFile, sizeof(outputFile), "output_%d.exe", currentGridIndex);

    // Format the compile command
    snprintf(command, sizeof(command), "gcc %s -o %s 2> compile_errors.txt", filename, outputFile);

    // Run the compile command asynchronously
    RunCommandAsync(command);

    // Check if the compilation was successful before running
    FILE *file = fopen("compile_errors.txt", "r");
    if (file) {
        char errorLine[256];
        if (fgets(errorLine, sizeof(errorLine), file) == NULL) {
            // No errors, so run the executable
            snprintf(command, sizeof(command), "%s", outputFile);
            RunCommandAsync(command);
        } else {
            // Display compilation errors to the user
            printf("Compilation failed. Check 'compile_errors.txt' for details.\n");
        }
        fclose(file);
    }
}


void CreateNewScript(int gridIndex, int scriptIndex) {
    selectedScriptIndex = scriptIndex;
    grids[gridIndex].scripts[scriptIndex].isEditing = true;

    if (isCFile) {
        snprintf(grids[gridIndex].scripts[scriptIndex].filename, sizeof(grids[gridIndex].scripts[scriptIndex].filename), GAME_FILES_PATH "script%d.c", gridIndex * MAX_SCRIPTS + scriptIndex + 1);
    } else {
        snprintf(grids[gridIndex].scripts[scriptIndex].filename, sizeof(grids[gridIndex].scripts[scriptIndex].filename), GAME_FILES_PATH "script%d.py", gridIndex * MAX_SCRIPTS + scriptIndex + 1);
    }
    grids[gridIndex].scripts[scriptIndex].isCFile = isCFile;

    if (!DoesFileExist(grids[gridIndex].scripts[scriptIndex].filename)) {
        SaveScriptToFile(grids[gridIndex].scripts[scriptIndex].filename, "");
    } else {
        LoadScriptFromFile(grids[gridIndex].scripts[scriptIndex].filename, grids[gridIndex].scripts[scriptIndex].text, MAX_TEXT_LENGTH);
    }
}

void CreateDescriptionFile(const char* scriptFilename) {
    char descriptionFilename[256];
    snprintf(descriptionFilename, sizeof(descriptionFilename), "%s_description.txt", scriptFilename);

    if (!DoesFileExist(descriptionFilename)) {
        FILE* file = fopen(descriptionFilename, "w");
        if (file) {
            fprintf(file, "Description for %s", scriptFilename);
            fclose(file);
        }
    }
}

void SwitchGrid(int gridID) {
    if (gridID >= 0 && gridID < MAX_GRIDS) {
        currentGridIndex = gridID;
        selectedScriptIndex = -1;
    }
}

void ToggleScriptMode() {
    // Toggle between Python mode and C mode
    isCFile = !isCFile;
    
    // Update the filenames for the current grid to reflect the new mode
    for (int i = 0; i < MAX_GRIDS; i++) {
        for (int j = 0; j < MAX_SCRIPTS; j++) {
            if (isCFile) {
                snprintf(grids[i].scripts[j].filename, sizeof(grids[i].scripts[j].filename), GAME_FILES_PATH "script%d.c", i * MAX_SCRIPTS + j + 1);
            } else {
                snprintf(grids[i].scripts[j].filename, sizeof(grids[i].scripts[j].filename), GAME_FILES_PATH "script%d.py", i * MAX_SCRIPTS + j + 1);
            }
            grids[i].scripts[j].isCFile = isCFile;  // Update the file type indicator
        }
    }
}


void ToggleEditMode() {
    isEditingMode = !isEditingMode;
}

void DrawHelpMenu() {
    int helpX = 20;
    int helpY = 100;
    DrawRectangle(10, 90, 780, 400, LIGHTGRAY);
    DrawText("HELP MENU", helpX, helpY, 30, DARKGRAY);
    DrawText("1. Grid Navigation: Use LEFT and RIGHT arrow keys to switch grids.", helpX, helpY + 40, 20, DARKGRAY);
    DrawText("2. Python/C Mode Toggle: Press '1' to switch between Python and C modes.", helpX, helpY + 70, 20, DARKGRAY);
    DrawText("3. Edit/Execute Mode Toggle: Press '2' to toggle between Editing and Executing modes.", helpX, helpY + 100, 20, DARKGRAY);
    DrawText("4. Creating Scripts: Click on a grid button to create a new script in the selected mode.", helpX, helpY + 130, 20, DARKGRAY);
    DrawText("5. Editing Scripts: Click on an existing script button to edit the script in Notepad.", helpX, helpY + 160, 20, DARKGRAY);
    DrawText("6. Saving Scripts: Press 'S' to save the currently opened script.", helpX, helpY + 190, 20, DARKGRAY);
    DrawText("7. Executing Scripts: Press 'E' to execute the current script (Python or compile C).", helpX, helpY + 220, 20, DARKGRAY);
    DrawText("8. Creating Descriptions: Right-click a script button to create a description file.", helpX, helpY + 250, 20, DARKGRAY);
    DrawText("9. Existing Scripts: Green buttons indicate scripts that exist in 'gameFiles'.", helpX, helpY + 280, 20, DARKGRAY);
    DrawText("10. Toggle Help Menu: Press 'H' to show or hide this help menu.", helpX, helpY + 310, 20, DARKGRAY);
}

void DrawFeedbackPanel() {
    int panelX = 620;
    int panelY = 10;
    DrawRectangle(panelX - 10, panelY - 10, 190, 150, LIGHTGRAY);
    DrawText("FEEDBACK PANEL", panelX, panelY, 20, DARKGRAY);
    DrawText(TextFormat("Current Grid: %d", currentGridIndex + 1), panelX, panelY + 30, 20, DARKGRAY);
    DrawText(TextFormat("Mode: %s", isCFile ? "C" : "Python"), panelX, panelY + 50, 20, DARKGRAY);
    DrawText(TextFormat("Edit Mode: %s", isEditingMode ? "Editing" : "Executing"), panelX, panelY + 70, 20, DARKGRAY);

    if (selectedScriptIndex != -1) {
        DrawText(TextFormat("Selected Script: %s", grids[currentGridIndex].scripts[selectedScriptIndex].filename), panelX, panelY + 90, 20, DARKGRAY);
        if (DoesFileExist(grids[currentGridIndex].scripts[selectedScriptIndex].filename)) {
            DrawText("File Status: Exists", panelX, panelY + 110, 20, GREEN);
        } else {
            DrawText("File Status: New", panelX, panelY + 110, 20, RED);
        }
    }
}

void InitializeAndLoadExistingScripts() {
    for (int i = 0; i < MAX_GRIDS; i++) {
        grids[i].gridID = i;
        for (int j = 0; j < MAX_SCRIPTS; j++) {
            grids[i].scripts[j].isEditing = false;
            grids[i].scripts[j].text[0] = '\0';
            grids[i].scripts[j].filename[0] = '\0';
            grids[i].scripts[j].isCFile = false;

            char filename[100];
            snprintf(filename, sizeof(filename), GAME_FILES_PATH "script%d.%s", i * MAX_SCRIPTS + j + 1, isCFile ? "c" : "py");
            
            if (DoesFileExist(filename)) {
                strcpy(grids[i].scripts[j].filename, filename);
                grids[i].scripts[j].isCFile = (strstr(filename, ".c") != NULL);
                LoadScriptFromFile(grids[i].scripts[j].filename, grids[i].scripts[j].text, MAX_TEXT_LENGTH);
            }
        }
    }
}

int main() {
    // Set the window to be resizable
    SetConfigFlags(FLAG_WINDOW_RESIZABLE);

    // Initialize window
    InitWindow(800, 600, "Script Editor - press h for Help Menu");
    MaximizeWindow();  // Maximize window on startup
    SetTargetFPS(60);

    // Ensure the game files directory exists
    mkdir(GAME_FILES_PATH);

    // Initialize grids and scripts
    InitializeAndLoadExistingScripts();

    while (!WindowShouldClose()) {
        Vector2 mousePosition = GetMousePosition();

        // Handle grid navigation with arrow keys
        if (IsKeyPressed(KEY_RIGHT)) {
            SwitchGrid((currentGridIndex + 1) % MAX_GRIDS);
        }
        if (IsKeyPressed(KEY_LEFT)) {
            SwitchGrid((currentGridIndex - 1 + MAX_GRIDS) % MAX_GRIDS);
        }

        // Toggle Python/C mode
        if (IsKeyPressed(KEY_ONE)) {
            ToggleScriptMode();  // Switch between Python and C grids
        }

        // Toggle Edit/Execute mode
        if (IsKeyPressed(KEY_TWO)) {
            ToggleEditMode();
        }

        // Toggle Help Menu
        if (IsKeyPressed(KEY_H)) {
            showHelpMenu = !showHelpMenu;
        }

        // Check for button clicks to create or edit scripts
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            int xIndex = mousePosition.x / BUTTON_SIZE;
            int yIndex = mousePosition.y / BUTTON_SIZE;
            int index = yIndex * GRID_COLS + xIndex;

            if (xIndex < GRID_COLS && yIndex < GRID_ROWS) {
                if (index < MAX_SCRIPTS) {
                    if (!DoesFileExist(grids[currentGridIndex].scripts[index].filename)) {
                        CreateNewScript(currentGridIndex, index);
                    } else if (isEditingMode) {
                        // Only open in Notepad if in editing mode
                        selectedScriptIndex = index;
                        grids[currentGridIndex].scripts[index].isEditing = true;
                        OpenScriptInNotepad(grids[currentGridIndex].scripts[index].filename);
                    }
                }
            }
        }

        // Handle right-click to create a description file
        if (IsMouseButtonPressed(MOUSE_BUTTON_RIGHT)) {
            int xIndex = mousePosition.x / BUTTON_SIZE;
            int yIndex = mousePosition.y / BUTTON_SIZE;
            int index = yIndex * GRID_COLS + xIndex;

            if (xIndex < GRID_COLS && yIndex < GRID_ROWS && index < MAX_SCRIPTS) {
                if (DoesFileExist(grids[currentGridIndex].scripts[index].filename)) {
                    CreateDescriptionFile(grids[currentGridIndex].scripts[index].filename);
                }
            }
        }

        // Handle save and execute operations using hotkeys
        if (selectedScriptIndex != -1) {
            if (isEditingMode && IsKeyPressed(KEY_S)) {
                // Save only if in editing mode
                SaveScriptToFile(grids[currentGridIndex].scripts[selectedScriptIndex].filename, grids[currentGridIndex].scripts[selectedScriptIndex].text);
            }
            if (!isEditingMode && IsKeyPressed(KEY_E)) {
                // Execute only if in execution mode
                if (grids[currentGridIndex].scripts[selectedScriptIndex].isCFile) {
                    CompileAndExecuteCFile(grids[currentGridIndex].scripts[selectedScriptIndex].filename);
                } else {
                    ExecutePythonScript(grids[currentGridIndex].scripts[selectedScriptIndex].filename);
                }
            }
        }

        // Draw grid and UI
        BeginDrawing();
        ClearBackground(RAYWHITE);

        if (showHelpMenu) {
            DrawHelpMenu();  // Draw help menu if the flag is set
        } else {
            DrawText(TextFormat("Grid ID: %d", grids[currentGridIndex].gridID), 10, 10, 20, DARKGRAY);

            for (int y = 0; y < GRID_ROWS; y++) {
                for (int x = 0; x < GRID_COLS; x++) {
                    int index = y * GRID_COLS + x;
                    Rectangle button = { x * BUTTON_SIZE, y * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE };
                    
                    // Default button color is light gray
                    Color buttonColor = LIGHTGRAY; 

                    // If the corresponding script file exists, set the color based on the current mode
                    if (DoesFileExist(grids[currentGridIndex].scripts[index].filename)) {
                        buttonColor = isCFile ? YELLOW : PURPLE;  // Yellow for C mode, purple for Python mode
                    }

                    // Draw button with the determined color
                    DrawRectangleRec(button, buttonColor);
                    DrawRectangleLinesEx(button, 2, DARKGRAY);

                    int scriptNumber = currentGridIndex * MAX_SCRIPTS + index + 1;
                    if (index == selectedScriptIndex) {
                        DrawRectangleRec(button, YELLOW);
                        DrawText("Editing...", button.x + 5, button.y + 5, 20, DARKGRAY);
                    } else {
                        DrawText(TextFormat("%d", scriptNumber), button.x + 5, button.y + 5, 20, DARKGRAY);
                    }
                }
            }

            // Draw feedback panel
            int panelX = 620;
            int panelY = 10;
            DrawRectangle(panelX - 10, panelY - 10, 190, 150, LIGHTGRAY);  // Panel background
            DrawText("FEEDBACK PANEL", panelX, panelY, 20, DARKGRAY);
            DrawText(TextFormat("Current Grid: %d", currentGridIndex + 1), panelX, panelY + 30, 20, DARKGRAY);

            // Draw "Mode" with background fill based on mode type
            if (isCFile) {
                DrawRectangle(panelX, panelY + 50, 80, 30, YELLOW); // Yellow background for "C"
                DrawText("C", panelX, panelY + 50, 20, DARKGRAY);
            } else {
                DrawRectangle(panelX, panelY + 50, 120, 30, PURPLE); // Purple background for "Python"
                DrawText("Python", panelX, panelY + 50, 20, DARKGRAY);
            }

            // Draw Edit Mode status
            DrawText(TextFormat("Edit Mode: %s", isEditingMode ? "Editing" : "Executing"), panelX, panelY + 90, 20, DARKGRAY);

            if (selectedScriptIndex != -1) {
                DrawText(TextFormat("Selected Script: %s", grids[currentGridIndex].scripts[selectedScriptIndex].filename), panelX, panelY + 110, 20, DARKGRAY);
                if (DoesFileExist(grids[currentGridIndex].scripts[selectedScriptIndex].filename)) {
                    DrawText("File Status: Exists", panelX, panelY + 130, 20, GREEN);
                } else {
                    DrawText("File Status: New", panelX, panelY + 130, 20, RED);
                }
            }
        }

        EndDrawing();
    }

    CloseWindow();
    return 0;
}

#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <vector>
#include <filesystem>
#include <unordered_map>

//g++ programming.cpp -o programming -std=c++17 -pthread

const int MAX_SCRIPTS = 25;
const int MAX_GRIDS = 200;
const std::string GAME_FILES_PATH = "gameFiles/";

class Script {
public:
    std::string text;
    bool isEditing;
    std::string filename;
    std::string customCompileCommand;
    std::string customRunCommand;

    Script() : isEditing(false) {}
};

class ScriptGrid {
public:
    std::vector<Script> scripts;
    int gridID;

    ScriptGrid(int id) : gridID(id), scripts(MAX_SCRIPTS) {}
};

std::vector<ScriptGrid> grids(MAX_GRIDS, ScriptGrid(0));
int currentGridIndex = 0;
int selectedScriptIndex = -1;
bool isEditingMode = true;
bool showHelpMenu = false;

void save_script_to_file(const std::string &filename, const std::string &text) {
    std::ofstream file(filename);
    if (file.is_open()) {
        file << text;
        file.close();
    }
}

std::string load_script_from_file(const std::string &filename) {
    std::ifstream file(filename);
    std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    return content;
}

bool does_file_exist(const std::string &filename) {
    return std::filesystem::exists(filename);
}

void execute_command(const std::string &command) {
    system(command.c_str());
}

void run_command_async(const std::string &command) {
    std::thread t(execute_command, command);
    t.detach();
}

void open_script_in_notepad(const std::string &filename) {
    run_command_async("notepad " + filename);
}

void compile_and_execute_cpp_file(const std::string &filename, const std::string &output_file) {
    std::string compile_command = "g++ " + filename + " -o " + output_file + " 2> compile_errors.txt";
    system(compile_command.c_str());

    if (does_file_exist("compile_errors.txt")) {
        std::ifstream file("compile_errors.txt");
        std::string errors((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();
        if (errors.empty()) {
            run_command_async("./" + output_file);
        } else {
            std::cout << "Compilation failed. Check 'compile_errors.txt' for details.\n";
        }
    }
}

void create_new_script(int gridIndex, int scriptIndex) {
    selectedScriptIndex = scriptIndex;
    grids[gridIndex].scripts[scriptIndex].isEditing = true;
    grids[gridIndex].scripts[scriptIndex].filename = GAME_FILES_PATH + "script" + std::to_string(gridIndex * MAX_SCRIPTS + scriptIndex + 1) + ".cpp";

    if (!does_file_exist(grids[gridIndex].scripts[scriptIndex].filename)) {
        save_script_to_file(grids[gridIndex].scripts[scriptIndex].filename, "");
    } else {
        grids[gridIndex].scripts[scriptIndex].text = load_script_from_file(grids[gridIndex].scripts[scriptIndex].filename);
    }
}

void toggle_edit_mode() {
    isEditingMode = !isEditingMode;
}

void set_custom_commands(Script& script) {
    std::cout << "Enter custom compilation command (or leave blank for default): ";
    std::getline(std::cin, script.customCompileCommand);
    std::cout << "Enter custom run command (or leave blank for default): ";
    std::getline(std::cin, script.customRunCommand);
}

void execute_script(Script& script) {
    if (!script.customRunCommand.empty()) {
        run_command_async(script.customRunCommand);
    } else {
        if (!script.customCompileCommand.empty()) {
            system(script.customCompileCommand.c_str());
        } else {
            compile_and_execute_cpp_file(script.filename, "output");
        }
    }
}

void main_menu() {
    std::string command;
    while (true) {
        if (showHelpMenu) {
            std::cout << "Help Menu:\n";
            std::cout << "1. Edit/Execute Mode Toggle\n";
            std::cout << "2. Create/Edit Scripts\n";
            std::cout << "3. Save Scripts\n";
            std::cout << "4. Execute Scripts\n";
            std::cout << "5. Set Custom Commands\n";
            std::cout << "6. Show/Hide Help Menu\n";
            std::cout << "7. Quit\n";
        }

        std::cout << "Enter command (help, create, edit, save, execute, toggle, custom, quit): ";
        std::cin >> command;
        std::cin.ignore();  // Ignore newline after command

        if (command == "create") {
            int gridIndex, scriptIndex;
            std::cout << "Enter Grid Index (0-" << MAX_GRIDS - 1 << "): ";
            std::cin >> gridIndex;
            std::cout << "Enter Script Index (0-" << MAX_SCRIPTS - 1 << "): ";
            std::cin >> scriptIndex;
            std::cin.ignore(); // Ignore newline
            create_new_script(gridIndex, scriptIndex);
        } else if (command == "edit") {
            if (selectedScriptIndex != -1) {
                open_script_in_notepad(grids[currentGridIndex].scripts[selectedScriptIndex].filename);
            } else {
                std::cout << "No script selected. Use 'create' to select a script.\n";
            }
        } else if (command == "save") {
            if (selectedScriptIndex != -1) {
                save_script_to_file(grids[currentGridIndex].scripts[selectedScriptIndex].filename, grids[currentGridIndex].scripts[selectedScriptIndex].text);
            } else {
                std::cout << "No script selected. Use 'create' to select a script.\n";
            }
        } else if (command == "execute") {
            if (!isEditingMode && selectedScriptIndex != -1) {
                execute_script(grids[currentGridIndex].scripts[selectedScriptIndex]);
            } else if (isEditingMode) {
                std::cout << "Switch to execute mode by using 'toggle' command.\n";
            } else {
                std::cout << "No script selected. Use 'create' to select a script.\n";
            }
        } else if (command == "toggle") {
            toggle_edit_mode();
            std::cout << "Mode switched to " << (isEditingMode ? "Edit" : "Execute") << " mode.\n";
        } else if (command == "custom") {
            if (selectedScriptIndex != -1) {
                set_custom_commands(grids[currentGridIndex].scripts[selectedScriptIndex]);
            } else {
                std::cout << "No script selected. Use 'create' to select a script.\n";
            }
        } else if (command == "help") {
            showHelpMenu = !showHelpMenu;
        } else if (command == "quit") {
            break;
        } else {
            std::cout << "Unknown command.\n";
        }
    }
}

int main() {
    std::filesystem::create_directory(GAME_FILES_PATH);
    main_menu();
    return 0;
}

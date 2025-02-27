#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <format>
#include <vector>
#include <filesystem>
#include <chrono>
#include <algorithm>
#include <regex>
#include <optional>
#include <ranges>
#include <map>
#include <sstream>
#include <limits>
#include <cctype>
#include <utility>
#include <zip.h>
#include <nlohmann/json.hpp>

namespace fs = std::filesystem;
using json = nlohmann::json;

// Program by Dominic Alexander Cooper
// Integrated C++23 version

class MemorySlotManager {
private:
    std::map<std::string, std::map<std::string, std::string>> memory_slots;

public:
    std::string assign_slot(const std::string& file_number, const std::string& slot_number, const std::string& value) {
        if (file_number.empty() || slot_number.empty() || value.empty()) {
            return "Error: Invalid input parameters.";
        }

        if (value_exists(value)) {
            return "Error: The value already exists in another memory slot.";
        }

        memory_slots[file_number][slot_number] = value;
        return std::format("Assigned value to slot {} in file {}.", slot_number, file_number);
    }

    std::string read_slot(const std::string& file_number, const std::string& slot_number) {
        if (memory_slots.contains(file_number) && 
            memory_slots[file_number].contains(slot_number)) {
            return memory_slots[file_number][slot_number];
        }
        return std::format("Slot {} not found in file {}.", slot_number, file_number);
    }

    std::optional<int> get_last_slot_number(const std::string& file_number) {
        if (memory_slots.contains(file_number) && !memory_slots[file_number].empty()) {
            try {
                std::vector<int> slots;
                for (const auto& [slot, _] : memory_slots[file_number]) {
                    bool is_digit = std::ranges::all_of(slot, [](char c) { return std::isdigit(c); });
                    if (is_digit) {
                        slots.push_back(std::stoi(slot));
                    }
                }
                if (!slots.empty()) {
                    return *std::max_element(slots.begin(), slots.end());
                }
            } catch (const std::exception&) {
                // Ignore exceptions
            }
        }
        return std::nullopt;
    }

    struct SearchResult {
        std::string file;
        std::string slot;
        std::string value;
    };

    std::vector<SearchResult> search_value(const std::string& value) {
        std::vector<SearchResult> results;
        std::string search_value_lower = to_lower(value);

        for (const auto& [file, slots] : memory_slots) {
            for (const auto& [slot, val] : slots) {
                if (to_lower(val).find(search_value_lower) != std::string::npos) {
                    results.push_back({file, slot, val});
                }
            }
        }

        return results;
    }

    bool value_exists(const std::string& value) {
        std::string value_lower = to_lower(value);

        for (const auto& [_, slots] : memory_slots) {
            for (const auto& [__, val] : slots) {
                if (to_lower(val) == value_lower) {
                    return true;
                }
            }
        }

        return false;
    }

    std::string call_slot_range(const std::string& file_number, int start_slot, int end_slot) {
        if (!memory_slots.contains(file_number)) {
            return "File " + file_number + " not found.";
        }

        std::vector<std::string> results;
        for (int slot = start_slot; slot <= end_slot; ++slot) {
            std::string slot_str = std::to_string(slot);
            if (memory_slots[file_number].contains(slot_str)) {
                results.push_back("Slot " + slot_str + ":\n" + memory_slots[file_number][slot_str]);
            } else {
                results.push_back("Slot " + slot_str + " not found.");
            }
        }

        std::string result;
        for (size_t i = 0; i < results.size(); ++i) {
            result += results[i];
            if (i < results.size() - 1) {
                result += "\n\n";
            }
        }
        return result;
    }

    std::string export_to_text_file(const std::string& file_number, const std::string& file_path) {
        if (!memory_slots.contains(file_number)) {
            return "Error: File " + file_number + " not found.";
        }

        try {
            std::ofstream file(file_path);
            if (!file.is_open()) {
                return "Error: Could not open file for writing.";
            }

            auto slots = memory_slots[file_number];
            std::vector<std::string> slot_keys;

            try {
                std::vector<int> numeric_keys;
                for (const auto& [key, _] : slots) {
                    bool is_digit = true;
                    for (char c : key) {
                        if (!std::isdigit(c)) {
                            is_digit = false;
                            break;
                        }
                    }
                    if (is_digit) {
                        numeric_keys.push_back(std::stoi(key));
                    }
                }
                std::sort(numeric_keys.begin(), numeric_keys.end());
                for (int key : numeric_keys) {
                    slot_keys.push_back(std::to_string(key));
                }
            } catch (const std::exception&) {
                // If conversion fails, sort alphabetically
                for (const auto& [key, _] : slots) {
                    slot_keys.push_back(key);
                }
                std::sort(slot_keys.begin(), slot_keys.end());
            }

            for (const auto& slot : slot_keys) {
                std::string value = slots[slot];
                // Format: SLOT <number>
                file << "SLOT " << slot << std::endl;
                // Then the value
                file << value << std::endl;
                // Add a separator between slots
                file << "--------------------" << std::endl;
            }

            return "Exported file " + file_number + " to " + fs::path(file_path).filename().string();
        } catch (const std::exception& e) {
            return "Error exporting to text file: " + std::string(e.what());
        }
    }

    std::pair<std::string, std::map<std::string, std::string>> parse_text_file(const std::string& file_path) {
        try {
            // Extract file number from filename (e.g., "file1.txt" -> "1")
            std::string file_name = fs::path(file_path).filename().string();
            std::regex file_number_pattern("(\\d+)");
            std::smatch file_number_match;
            std::string file_number = "1";
            if (std::regex_search(file_name, file_number_match, file_number_pattern)) {
                file_number = file_number_match[1].str();
            }

            std::ifstream file(file_path);
            if (!file.is_open()) {
                throw std::runtime_error("Could not open file for reading.");
            }

            std::map<std::string, std::string> slots;
            std::string line;
            std::string current_slot;
            std::string current_content;
            bool in_slot = false;

            while (std::getline(file, line)) {
                if (line.find("SLOT ") == 0) {
                    // If we were in a slot, save the previous content
                    if (in_slot && !current_slot.empty()) {
                        // Remove separator if present
                        size_t sep_pos = current_content.find("--------------------");
                        if (sep_pos != std::string::npos) {
                            current_content = current_content.substr(0, sep_pos);
                        }
                        // Trim trailing whitespace
                        current_content = std::regex_replace(current_content, std::regex("\\s+$"), "");
                        slots[current_slot] = current_content;
                    }

                    // Start a new slot
                    current_slot = line.substr(5); // Skip "SLOT "
                    current_content = "";
                    in_slot = true;
                } else if (in_slot) {
                    if (current_content.empty()) {
                        current_content = line;
                    } else {
                        current_content += "\n" + line;
                    }
                }
            }

            // Save the last slot
            if (in_slot && !current_slot.empty()) {
                // Remove separator if present
                size_t sep_pos = current_content.find("--------------------");
                if (sep_pos != std::string::npos) {
                    current_content = current_content.substr(0, sep_pos);
                }
                // Trim trailing whitespace
                current_content = std::regex_replace(current_content, std::regex("\\s+$"), "");
                slots[current_slot] = current_content;
            }

            return {file_number, slots};
        } catch (const std::exception& e) {
            throw std::runtime_error("Error parsing text file: " + std::string(e.what()));
        }
    }

    std::string load_json_file(const std::string& file_path) {
        try {
            std::ifstream file(file_path);
            if (!file.is_open()) {
                return "Error: Could not open file for reading.";
            }

            json content;
            file >> content;

            // Get a file number from the filename
            std::string file_name = fs::path(file_path).filename().string();
            std::regex file_number_pattern("(\\d+)");
            std::smatch file_number_match;
            std::string file_number = "1";
            if (std::regex_search(file_name, file_number_match, file_number_pattern)) {
                file_number = file_number_match[1].str();
            }

            if (content.is_object()) {
                // Check if this is already in our expected format {file: {slot: value}}
                bool is_full_structure = false;
                for (const auto& [_, value] : content.items()) {
                    if (value.is_object()) {
                        is_full_structure = true;
                        break;
                    }
                }

                if (is_full_structure) {
                    // It's our full structure
                    for (const auto& [file_key, slots] : content.items()) {
                        if (!memory_slots.contains(file_key)) {
                            memory_slots[file_key] = {};
                        }

                        for (const auto& [slot_number, value] : slots.items()) {
                            if (value.is_string()) {
                                memory_slots[file_key][slot_number] = value.get<std::string>();
                            } else {
                                memory_slots[file_key][slot_number] = value.dump(2);
                            }
                        }
                    }
                } else {
                    // It's a single file's slots {slot: value}
                    if (!memory_slots.contains(file_number)) {
                        memory_slots[file_number] = {};
                    }

                    for (const auto& [slot_number, value] : content.items()) {
                        if (value.is_string()) {
                            memory_slots[file_number][slot_number] = value.get<std::string>();
                        } else {
                            memory_slots[file_number][slot_number] = value.dump(2);
                        }
                    }
                }
            }

            return "Loaded JSON file: " + fs::path(file_path).filename().string();
        } catch (const std::exception& e) {
            return "Error loading " + fs::path(file_path).filename().string() + ": " + e.what();
        }
    }

    std::string load_txt_file(const std::string& file_path) {
        try {
            auto [file_number, slots] = parse_text_file(file_path);

            if (!memory_slots.contains(file_number)) {
                memory_slots[file_number] = {};
            }

            // Add the loaded slots to our memory
            for (const auto& [slot_number, value] : slots) {
                memory_slots[file_number][slot_number] = value;
            }

            return "Loaded text file: " + fs::path(file_path).filename().string() + " as file " + file_number;
        } catch (const std::exception& e) {
            return "Error loading " + fs::path(file_path).filename().string() + ": " + e.what();
        }
    }

    std::string save_json_file(const std::string& file_path) {
        try {
            std::ofstream file(file_path);
            if (!file.is_open()) {
                return "Error: Could not open file for writing.";
            }

            json j_memory = json::object();

            for (const auto& [file_number, slots] : memory_slots) {
                j_memory[file_number] = json::object();
                for (const auto& [slot_number, value] : slots) {
                    j_memory[file_number][slot_number] = value;
                }
            }

            file << j_memory.dump(2);
            return "Memory slots saved to JSON: " + fs::path(file_path).filename().string();
        } catch (const std::exception& e) {
            return "Error saving file: " + std::string(e.what());
        }
    }

    std::string save_txt_file(const std::string& file_number, const std::string& file_path) {
        return export_to_text_file(file_number, file_path);
    }

    std::string save_zip_file(const std::string& file_path) {
        try {
            // Create a new zip archive
            int error = 0;
            zip_t* zip = zip_open(file_path.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &error);
            if (zip == nullptr) {
                return "Error creating zip archive.";
            }

            // Add JSON files
            for (const auto& [file_number, slots] : memory_slots) {
                // Create a JSON string for this file's slots
                json j_slots = json::object();
                for (const auto& [slot_number, value] : slots) {
                    j_slots[slot_number] = value;
                }
                std::string json_data = j_slots.dump(2);

                // Add the JSON data to the zip file
                std::string json_path = "json/file_" + file_number + ".json";
                zip_source_t* json_source = zip_source_buffer(zip, json_data.c_str(), json_data.size(), 0);
                if (json_source == nullptr) {
                    zip_close(zip);
                    return "Error creating source for JSON data.";
                }
                zip_file_add(zip, json_path.c_str(), json_source, ZIP_FL_OVERWRITE);

                // Also create a text file version
                std::string txt_data;
                for (const auto& [slot, value] : slots) {
                    txt_data += "SLOT " + slot + "\n" + value + "\n--------------------\n";
                }

                std::string txt_path = "txt/file_" + file_number + ".txt";
                zip_source_t* txt_source = zip_source_buffer(zip, txt_data.c_str(), txt_data.size(), 0);
                if (txt_source == nullptr) {
                    zip_close(zip);
                    return "Error creating source for text data.";
                }
                zip_file_add(zip, txt_path.c_str(), txt_source, ZIP_FL_OVERWRITE);
            }

            // Also save the complete structure as one JSON file
            json j_all = json::object();
            for (const auto& [file_number, slots] : memory_slots) {
                j_all[file_number] = json::object();
                for (const auto& [slot_number, value] : slots) {
                    j_all[file_number][slot_number] = value;
                }
            }
            std::string all_json = j_all.dump(2);
            zip_source_t* all_source = zip_source_buffer(zip, all_json.c_str(), all_json.size(), 0);
            if (all_source == nullptr) {
                zip_close(zip);
                return "Error creating source for complete JSON data.";
            }
            zip_file_add(zip, "all_memory_slots.json", all_source, ZIP_FL_OVERWRITE);

            // Close the zip file
            if (zip_close(zip) != 0) {
                return "Error closing zip archive.";
            }

            return "Memory slots saved to zip archive: " + fs::path(file_path).filename().string();
        } catch (const std::exception& e) {
            return "Error creating zip archive: " + std::string(e.what());
        }
    }

    std::string export_all_txt(const std::string& export_dir) {
        if (memory_slots.empty()) {
            return "No memory slots available to export.";
        }

        if (!fs::exists(export_dir)) {
            try {
                fs::create_directories(export_dir);
            } catch (const std::exception& e) {
                return "Error creating directory: " + std::string(e.what());
            }
        }

        int success_count = 0;
        int error_count = 0;
        std::vector<std::string> errors;

        for (const auto& [file_number, _] : memory_slots) {
            std::string file_path = (fs::path(export_dir) / ("file" + file_number + ".txt")).string();
            try {
                export_to_text_file(file_number, file_path);
                success_count++;
            } catch (const std::exception& e) {
                error_count++;
                errors.push_back("Error exporting file " + file_number + ": " + e.what());
            }
        }

        std::string result = "Exported " + std::to_string(success_count) + " files as text files";
        if (error_count > 0) {
            result += ", " + std::to_string(error_count) + " files had errors.";
            for (const auto& error : errors) {
                result += "\n" + error;
            }
        } else {
            result += ".";
        }

        return result;
    }

    const std::map<std::string, std::map<std::string, std::string>>& get_memory_slots() const {
        return memory_slots;
    }

    // Static utility function
    static std::string to_lower(const std::string& str) {
        std::string result = str;
        std::ranges::transform(result, result.begin(), 
                              [](unsigned char c) { return std::tolower(c); });
        return result;
    }

    // Generate all possible combinations using character set
    void generate_combinations(const std::string& chars, int n, const std::string& output_file) {
        std::ofstream file(output_file);
        if (!file) {
            throw std::runtime_error("Error opening output file.");
        }

        int k = chars.length() - 1;
        int id = 0;
        long long nbr_comb = static_cast<long long>(std::pow(k + 1, n));
        
        std::cout << std::format("Generating {} combinations...\n", nbr_comb);
        
        auto start_time = std::chrono::high_resolution_clock::now();
        
        for (int row = 0; row < nbr_comb; row++) {
            id++;
            file << std::format("\nF{}\n", id);
            
            std::string combination;
            for (int col = n - 1; col >= 0; col--) {
                int rdiv = static_cast<int>(std::pow(k + 1, col));
                int cell = (row / rdiv) % (k + 1);
                combination.push_back(chars[cell]);
            }
            
            file << combination;
            
            // Store in memory slots
            memory_slots[std::to_string(id)]["1"] = combination;
            
            // Show progress every 10%
            if (nbr_comb > 1000 && row % (nbr_comb / 10) == 0) {
                int percent = (row * 100) / nbr_comb;
                std::cout << std::format("Progress: {}%\n", percent);
            }
        }

        file << std::format("\n\nEnd.(k+1)^n = ({} + 1)^{} = {}\n", k, n, id);
        file.close();
        
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        std::cout << std::format("Generation completed in {:.2f} seconds.\n", duration.count() / 1000.0);
    }
};

class IntegratedApp {
private:
    MemorySlotManager memory_manager;
    bool running = true;
    
    void show_welcome_message() {
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "      INTEGRATED C++23 MEMORY & COMBINATION GENERATOR" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::cout << std::format("SYSTEM INITIALIZED: {:%Y-%m-%d %H:%M:%S}\n", *std::localtime(&time));
        
        std::cout << "MEMORY MANAGER & COMBINATION GENERATOR LOADED" << std::endl;
        std::cout << "READY FOR INPUT" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        std::cout << "Type \"help\" for a list of commands.\n" << std::endl;
    }
    
    void show_help() {
        std::string help_text = R"(
AVAILABLE COMMANDS:
------------------
assign <fileNumber> <slotNumber>
  <value>             : Assign a multi-line value to a slot
                        (Enter your multi-line value after the first line)
                        Type 'END' on a line by itself to finish input

read <fileNumber> <slotNumber>
                     : Read the value from a slot

last_slot <fileNumber>
                     : Get the last slot number in a file

search
  <value>             : Search for a multi-line value across all slots
                        (Type 'END' on a line by itself to finish input)

call <fileNumber> <startSlot> <endSlot>
                     : Call values from a range of slots

export <fileNumber> <filePath>
                     : Export a file's memory slots to a text file

generate <n>         : Generate all combinations with n cells
                       using the standard character set

custom_generate <n>  : Generate combinations with custom character set

display              : Show all memory slots
clear                : Clear the screen
help                 : Display this help message
exit                 : Exit the application

load_json <filePath>  : Load memory slots from a JSON file
load_txt <filePath>   : Load memory slots from a text file
save_json <filePath>  : Save all memory slots to a JSON file
save_txt <fileNumber> <filePath>
                     : Save a file's memory slots to a text file
save_zip <filePath>   : Save all memory slots to a ZIP archive
export_all_txt <dirPath>
                     : Export all files as separate text files

FILE FORMATS:
------------------
JSON                 : Standard format with nested objects
                       {fileNumber: {slotNumber: value, ...}, ...}
                       
TXT                  : Text format with SLOT markers
                       SLOT <number>
                       <value content>
                       --------------------
)";
        std::cout << help_text << std::endl;
    }
    
    void display_memory() {
        const auto& memory_slots = memory_manager.get_memory_slots();
        if (memory_slots.empty()) {
            std::cout << "\n>>> No memory slots available.\n" << std::endl;
            return;
        }

        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "MEMORY SLOT CONTENTS" << std::endl;
        std::cout << std::string(60, '=') << std::endl;

        for (const auto& [file_number, slots] : memory_slots) {
            std::cout << "\nFILE " << file_number << ":" << std::endl;
            std::cout << std::string(40, '-') << std::endl;
            
            // Sort slots numerically if possible
            std::vector<std::string> slot_numbers;
            try {
                std::vector<int> numeric_slots;
                for (const auto& [slot, _] : slots) {
                    bool is_digit = true;
                    for (char c : slot) {
                        if (!std::isdigit(c)) {
                            is_digit = false;
                            break;
                        }
                    }
                    if (is_digit) {
                        numeric_slots.push_back(std::stoi(slot));
                    }
                }
                std::sort(numeric_slots.begin(), numeric_slots.end());
                for (int slot : numeric_slots) {
                    slot_numbers.push_back(std::to_string(slot));
                }
            } catch (const std::exception&) {
                // If conversion fails, sort alphabetically
                for (const auto& [slot, _] : slots) {
                    slot_numbers.push_back(slot);
                }
                std::sort(slot_numbers.begin(), slot_numbers.end());
            }

            // Limit display to max 10 slots per file for readability
            int count = 0;
            for (const auto& slot : slot_numbers) {
                std::string value = slots.at(slot);
                // Truncate long values for display
                std::string display_value = value;
                if (display_value.length() > 100) {
                    display_value = display_value.substr(0, 97) + "...";
                }

                // Replace newlines with visible indicator for console display
                std::string newline_replaced;
                for (char c : display_value) {
                    if (c == '\n') {
                        newline_replaced += " ⏎ ";
                    } else {
                        newline_replaced += c;
                    }
                }

                std::cout << "Slot " << slot << ": " << newline_replaced << std::endl;
                
                count++;
                if (count >= 10 && slots.size() > 10) {
                    std::cout << std::format("... and {} more slots (not displayed)\n", 
                                           slots.size() - 10);
                    break;
                }
            }
        }

        std::cout << "\n" << std::string(60, '=') << std::endl;
    }
    
    // Generate the standard 100-character set
    std::string generate_char_set() {
        std::string chars = 
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "!@#$%^&*()-_=+[]{}|;:,.<>/?"
            " \t\n\r"
            "~`'\"\\"
            "€£¥¢©®™";
        
        // Ensure exactly 100 characters
        if (chars.length() > 100) {
            chars = chars.substr(0, 100);
        }
        else if (chars.length() < 100) {
            // Pad with additional characters if needed
            while (chars.length() < 100) {
                chars += '?';
            }
        }
        
        return chars;
    }
    
    void clear_screen() {
    #ifdef _WIN32
        std::system("cls");
    #else
        std::system("clear");
    #endif
    }
    
public:
    IntegratedApp() {
        show_welcome_message();
    }
    
    void execute_command(const std::string& command_input) {
        if (command_input.empty()) {
            return;
        }
        
        // Split the command input into lines to handle multi-line values
        std::vector<std::string> command_lines;
        std::istringstream iss(command_input);
        std::string line;
        while (std::getline(iss, line)) {
            command_lines.push_back(line);
        }
        
        std::vector<std::string> tokens;
        std::istringstream first_line_iss(command_lines[0]);
        std::string token;
        while (first_line_iss >> token) {
            tokens.push_back(token);
        }
        
        if (tokens.empty()) {
            return;
        }
        
        std::string cmd = tokens[0];
        std::transform(cmd.begin(), cmd.end(), cmd.begin(), 
                      [](unsigned char c) { return std::tolower(c); });
        
        try {
            if (cmd == "help" || cmd == "?") {
                show_help();
            }
            else if (cmd == "assign") {
                if (tokens.size() < 3) {
                    std::cout << "Error: Missing arguments for assign command." << std::endl;
                    return;
                }
                
                std::string file_number = tokens[1];
                std::string slot_number = tokens[2];
                
                std::string value;
                for (size_t i = 1; i < command_lines.size(); ++i) {
                    if (i > 1) value += "\n";
                    value += command_lines[i];
                }
                
                if (value.empty()) {
                    std::cout << "Enter multi-line value (type 'END' on a line by itself to finish):" << std::endl;
                    std::string line;
                    while (true) {
                        std::getline(std::cin, line);
                        if (line == "END") {
                            break;
                        }
                        if (!value.empty()) value += "\n";
                        value += line;
                    }
                }
                
                if (value.empty()) {
                    std::cout << "Error: No value provided for assign command." << std::endl;
                    return;
                }
                
                std::string result = memory_manager.assign_slot(file_number, slot_number, value);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "read") {
                if (tokens.size() < 3) {
                    std::cout << "Error: Missing arguments for read command." << std::endl;
                    return;
                }
                
                std::string result = memory_manager.read_slot(tokens[1], tokens[2]);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "last_slot") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing file number for last_slot command." << std::endl;
                    return;
                }
                
                auto last_slot = memory_manager.get_last_slot_number(tokens[1]);
                if (last_slot.has_value()) {
                    std::cout << std::format("\n>>> Last slot number in file {} is {}.", tokens[1], *last_slot) << std::endl;
                } else {
                    std::cout << std::format("\n>>> No slots found in file {}.", tokens[1]) << std::endl;
                }
            }
            else if (cmd == "search") {
                std::string search_value;
                
                if (tokens.size() == 1 && command_lines.size() < 2) {
                    std::cout << "Enter search value (type 'END' on a line by itself to finish):" << std::endl;
                    std::string line;
                    while (true) {
                        std::getline(std::cin, line);
                        if (line == "END") {
                            break;
                        }
                        if (!search_value.empty()) search_value += "\n";
                        search_value += line;
                    }
                } else {
                    // For search, handle multi-line input correctly
                    if (tokens.size() == 1) {
                        // If the first line contains just "search", use the rest as the search value
                        for (size_t i = 1; i < command_lines.size(); ++i) {
                            if (i > 1) search_value += "\n";
                            search_value += command_lines[i];
                        }
                    } else {
                        // Otherwise, use everything after "search" in the first line
                        std::string first_line_value;
                        for (size_t i = 1; i < tokens.size(); ++i) {
                            if (i > 1) first_line_value += " ";
                            first_line_value += tokens[i];
                        }
                        
                        if (command_lines.size() > 1) {
                            search_value = first_line_value + "\n";
                            for (size_t i = 1; i < command_lines.size(); ++i) {
                                if (i > 1) search_value += "\n";
                                search_value += command_lines[i];
                            }
                        } else {
                            search_value = first_line_value;
                        }
                    }
                }
                
                if (search_value.empty()) {
                    std::cout << "Error: No search value provided." << std::endl;
                    return;
                }
                
                auto search_results = memory_manager.search_value(search_value);
                if (!search_results.empty()) {
                    std::cout << "\n>>> Search Results:" << std::endl;
                    for (const auto& result : search_results) {
                        std::cout << "File: " << result.file << ", Slot: " << result.slot << ", Value:" << std::endl;
                        std::cout << result.value << std::endl << std::endl;
                    }
                } else {
                    std::cout << "\n>>> No results found." << std::endl;
                }
            }
            else if (cmd == "call") {
                if (tokens.size() < 4) {
                    std::cout << "Error: Missing arguments for call command." << std::endl;
                    return;
                }
                
                try {
                    std::string file_number = tokens[1];
                    int start_slot = std::stoi(tokens[2]);
                    int end_slot = std::stoi(tokens[3]);
                    std::string result = memory_manager.call_slot_range(file_number, start_slot, end_slot);
                    std::cout << "\n>>> " << result << std::endl;
                } catch (const std::exception&) {
                    std::cout << "Error: Slot numbers must be integers." << std::endl;
                }
            }
            else if (cmd == "export") {
                if (tokens.size() < 3) {
                    std::cout << "Error: Missing arguments for export command." << std::endl;
                    return;
                }
                
                std::string file_number = tokens[1];
                std::string file_path = tokens[2];
                std::string result = memory_manager.export_to_text_file(file_number, file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "generate") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Please specify the number of cells (n)." << std::endl;
                    return;
                }
                
                int n = std::stoi(tokens[1]);
                if (n <= 0) {
                    std::cout << "Error: n must be a positive integer." << std::endl;
                    return;
                }
                
                if (n > 6) {
                    std::cout << "Warning: Large values of n will generate very large outputs." << std::endl;
                    std::cout << "Continue? (y/n): ";
                    char response;
                    std::cin >> response;
                    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                    
                    if (tolower(response) != 'y') {
                        return;
                    }
                }
                
                std::string char_set = generate_char_set();
                std::cout << std::format("Using standard character set ({} chars)", char_set.length()) << std::endl;
                memory_manager.generate_combinations(char_set, n, "SOLUTION_RENAME.txt");
                std::cout << "Results written to SOLUTION_RENAME.txt" << std::endl;
            }
            else if (cmd == "custom_generate") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Please specify the number of cells (n)." << std::endl;
                    return;
                }
                
                int n = std::stoi(tokens[1]);
                if (n <= 0) {
                    std::cout << "Error: n must be a positive integer." << std::endl;
                    return;
                }
                
                std::cout << "Enter custom character set (press Enter to use default 100-char set): ";
                std::string custom_chars;
                std::getline(std::cin, custom_chars);
                
                if (custom_chars.empty()) {
                    custom_chars = generate_char_set();
                    std::cout << std::format("Using default character set ({} chars)", custom_chars.length()) << std::endl;
                } else {
                    std::cout << std::format("Using custom character set ({} chars)", custom_chars.length()) << std::endl;
                }
                
                memory_manager.generate_combinations(custom_chars, n, "CUSTOM_SOLUTION.txt");
                std::cout << "Results written to CUSTOM_SOLUTION.txt" << std::endl;
            }
            else if (cmd == "display" || cmd == "show") {
                display_memory();
            }
            else if (cmd == "clear") {
                clear_screen();
            }
            else if (cmd == "exit" || cmd == "quit") {
                std::cout << "Exiting application. Goodbye!" << std::endl;
                running = false;
            }
            else if (cmd == "load_json") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing file path for load_json command." << std::endl;
                    return;
                }
                
                std::string file_path = tokens[1];
                std::string result = memory_manager.load_json_file(file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "load_txt") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing file path for load_txt command." << std::endl;
                    return;
                }
                
                std::string file_path = tokens[1];
                std::string result = memory_manager.load_txt_file(file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "save_json") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing file path for save_json command." << std::endl;
                    return;
                }
                
                std::string file_path = tokens[1];
                std::string result = memory_manager.save_json_file(file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "save_txt") {
                if (tokens.size() < 3) {
                    std::cout << "Error: Missing arguments for save_txt command." << std::endl;
                    return;
                }
                
                std::string file_number = tokens[1];
                std::string file_path = tokens[2];
                std::string result = memory_manager.save_txt_file(file_number, file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "save_zip") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing file path for save_zip command." << std::endl;
                    return;
                }
                
                std::string file_path = tokens[1];
                std::string result = memory_manager.save_zip_file(file_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else if (cmd == "export_all_txt") {
                if (tokens.size() < 2) {
                    std::cout << "Error: Missing directory path for export_all_txt command." << std::endl;
                    return;
                }
                
                std::string directory_path = tokens[1];
                std::string result = memory_manager.export_all_txt(directory_path);
                std::cout << "\n>>> " << result << std::endl;
            }
            else {
                std::cout << "Unknown command: " << cmd << std::endl;
                std::cout << "Type 'help' for available commands." << std::endl;
            }
        }
        catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
    
    void run() {
        while (running) {
            std::cout << "> ";
            std::string command;
            std::getline(std::cin, command);
            
            // Handle multi-line input for assign and search commands
            if (command.find("assign ") == 0 || command == "search" || command.find("search ") == 0) {
                std::vector<std::string> tokens;
                std::istringstream iss(command);
                std::string token;
                while (iss >> token) {
                    tokens.push_back(token);
                }
                
                if ((command.find("assign ") == 0 && tokens.size() >= 3) ||
                    (command == "search" || command.find("search ") == 0)) {
                    
                    std::cout << "Enter multi-line value (type 'END' on a line by itself to finish):" << std::endl;
                    std::vector<std::string> lines;
                    lines.push_back(command);
                    
                    std::string line;
                    while (true) {
                        std::getline(std::cin, line);
                        if (line == "END") {
                            break;
                        }
                        lines.push_back(line);
                    }
                    
                    // Process the multi-line command
                    std::string full_command;
                    for (size_t i = 0; i < lines.size(); ++i) {
                        if (i > 0) {
                            full_command += "\n";
                        }
                        full_command += lines[i];
                    }
                    execute_command(full_command);
                } else {
                    execute_command(command);
                }
            } else {
                execute_command(command);
            }
        }
    }
};

int main() {
    try {
        IntegratedApp app;
        app.run();
    }
    catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
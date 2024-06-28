/*
 * Installation Instructions for Mathematicion
 *
 * Prerequisites:
 * 1. C++ Compiler (g++ or Visual Studio)
 * 2. CMake (if using a CMake project)
 * 3. vcpkg (for managing C++ libraries)
 * 4. JSON for Modern C++ library (nlohmann/json)
 *
 * Step 1: Install vcpkg
 * - Clone the vcpkg repository:
 *   git clone https://github.com/microsoft/vcpkg.git
 * - Navigate to the vcpkg directory:
 *   cd vcpkg
 * - Bootstrap vcpkg:
 *   .\bootstrap-vcpkg.bat (on Windows)
 *   ./bootstrap-vcpkg.sh (on Unix)
 * - Integrate vcpkg with your shell:
 *   .\vcpkg integrate install
 *
 * Step 2: Install JSON for Modern C++ library
 * - Use vcpkg to install the nlohmann-json package:
 *   .\vcpkg install nlohmann-json
 *
 * Step 3: Compile the Program
 * - Open a command prompt (cmd) or PowerShell.
 * - Navigate to the directory containing the source code (e.g., main.cpp).
 * - Compile the program using g++:
 *   g++ -ID:/vcpkgm/vcpkg/installed/x64-windows/include main.cpp -o Mathematicion.exe
 *   (Replace D:/vcpkgm/vcpkg/installed/x64-windows/include with the correct path to your vcpkg installation)
 * - If using MSVC (Visual Studio):
 *   - Open the Developer Command Prompt for Visual Studio.
 *   - Navigate to the directory containing the source code.
 *   - Compile the program using cl:
 *     cl /EHsc main.cpp /I D:/vcpkgm/vcpkg/installed/x64-windows/include /link /OUT:Mathematicion.exe
 *   (Replace D:/vcpkgm/vcpkg/installed/x64-windows/include with the correct path to your vcpkg installation)
 *
 * Step 4: Run the Program
 * - After successful compilation, run the executable:
 *   .\Mathematicion.exe
 *
 * Troubleshooting:
 * - Ensure all paths are correct and point to the appropriate directories.
 * - Ensure all dependencies are installed and accessible.
 * - Check for any compilation errors and resolve missing include paths or libraries.
 *
 * Example:
 * > mkdir config
 * > .\Mathematicion.exe
 * 
 * You should now be able to interact with the menu and perform various operations as described in the program.
 *
 * For further help and documentation, refer to the official documentation of the JSON for Modern C++ library and vcpkg.
 */
#include <iostream>
#include <string>
#include <set>
#include <unordered_map>
#include <memory>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <fstream>
#include "D:/vcpkgm/vcpkg/installed/x64-windows/include/nlohmann/json.hpp"
#include <filesystem>
//#include <nlohmann/json.hpp>

using json = nlohmann::json;

// A function to get the current timestamp in the desired format
std::string getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);

    std::stringstream ss;
    ss << std::put_time(std::gmtime(&in_time_t), "%Y-%m-%dT%H:%M:%SZ");
    return ss.str();
}

// Base class for PS (Property Set)
class PropertySet {
public:
    virtual void display() const = 0;
    virtual json to_json() const = 0;
    virtual void delete_property(const std::string& key) = 0;
    virtual ~PropertySet() = default;
};

// An example of a user-defined property set using JSON
class DynamicPropertySet : public PropertySet {
private:
    json properties;
public:
    DynamicPropertySet(const json& props) : properties(props) {}

    void display() const override {
        std::cout << properties.dump(4) << std::endl;
    }

    json to_json() const override {
        return properties;
    }

    void delete_property(const std::string& key) override {
        properties.erase(key);
    }
};

// Cooper class to encapsulate the structure
class Cooper {
private:
    std::string id;
    std::unique_ptr<PropertySet> propertySet;
    std::string timestamp;

    static std::set<std::string> idSet;

public:
    Cooper(std::string id, std::unique_ptr<PropertySet> ps)
        : id(std::move(id)), propertySet(std::move(ps)), timestamp(getCurrentTimestamp()) {
        if (idSet.find(this->id) != idSet.end()) {
            throw std::invalid_argument("ID already exists.");
        }
        idSet.insert(this->id);
    }

    const std::string& getId() const { return id; }
    const std::string& getTimestamp() const { return timestamp; }
    const PropertySet* getPropertySet() const { return propertySet.get(); }

    void display() const {
        std::cout << "ID: " << id << std::endl;
        std::cout << "Timestamp: " << timestamp << std::endl;
        std::cout << "Properties: ";
        propertySet->display();
    }

    static void resetIdSet() {
        idSet.clear();
    }

    static void updateIdSet(const std::set<std::string>& newIdSet) {
        idSet = newIdSet;
    }

    void save(const std::string& filename) const {
        json j;
        j["id"] = id;
        j["timestamp"] = timestamp;
        j["properties"] = propertySet->to_json();

        std::ofstream file(filename);
        if (file.is_open()) {
            file << j.dump(4);
        }
    }

    static Cooper load(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file for reading");
        }
        json j;
        file >> j;

        std::string id = j["id"];
        std::string timestamp = j["timestamp"];
        json properties = j["properties"];

        auto propertySet = std::make_unique<DynamicPropertySet>(properties);
        Cooper loadedCooper(id, std::move(propertySet));
        loadedCooper.timestamp = timestamp; // Ensure the timestamp is preserved
        return loadedCooper;
    }

    void updatePropertySet(const json& newProps) {
        propertySet = std::make_unique<DynamicPropertySet>(newProps);
    }

    void deleteProperty(const std::string& key) {
        propertySet->delete_property(key);
    }

    void changeId(const std::string& newId) {
        if (idSet.find(newId) != idSet.end()) {
            throw std::invalid_argument("ID already exists.");
        }
        idSet.erase(id);
        id = newId;
        idSet.insert(id);
    }
};

std::set<std::string> Cooper::idSet;

void displayMenu() {
    std::cout << "Menu:\n";
    std::cout << "1. Create new structure\n";
    std::cout << "2. Display structure\n";
    std::cout << "3. Update structure properties\n";
    std::cout << "4. Delete structure\n";
    std::cout << "5. Change structure ID\n";
    std::cout << "6. Save structure to file\n";
    std::cout << "7. Load structure from file\n";
    std::cout << "8. Delete a property from structure\n";
    std::cout << "9. Help documentation\n";
    std::cout << "10. Exit\n";
}

void helpDocumentation() {
    std::cout << "Help Documentation:\n";
    std::cout << "1. Create new structure: Allows you to create a new mathematical structure by entering properties interactively.\n";
    std::cout << "2. Display structure: Displays the details of a selected structure.\n";
    std::cout << "3. Update structure properties: Allows you to update the properties of an existing structure.\n";
    std::cout << "4. Delete structure: Deletes an existing structure from the system.\n";
    std::cout << "5. Change structure ID: Changes the ID of an existing structure, ensuring no duplicates.\n";
    std::cout << "6. Save structure to file: Saves the details of a selected structure to a JSON file.\n";
    std::cout << "7. Load structure from file: Loads a structure from a JSON file and adds it to the system.\n";
    std::cout << "8. Delete a property from structure: Deletes a specific property from an existing structure.\n";
    std::cout << "9. Help documentation: Displays this help documentation.\n";
    std::cout << "10. Exit: Exits the application.\n";
}

json getUserProperties() {
    json userProps;
    std::string key;
    std::string value;
    bool booleanValue;
    int intValue;

    std::cout << "Enter the properties for the structure. Type 'done' when finished." << std::endl;
    while (true) {
        std::cout << "Enter property name (or type 'done' to finish): ";
        std::getline(std::cin, key);
        if (key == "done") break;

        std::cout << "Enter property type (string, int, bool): ";
        std::string type;
        std::getline(std::cin, type);

        if (type == "string") {
            std::cout << "Enter string value (type 'END' to finish multi-line input): ";
            std::string line;
            value.clear();
            while (std::getline(std::cin, line)) {
                if (line == "END") break;
                value += line + "\n";
            }
            userProps[key] = value;
        } else if (type == "int") {
            std::cout << "Enter integer value: ";
            std::cin >> intValue;
            userProps[key] = intValue;
            std::cin.ignore(); // Ignore the newline character left in the input buffer
        } else if (type == "bool") {
            std::cout << "Enter boolean value (0 for false, 1 for true): ";
            std::cin >> booleanValue;
            userProps[key] = booleanValue;
            std::cin.ignore(); // Ignore the newline character left in the input buffer
        } else {
            std::cout << "Invalid type. Please enter 'string', 'int', or 'bool'." << std::endl;
        }
    }

    return userProps;
}

int main() {
    try {
        std::unordered_map<std::string, std::unique_ptr<Cooper>> cooperMap;
        int choice;
        std::string id;
        std::string filename;

        while (true) {
            displayMenu();
            std::cout << "Enter your choice: ";
            std::cin >> choice;
            std::cin.ignore(); // Ignore the newline character left in the input buffer

            switch (choice) {
                case 1: {
                    std::cout << "Enter structure ID: ";
                    std::getline(std::cin, id);
                    auto props = getUserProperties();
                    cooperMap[id] = std::make_unique<Cooper>(id, std::make_unique<DynamicPropertySet>(props));
                    break;
                }
                case 2: {
                    std::cout << "Enter structure ID to display: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        cooperMap[id]->display();
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 3: {
                    std::cout << "Enter structure ID to update: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        auto newProps = getUserProperties();
                        cooperMap[id]->updatePropertySet(newProps);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 4: {
                    std::cout << "Enter structure ID to delete: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        cooperMap.erase(id);
                        std::set<std::string> newIdSet;
                        for (const auto& pair : cooperMap) {
                            newIdSet.insert(pair.first);
                        }
                        Cooper::updateIdSet(newIdSet);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 5: {
                    std::cout << "Enter current structure ID: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        std::cout << "Enter new structure ID: ";
                        std::string newId;
                        std::getline(std::cin, newId);
                        cooperMap[id]->changeId(newId);
                        cooperMap[newId] = std::move(cooperMap[id]);
                        cooperMap.erase(id);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 6: {
                    std::cout << "Enter structure ID to save: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        std::cout << "Enter filename to save to: ";
                        std::getline(std::cin, filename);
                        cooperMap[id]->save("config/" + filename);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 7: {
                    std::cout << "Enter filename to load from: ";
                    std::getline(std::cin, filename);
                    Cooper loadedCooper = Cooper::load("config/" + filename);
                    std::string loadedId = loadedCooper.getId();
                    cooperMap[loadedId] = std::make_unique<Cooper>(std::move(loadedCooper));
                    break;
                }
                case 8: {
                    std::cout << "Enter structure ID: ";
                    std::getline(std::cin, id);
                    if (cooperMap.find(id) != cooperMap.end()) {
                        std::string propertyKey;
                        std::cout << "Enter property name to delete: ";
                        std::getline(std::cin, propertyKey);
                        cooperMap[id]->deleteProperty(propertyKey);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 9: {
                    helpDocumentation();
                    break;
                }
                case 10: {
                    std::cout << "Exiting program." << std::endl;
                    return 0;
                }
                default: {
                    std::cout << "Invalid choice. Please try again." << std::endl;
                }
            }
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}






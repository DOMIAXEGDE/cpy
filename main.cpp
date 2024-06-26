//#include <D:/vcpkgm/vcpkg/installed/x64-windows/include/nlohmann/json.hpp>
#include <iostream>
#include <string>
#include <set>
#include <unordered_map>
#include <memory>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <nlohmann/json.hpp>
#include <filesystem>

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
};

// Cooper class to encapsulate the structure
class Cooper {
private:
    int id;
    std::unique_ptr<PropertySet> propertySet;
    std::string timestamp;

    static std::set<int> idSet;

public:
    Cooper(int id, std::unique_ptr<PropertySet> ps)
        : id(id), propertySet(std::move(ps)), timestamp(getCurrentTimestamp()) {
        if (idSet.find(id) != idSet.end()) {
            throw std::invalid_argument("ID already exists.");
        }
        idSet.insert(id);
    }

    int getId() const { return id; }
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

    static void updateIdSet(const std::set<int>& newIdSet) {
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

        int id = j["id"];
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

    void changeId(int newId) {
        if (idSet.find(newId) != idSet.end()) {
            throw std::invalid_argument("ID already exists.");
        }
        idSet.erase(id);
        id = newId;
        idSet.insert(id);
    }
};

std::set<int> Cooper::idSet;

void displayMenu() {
    std::cout << "Menu:\n";
    std::cout << "1. Create new structure\n";
    std::cout << "2. Display structure\n";
    std::cout << "3. Update structure properties\n";
    std::cout << "4. Delete structure\n";
    std::cout << "5. Change structure ID\n";
    std::cout << "6. Save structure to file\n";
    std::cout << "7. Load structure from file\n";
    std::cout << "8. Help documentation\n";
    std::cout << "9. Exit\n";
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
    std::cout << "8. Help documentation: Displays this help documentation.\n";
    std::cout << "9. Exit: Exits the application.\n";
}

json getUserProperties() {
    json userProps;
    std::string key;
    std::string value;
    bool booleanValue;
    int intValue;

    std::cout << "Enter the properties for the structure. Type 'done' when finished." << std::endl;
    while (true) {
        std::cout << "Enter property name (or type 'done' to finish)_";
        std::cin >> key;
        if (key == "done") break;

        std::cout << "Enter property type (string, int, bool): ";
        std::string type;
        std::cin >> type;

        if (type == "string") {
            std::cout << "Enter string value: ";
            std::cin >> value;
            userProps[key] = value;
        } else if (type == "int") {
            std::cout << "Enter integer value: ";
            std::cin >> intValue;
            userProps[key] = intValue;
        } else if (type == "bool") {
            std::cout << "Enter boolean value (0 for false, 1 for true): ";
            std::cin >> booleanValue;
            userProps[key] = booleanValue;
        } else {
            std::cout << "Invalid type. Please enter 'string', 'int', or 'bool'." << std::endl;
        }
    }

    return userProps;
}

int main() {
    try {
        std::unordered_map<int, std::unique_ptr<Cooper>> cooperMap;
        int choice;
        int id;
        std::string filename;

        while (true) {
            displayMenu();
            std::cout << "Enter your choice: ";
            std::cin >> choice;

            switch (choice) {
                case 1: {
                    std::cout << "Enter structure ID: ";
                    std::cin >> id;
                    auto props = getUserProperties();
                    cooperMap[id] = std::make_unique<Cooper>(id, std::make_unique<DynamicPropertySet>(props));
                    break;
                }
                case 2: {
                    std::cout << "Enter structure ID to display: ";
                    std::cin >> id;
                    if (cooperMap.find(id) != cooperMap.end()) {
                        cooperMap[id]->display();
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 3: {
                    std::cout << "Enter structure ID to update: ";
                    std::cin >> id;
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
                    std::cin >> id;
                    if (cooperMap.find(id) != cooperMap.end()) {
                        cooperMap.erase(id);
                        std::set<int> newIdSet;
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
                    std::cin >> id;
                    if (cooperMap.find(id) != cooperMap.end()) {
                        std::cout << "Enter new structure ID: ";
                        int newId;
                        std::cin >> newId;
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
                    std::cin >> id;
                    if (cooperMap.find(id) != cooperMap.end()) {
                        std::cout << "Enter filename to save to: ";
                        std::cin >> filename;
                        cooperMap[id]->save("config/" + filename);
                    } else {
                        std::cout << "Structure ID not found." << std::endl;
                    }
                    break;
                }
                case 7: {
                    std::cout << "Enter filename to load from: ";
                    std::cin >> filename;
                    Cooper loadedCooper = Cooper::load("config/" + filename);
                    int loadedId = loadedCooper.getId();
                    cooperMap[loadedId] = std::make_unique<Cooper>(std::move(loadedCooper));
                    break;
                }
                case 8: {
                    helpDocumentation();
                    break;
                }
                case 9: {
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



local MemorySlotManager = {}
MemorySlotManager.__index = MemorySlotManager

function MemorySlotManager:new(memory_dir, no_duplicates)
    local obj = {
        memory_dir = memory_dir or "memory_slots",
        no_duplicates = no_duplicates or false
    }
    setmetatable(obj, self)

    if not fs.exists(obj.memory_dir) then
        fs.makeDir(obj.memory_dir)
    end

    return obj
end

function MemorySlotManager:write_memory_slot(file_number, slot_number, value)
    local file_path = fs.combine(self.memory_dir, tostring(file_number) .. ".txt")
    local file = fs.open(file_path, 'a')
    file.writeLine(slot_number .. "\t\t\t\t" .. value)
    file.close()
end

function MemorySlotManager:read_memory_slot(file_number, slot_number)
    local file_path = fs.combine(self.memory_dir, tostring(file_number) .. ".txt")
    if not fs.exists(file_path) then
        error("File " .. file_number .. ".txt does not exist.")
    end

    local file = fs.open(file_path, 'r')
    while true do
        local line = file.readLine()
        if not line then break end
        local slot, value = line:match("^(%d+)%s+(.+)$")
        if tonumber(slot) == slot_number then
            file.close()
            return value
        end
    end
    file.close()
    error("Slot " .. slot_number .. " not found in file " .. file_number .. ".txt.")
end

function MemorySlotManager:get_last_slot_number(file_number)
    local file_path = fs.combine(self.memory_dir, tostring(file_number) .. ".txt")
    if not fs.exists(file_path) then
        error("File " .. file_number .. ".txt does not exist.")
    end

    local last_slot_number = nil
    local file = fs.open(file_path, 'r')
    while true do
        local line = file.readLine()
        if not line then break end
        local slot = line:match("^(%d+)%s")
        last_slot_number = tonumber(slot)
    end
    file.close()

    if not last_slot_number then
        error("No slots found in file " .. file_number .. ".txt.")
    end
    return last_slot_number
end

function MemorySlotManager:check_duplicate_assignment(file_number, slot_number, value)
    local file_path = fs.combine(self.memory_dir, tostring(file_number) .. ".txt")
    if not fs.exists(file_path) then
        return false
    end

    local file = fs.open(file_path, 'r')
    while true do
        local line = file.readLine()
        if not line then break end
        local slot, existing_value = line:match("^(%d+)%s+(.+)$")
        if tonumber(slot) == slot_number and existing_value == value then
            file.close()
            return true
        end
    end
    file.close()
    return false
end

function MemorySlotManager:check_value_exists(value)
    for _, file_name in ipairs(fs.list(self.memory_dir)) do
        local file_path = fs.combine(self.memory_dir, file_name)
        local file = fs.open(file_path, 'r')
        while true do
            local line = file.readLine()
            if not line then break end
            local existing_value = line:match("^%d+%s+(.+)$")
            if existing_value == value then
                file.close()
                return tonumber(file_name:match("^(%d+)%.txt$"))
            end
        end
        file.close()
    end
    return nil
end

function MemorySlotManager:execute_sequence(sequence)
    local tokens = {}
    for token in string.gmatch(sequence, "%S+") do
        table.insert(tokens, token)
    end

    if tokens[1] == 'assign' then
        local current_file = tonumber(tokens[2])
        local slot_number = tonumber(tokens[3])
        local value_or_reference = tokens[4]

        local value
        if value_or_reference:find('%.') then
            local ref_file, ref_slot = value_or_reference:match("(%d+)%.(%d+)")
            value = self:read_memory_slot(tonumber(ref_file), tonumber(ref_slot))
        else
            value = value_or_reference
        end

        local existing_file = self.no_duplicates and self:check_value_exists(value) or nil
        if existing_file then
            print("Error: Value '" .. value .. "' already exists in file " .. existing_file .. ".")
        elseif self:check_duplicate_assignment(current_file, slot_number, value) then
            print("Duplicate assignment detected: " .. value .. " is already assigned to slot " .. slot_number .. " in file " .. current_file .. ".")
        else
            self:write_memory_slot(current_file, slot_number, value)
        end
    elseif tokens[1]:find('%.') then
        local file_number, slot_number = tokens[1]:match("(%d+)%.(%d+)")
        local value = self:read_memory_slot(tonumber(file_number), tonumber(slot_number))
        print(value)
    elseif tokens[1] == 'last_slot' then
        local file_number = tonumber(tokens[2])
        local last_slot_number = self:get_last_slot_number(file_number)
        print("The last slot number in file " .. file_number .. ".txt is " .. last_slot_number)
    elseif tokens[1] == 'check_duplicate' then
        local file_number = tonumber(tokens[2])
        local slot_number = tonumber(tokens[3])
        local value = tokens[4]
        if self:check_duplicate_assignment(file_number, slot_number, value) then
            print("Duplicate: " .. value .. " is already assigned to slot " .. slot_number .. " in file " .. file_number .. ".")
        else
            print("No duplicate found: " .. value .. " is not assigned to slot " .. slot_number .. " in file " .. file_number .. ".")
		end
    elseif tokens[1] == 'help_command' then
        self:print_help()
    else
        print("Invalid sequence")
    end
end

function MemorySlotManager:print_help()
    local help_text = [[
Memory Slot Language Help Documentation
=======================================
        
Command Structure:
- assign <current_file> <slot_number> <reference_or_value>
    Assigns the value from the reference (another slot) or a direct value to the specified slot in the current file.
    Examples: 
        assign 3 1 1.1    # Assigns the value from slot 1 in file 1 to slot 1 in file 3
        assign 3 1 hello  # Assigns the value 'hello' directly to slot 1 in file 3
        
- <file_number>.<slot_number>
    Retrieves and prints the value from the specified slot in the specified file.
    Example: 3.1
        
- last_slot <file_number>
    Displays the last memory slot number in the specified file.
    Example: last_slot 3

- check_duplicate <file_number> <slot_number> <value>
    Checks if the specified value is already assigned to the given slot in the specified file.
    Example: check_duplicate 1 2 hello

- help_command
    Prints this help documentation.
        
Usage Examples:
1. Write values to memory slots:
    write_memory_slot(1, 1, "hello")
    write_memory_slot(2, 1, "world")
        
2. Assign and retrieve values dynamically:
    assign 3 1 1.1  # Assigns the value from slot 1 in file 1 to slot 1 in file 3
    3.1            # Retrieves and prints the value from slot 1 in file 3
        
3. Assign direct values:
    assign 1 2 new_value  # Directly assigns 'new_value' to slot 2 in file 1
        
4. Display last slot number:
    last_slot 1  # Displays the last slot number in file 1

5. Check for duplicate assignments:
    check_duplicate 1 2 hello  # Checks if 'hello' is already assigned to slot 2 in file 1

6. Check if value exists in any file:
    assign <current_file> <slot_number> <value>
    This will prevent assigning if value exists in any slot of any file.
        
Notes:
- Ensure the file paths are correct and the files exist.
- Use integer values for file numbers and slot numbers.
- The values assigned and retrieved can be any string.
]]
    print(help_text)
end

local function main()
    print("Allow duplicate values in memory slots? (yes/no): ")
    local allow_duplicates = read():lower() ~= 'no'
    local manager = MemorySlotManager:new("memory_slots", not allow_duplicates)

    while true do
        print("Enter help_command or a command (or 'exit' to quit): ")
        local user_input = read()
        if user_input:lower() == 'exit' then
            break
        end
        pcall(function() manager:execute_sequence(user_input) end)
    end
end

main()

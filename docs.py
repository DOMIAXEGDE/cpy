import os

def list_text_files():
    extensions = ['.asm']
    # Filter files in the current directory based on specified extensions
    return [f for f in os.listdir() if any(f.endswith(ext) for ext in extensions)]

def read_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e)

def sort_files(files):
    # Extract numbers from filenames and sort based on those numbers
    def extract_number(file):
        try:
            return int(file.split('.')[0])
        except ValueError:
            return float('inf')  # In case of unexpected filename format, put it at the end

    return sorted(files, key=extract_number)

def create_txt(files):
    # Create a text file and write contents of each listed file
    with open("assemblyOS_documentation.txt", "w", encoding='utf-8') as txt_file:
        for file in files:
            txt_file.write(f"{file}\n;Content of {file}\n")
            txt_file.write(read_file_content(file))
            txt_file.write("\n\n")

if __name__ == "__main__":
    text_files = list_text_files()
    sorted_text_files = sort_files(text_files)

    create_txt(sorted_text_files)  # Generate the text file

    print("Documentation updated: Created 'assemblyOS_documentation.txt'")

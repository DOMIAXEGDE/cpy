#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to generate the files with different extensions
void generate_files(int n, int k, char a[]) {
    // Calculate the number of combinations
    unsigned long long nbr_comb = 1;
    for (int i = 0; i < n; i++) {
        nbr_comb *= (k + 1);
    }
    unsigned long long id = 0;

    // Define the array of file extensions
    const char *extensions[] = {
        // Document Formats
        ".txt", ".doc", ".docx", ".pdf", ".rtf", ".odt", ".tex", ".wpd", ".pages", ".numbers",
        ".key", ".md", ".markdown", ".log", ".csv", ".tsv", ".xls", ".xlsx", ".ppt", ".pptx",
        ".pps", ".ppsx", ".pub", ".mobi", ".epub",

        // Image Formats
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".webp", ".ico",
        ".raw", ".psd", ".ai", ".eps", ".indd", ".heic", ".jfif", ".pjpeg", ".pjp", ".svgz",
        ".apng",

        // Audio Formats
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".aiff", ".alac", ".mid",
        ".midi", ".opus", ".amr", ".pcm", ".caf", ".dsd", ".vqf",

        // Video Formats
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v",
        ".3gp", ".3g2", ".ts", ".mts", ".m2ts", ".rmvb", ".vob", ".divx", ".xvid", ".ogv",
        ".swf", ".f4v", ".mxf", ".rm",

        // Programming and Markup Languages
        ".c", ".cpp", ".h", ".hpp", ".cs", ".java", ".py", ".js", ".ts", ".rb", ".go",
        ".php", ".swift", ".kt", ".rs", ".scala", ".pl", ".sh", ".bat", ".ps1", ".lua",
        ".sql", ".html", ".css", ".xml", ".yml", ".yaml", ".ini", ".make", ".gradle",
        ".pom", ".dockerfile", ".tsx", ".jsx",

        // Archives and Compressed Files
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".deb",
        ".rpm", ".pkg", ".cab", ".msi", ".arj", ".ace", ".lzh", ".alz", ".z", ".cpio",
        ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz",

        // Executables and Scripts
        ".exe", ".dll", ".so", ".dylib", ".app", ".msi", ".bat", ".cmd", ".sh", ".bash",
        ".zsh", ".ksh", ".csh", ".fish", ".pyw", ".pl", ".pm", ".ps1", ".vbs", ".jar",
        ".apk", ".appx", ".msix",

        // Fonts
        ".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".fnt", ".pfb", ".pfm", ".sfd",

        // Database Files
        ".db", ".mdb", ".accdb", ".sqlite", ".dbf", ".tar", ".bak", ".dump",

        // Miscellaneous
        ".img", ".bin", ".cue", ".nrg", ".vcd", ".mdf", ".vhd", ".vdi", ".qcow2",
        ".temp", ".lock", ".pid", ".swp", ".swo", ".swn", ".dmp", ".sys", ".drv",
        ".icns", ".lnk", ".url", ".torrent", ".crdownload",

        // 3D Models and CAD
        ".obj", ".fbx", ".3ds", ".dae", ".blend", ".stl", ".iges", ".step", ".skp",
        ".max", ".c4d", ".dwg", ".dxf",

        // eBook Formats
        ".azw", ".azw3", ".kf8", ".ibooks",

        // Web Files
        ".htm", ".asp", ".aspx", ".jsp", ".twig", ".erb", ".vue", ".less", ".scss", ".sass",
        ".rss", ".atom",

        // Configuration Files
        ".conf", ".config", ".toml", ".env", ".properties", ".htaccess",

        // LaTeX
        ".bib", ".cls", ".sty", ".dtx", ".ins",

        // Virtualization
        ".vmdk", ".vdi", ".vhdx", ".ova", ".ovf",

        // Design and Multimedia
        ".sketch", ".fig", ".xd",

        // Scientific Data
        ".ods", ".sav", ".rda", ".mat", ".h5", ".hdf5", ".nc",

        // Other Common Extensions
        ".old", ".cache", ".dat", ".db3", ".sqlite3", ".plist", ".war", ".ear"
    };
    
	int num_extensions = sizeof(extensions) / sizeof(extensions[0]);

	for (unsigned long long row = 0; row < nbr_comb; row++) {
		// Iterate over each file extension type
		for (int ext_idx = 0; ext_idx < num_extensions; ext_idx++) {
			// Iterate over all configurations for this file extension
			for (unsigned long long config = 0; config < nbr_comb; config++) { // This ensures multiple configurations
				char filename[700];
				const char *ext = extensions[ext_idx];
				sprintf(filename, "production/fs%d_%llu_config%llu%s", n, id, config, ext);
				
				FILE *p = fopen(filename, "w");
				if (p == NULL) {
					fprintf(stderr, "Error creating file %s\n", filename);
					exit(1);
				}
				
				// Generate the content of the file for this configuration
				unsigned long long temp_row = row;
				for (int col = n - 1; col >= 0; col--) {
					int cell = temp_row % (k + 1);
					fprintf(p, "%c", a[cell]);
					temp_row /= (k + 1);
				}
				fprintf(p, "\n"); // Optional: Add a newline for readability
				fclose(p);
				id++; // Increment the unique identifier after each file is created
			}
		}
	}
}

/*
// Function to generate the compile script for Windows (only for .cpp files)
void generate_compile_script(int n, int k) {
    FILE *script = fopen("production/compile.bat", "w");
    fprintf(script, "@echo off\n\n");
    fprintf(script, "setlocal enabledelayedexpansion\n\n");
    fprintf(script, "set DIRECTORY=.\n");
    fprintf(script, "set EXE_DIR=executables\n\n");
    fprintf(script, "if not exist %%EXE_DIR%% mkdir %%EXE_DIR%%\n\n");

    // Calculate the number of combinations
    unsigned long long nbr_comb = 1;
    for (int i = 0; i < n; i++) {
        nbr_comb *= (k + 1);
    }

    unsigned long long id = 0;

    for (unsigned long long row = 0; row < nbr_comb; row++) {
        const char *ext = ".cpp";
        fprintf(script, "g++ %%DIRECTORY%%\\fs%d_%llu%s -o %%EXE_DIR%%\\fs%d_%llu.exe\n", n, id, ext, n, id);
        id++;
    }
    fclose(script);
}

// Function to generate the executor script for Windows (only for .exe files)
void generate_executor_script(int n, int k) {
    FILE *executor = fopen("production/executor.bat", "w");
    fprintf(executor, "@echo off\n\n");
    fprintf(executor, "set EXE_DIR=executables\n\n");

    // Calculate the number of combinations
    unsigned long long nbr_comb = 1;
    for (int i = 0; i < n; i++) {
        nbr_comb *= (k + 1);
    }

    unsigned long long id = 0;

    for (unsigned long long row = 0; row < nbr_comb; row++) {
        fprintf(executor, "%%EXE_DIR%%\\fs%d_%llu.exe\n", n, id);
        id++;
    }
    fclose(executor);
}
*/

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <n value> <character set size (max 100)>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    int char_set_size = atoi(argv[2]);
    if (char_set_size > 100) {
        printf("Character set size cannot exceed 100.\n");
        return 1;
    }
    int k = char_set_size - 1;

    // Define the character set dynamically based on the input size
    char a[100];
    // Example character set (you can customize this as needed)
    char full_char_set[100] = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\n', '\t',
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+',
        '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', '\'', '<', '>',
        ',', '.', '?', '/', '`', '~'
    };
    // Copy the required number of characters to 'a'
    memcpy(a, full_char_set, char_set_size * sizeof(char));

    // Create the production directories
    system("mkdir production");
    system("mkdir production\\executables");

    // Generate the files and scripts
    generate_files(n, k, a);
    //generate_compile_script(n, k);
    //generate_executor_script(n, k);

    return 0;
}



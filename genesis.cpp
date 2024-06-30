#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// Function to generate the C++ source files
void generate_files(int n, int k, char a[]) {
    int nbr_comb = pow(k + 1, n);
    unsigned long long id = 0;
    for (int row = 0; row < nbr_comb; row++) {
        char filename[500];
        sprintf(filename, "production/fs%d_%llu.cpp", n, id);
        FILE *p = fopen(filename, "w");
        id++;
        for (int col = n - 1; col >= 0; col--) {
            int rdiv = pow(k + 1, col);
            int cell = (row / rdiv) % (k + 1);
            fprintf(p, "%c", a[cell]);
        }
        fclose(p);
    }
}

// Function to generate the compile script for Windows
void generate_compile_script(int n, int k) {
    FILE *script = fopen("production/compile.bat", "w");
    fprintf(script, "@echo off\n\n");
    fprintf(script, "setlocal enabledelayedexpansion\n\n");
    fprintf(script, "set DIRECTORY=.\n");
    fprintf(script, "set EXE_DIR=executables\n\n");
    fprintf(script, "if not exist %%EXE_DIR%% mkdir %%EXE_DIR%%\n\n");

    int nbr_comb = pow(k + 1, n);
    for (int id = 0; id < nbr_comb; id++) {
        fprintf(script, "g++ %%DIRECTORY%%\\fs%d_%d.cpp -o %%EXE_DIR%%\\fs%d_%d.exe\n", n, id, n, id);
    }
    fclose(script);
}

// Function to generate the executor script for Windows
void generate_executor_script(int n, int k) {
    FILE *executor = fopen("production/executor.bat", "w");
    fprintf(executor, "@echo off\n\n");
    fprintf(executor, "set EXE_DIR=executables\n\n");

    int nbr_comb = pow(k + 1, n);
    for (int id = 0; id < nbr_comb; id++) {
        fprintf(executor, "%%EXE_DIR%%\\fs%d_%d.exe\n", n, id);
    }
    fclose(executor);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <n value> <character set size>\n", argv[0]);
        return 1;
    }

    int noc = atoi(argv[1]);
    int k = 99; // Since we have 100 characters in total

    // Define the character set including 100 unique characters
    char a[100] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\n', '\t', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', 
                    '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', '\'', '<', '>', ',', '.', '?', '/', '`', '~'};

    // Create the production directory if it doesn't exist
    system("mkdir production");

    // Create the executables subdirectory if it doesn't exist
    system("mkdir production\\executables");

    generate_files(noc, k, a);
    generate_compile_script(noc, k);
    generate_executor_script(noc, k);

    return 0;
}

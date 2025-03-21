//Written from 14:50 20/03/2025
//cLLM.c : C Large Language model

/*

setup(){
Here's a step-by-step guide to install MSYS2 on your system:

1. Download MSYS2: Go to the [official MSYS2 website](https://www.msys2.org/) and download the installer.

2. Run the Installer: Execute the downloaded installer and choose a suitable installation directory (e.g., `C:\msys64`). Avoid paths with spaces.

3. Update MSYS2: Open the MSYS2 MinGW 64-bit shell and run the following commands to update the package database and core system:
   ```bash
   pacman -Syu
   pacman -Su
   ```

4. Install the GCC Toolchain: Run the following command to install the necessary development tools:
   ```bash
   pacman -S --needed base-devel mingw-w64-x86_64-toolchain
   ```

5. Add to PATH: Add the `C:\msys64\mingw64\bin` directory to your system's PATH environment variable. This allows you to use GCC from PowerShell. You can do this by running the following command in PowerShell:
   ```powershell
   $env:Path += ";C:\msys64\mingw64\bin"
   ```

6. Verify Installation: Open PowerShell and run `gcc --version`. You should see the GCC version information.

For more detailed instructions, you can refer to the [MSYS2 installation guide](https://www.msys2.org/wiki/MSYS2-installation/).

Let me know if you need any further assistance!
}

-::	Prompt Engineered by Dominic Alexander Cooper at 19:35 09/03/2025
-::	cd C:/Users/dacoo/Documents/C
-::	gcc -o 1 1.c
-::	.\1.exe
*/

/*

setup(){
Here's a step-by-step guide to install MSYS2 on your system:

1. Download MSYS2: Go to the [official MSYS2 website](https://www.msys2.org/) and download the installer.

2. Run the Installer: Execute the downloaded installer and choose a suitable installation directory (e.g., `C:\msys64`). Avoid paths with spaces.

3. Update MSYS2: Open the MSYS2 MinGW 64-bit shell and run the following commands to update the package database and core system:
   ```bash
   pacman -Syu
   pacman -Su
   ```

4. Install the GCC Toolchain: Run the following command to install the necessary development tools:
   ```bash
   pacman -S --needed base-devel mingw-w64-x86_64-toolchain
   ```

5. Add to PATH: Add the `C:\msys64\mingw64\bin` directory to your system's PATH environment variable. This allows you to use GCC from PowerShell. You can do this by running the following command in PowerShell:
   ```powershell
   $env:Path += ";C:\msys64\mingw64\bin"
   ```

6. Verify Installation: Open PowerShell and run `gcc --version`. You should see the GCC version information.

For more detailed instructions, you can refer to the [MSYS2 installation guide](https://www.msys2.org/wiki/MSYS2-installation/).

Let me know if you need any further assistance!
}

-::	Prompt Engineered by Dominic Alexander Cooper at 22:23 09/03/2025
-::	cd C:/Users/dacoo/Documents/C
-::	gcc -o CLLM cLLM.c
-::	.\CLLM.exe
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main(){

	FILE *p; p = fopen("fs.txt", "w");
	char alphabet[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','\\','|',',','<','.','>','/','?',';',':','\'','@','#','~','[','{',']','}','`','!','"','$','%','^','&','*','(',')','-','_','=','+'};
	int k = strlen(alphabet) - 1;
	int cardinality = k + 1;
	printf("alphabet cardinality is : %d\n", (k + 1));
	int noc;
	scanf("%d", &noc);
	int n = noc;
	printf("Per file character cardinality is : %d\n", n);
	int row, cell, col, rdiv, id;
	id = 0;
	int nbr_comb = pow(cardinality, n);

	for(row = 0; row < nbr_comb; row++){

		id++; fprintf(p, "%d\t(){\n\t", id);

		for(col = n - 1; col >= 0; col--){

			rdiv = pow(cardinality, col);
			cell = (row/rdiv) % cardinality;
			fprintf(p, "%c", alphabet[cell]);

		}

		fprintf(p, "\n}[]\n\n");

	}

	fclose(p);
	return 0;

}
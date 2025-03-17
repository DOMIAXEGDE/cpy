#!/usr/bin/env python3
"""
Event Sequencer - Command Matrix System
---------------------------------------
A visual programming environment for managing and executing commands organized in a matrix.
The system supports navigation through keyboard, mouse, or game controller,
with commands stored in a grid-based layout for easy access and execution.

Author: Original code provided by user, enhanced with improvements
Version: 1.0
Date: 2025-03-17
"""

import pygame
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import pickle
import importlib
from datetime import datetime
import random
import math
import sys
import subprocess
import platform
import webbrowser

# Dictionary to store command parameters and values
command_dict = {}
# Session data for persistence
session_data = {
    "last_matrix": "Command_Template.txt",
    "last_position": (0, 0),
    "command_history": []
}

def install_dependencies():
    """
    Install all required dependencies for the Event Sequencer using pip.
    
    This function:
    1. Installs Python packages via pip
    2. Checks for Ghostscript installation (needed for PS file conversion)
    3. Provides system-specific instructions for installing Ghostscript
    
    Returns:
        bool: True if all dependencies were installed, False otherwise
    """
    try:
        import sys
        import subprocess
        import time
        import platform
        
        # List of all dependencies to install
        dependencies = [
            "pygame",
            "pillow",  # PIL
            "numpy",
            "matplotlib",
            "requests",
            "beautifulsoup4",  # bs4
            "pyautogui",
            "keyboard",
            "qiskit",
            "schemdraw",
            "plotly",
            "pyqt5",
            "psutil",
            "schedule"
        ]
        
        print("==========================================")
        print("Installing Event Sequencer Dependencies")
        print("==========================================")
        
        # Count for progress tracking
        total = len(dependencies)
        successful = 0
        failed = []
        
        for i, package in enumerate(dependencies):
            progress = (i / total) * 100
            print(f"[{progress:.1f}%] Installing {package}...")
            
            try:
                # Run pip install command
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                successful += 1
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                failed.append(package)
            except Exception as e:
                print(f"❌ Error installing {package}: {e}")
                failed.append(package)
            
            # Add a small delay to avoid overwhelming output
            time.sleep(0.5)
        
        # Check for Ghostscript
        print("\nChecking for Ghostscript (needed for PS file conversion)...")
        
        ghostscript_found = False
        try:
            # Try to find ghostscript using subprocess
            try:
                # Try Windows command
                subprocess.run(["gswin64c", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                ghostscript_found = True
            except FileNotFoundError:
                try:
                    # Try standard command (for Unix/macOS)
                    subprocess.run(["gs", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                    ghostscript_found = True
                except FileNotFoundError:
                    ghostscript_found = False
        except Exception:
            ghostscript_found = False
            
        if not ghostscript_found:
            print("❌ Ghostscript not found in PATH")
            
            # Ask if user wants to install Ghostscript
            install_gs = input("Would you like to try installing Ghostscript now? (y/n): ")
            
            if install_gs.lower() == 'y':
                system = platform.system()
                
                if system == "Windows":
                    print("\nFor Windows, you need to install Ghostscript manually:")
                    print("1. Download from: https://ghostscript.com/releases/gsdnld.html")
                    print("2. Run the installer and follow the instructions")
                    print("3. Make sure to add Ghostscript to your PATH")
                    
                    # Open download page
                    try:
                        import webbrowser
                        webbrowser.open("https://ghostscript.com/releases/gsdnld.html")
                    except:
                        pass
                    
                elif system == "Darwin":  # macOS
                    print("\nAttempting to install Ghostscript via Homebrew...")
                    try:
                        # Check if Homebrew is installed
                        subprocess.run(["brew", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                        
                        # Install Ghostscript
                        subprocess.run(["brew", "install", "ghostscript"], check=True)
                        print("✅ Ghostscript installed successfully via Homebrew")
                    except Exception as e:
                        print(f"❌ Homebrew installation failed: {e}")
                        print("\nPlease install Homebrew from https://brew.sh/")
                        print("Then run: brew install ghostscript")
                
                elif system == "Linux":
                    distro = ""
                    try:
                        # Try to detect Linux distribution
                        with open("/etc/os-release") as f:
                            lines = f.readlines()
                            for line in lines:
                                if line.startswith("ID="):
                                    distro = line.split("=")[1].strip().replace('"', '')
                                    break
                    except:
                        pass
                    
                    if distro in ["ubuntu", "debian", "linuxmint"]:
                        print(f"\nDetected {distro}. Attempting to install Ghostscript...")
                        try:
                            subprocess.run(["sudo", "apt-get", "update"], check=True)
                            subprocess.run(["sudo", "apt-get", "install", "-y", "ghostscript"], check=True)
                            print("✅ Ghostscript installed successfully")
                        except Exception as e:
                            print(f"❌ Installation failed: {e}")
                    elif distro in ["fedora", "rhel", "centos"]:
                        print(f"\nDetected {distro}. Attempting to install Ghostscript...")
                        try:
                            subprocess.run(["sudo", "dnf", "install", "-y", "ghostscript"], check=True)
                            print("✅ Ghostscript installed successfully")
                        except Exception as e:
                            print(f"❌ Installation failed: {e}")
                    else:
                        print("\nUnsupported Linux distribution or couldn't detect distribution.")
                        print("Please install Ghostscript using your distribution's package manager:")
                        print("- For Debian/Ubuntu: sudo apt-get install ghostscript")
                        print("- For Fedora/RHEL: sudo dnf install ghostscript")
                        print("- For Arch Linux: sudo pacman -S ghostscript")
                
                # Check if install was successful
                print("\nVerifying Ghostscript installation...")
                try:
                    result = False
                    try:
                        subprocess.run(["gswin64c", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                        result = True
                    except FileNotFoundError:
                        try:
                            subprocess.run(["gs", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                            result = True
                        except FileNotFoundError:
                            result = False
                    
                    if result:
                        print("✅ Ghostscript installed and accessible")
                    else:
                        print("❌ Ghostscript not found in PATH after installation")
                        print("Please restart your terminal/console after installation completes")
                except Exception:
                    print("❌ Could not verify Ghostscript installation")
            else:
                print("\nSkipping Ghostscript installation. PS to PNG conversion will use fallback method.")
        else:
            print("✅ Ghostscript is installed and accessible")
        
        # Summary
        print("\n==========================================")
        print(f"Installation Summary: {successful}/{total} packages installed successfully")
        
        if failed:
            print("\nThe following packages could not be installed automatically:")
            for package in failed:
                print(f"  - {package}")
            print("\nYou may need to install them manually or check for specific requirements.")
            print("For example: pip install package-name")
            
            # Offer some common troubleshooting advice
            print("\nTroubleshooting tips:")
            print("1. Make sure you have pip installed and updated")
            print("2. Some packages may require additional system dependencies")
            print("3. Try installing with: pip install package-name --user")
            
            return False
        else:
            print("\nAll dependencies installed successfully! The Event Sequencer is ready to run.")
            return True
    except Exception as e:
        print(f"Error during dependency installation: {e}")
        return False

def check_ghostscript():
    """
    Check if Ghostscript is installed and provide installation instructions if not.
    
    Ghostscript is required for PS to PNG conversion functionality.
    This function will identify the user's OS and provide appropriate installation instructions.
    """
    import subprocess
    import platform
    import sys
    
    print("\nChecking for Ghostscript installation...")
    
    ghostscript_found = False
    version_info = "Unknown"
    
    try:
        # Try Windows command first
        try:
            result = subprocess.run(["gswin64c", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                ghostscript_found = True
                version_info = result.stdout.split("\n")[0]
        except FileNotFoundError:
            # Try standard command (for Unix/macOS)
            try:
                result = subprocess.run(["gs", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    ghostscript_found = True
                    version_info = result.stdout.split("\n")[0]
            except FileNotFoundError:
                ghostscript_found = False
    except Exception as e:
        print(f"Error checking Ghostscript: {e}")
    
    if ghostscript_found:
        print(f"✅ Ghostscript is installed: {version_info}")
        print("PS to PNG conversion should work correctly.")
    else:
        system = platform.system()
        print("❌ Ghostscript is not installed or not in your PATH.")
        print("\nGhostscript is required for converting PS files to PNG.")
        print(f"\nInstallation instructions for {system}:")
        
        if system == "Windows":
            print("1. Download Ghostscript from: https://ghostscript.com/releases/gsdnld.html")
            print("2. Run the installer and follow the prompts.")
            print("3. Important: Make sure to check the option to add Ghostscript to your system PATH.")
            print("4. Restart your terminal/command prompt after installation.")
            
            # Ask if user wants to open the download page
            open_page = input("\nWould you like to open the download page now? (y/n): ")
            if open_page.lower() == 'y':
                import webbrowser
                webbrowser.open("https://ghostscript.com/releases/gsdnld.html")
                
        elif system == "Darwin":  # macOS
            print("1. The easiest way to install Ghostscript on macOS is with Homebrew:")
            print("   a. First install Homebrew if you don't have it: https://brew.sh/")
            print("   b. Then run: brew install ghostscript")
            print("2. Alternatively, you can download from: https://pages.uoregon.edu/koch/")
            
        elif system == "Linux":
            print("Install using your distribution's package manager:")
            print("- For Debian/Ubuntu: sudo apt-get install ghostscript")
            print("- For Fedora/RHEL: sudo dnf install ghostscript")
            print("- For Arch Linux: sudo pacman -S ghostscript")
            print("- For openSUSE: sudo zypper install ghostscript")
            
        else:
            print("Please search for Ghostscript installation instructions for your operating system.")
        
        print("\nOnce installed, you may need to restart your terminal or computer.")
        print("Alternative: You can use other tools to convert PS files to PNG before using this program.")

def alt_convert_ps_to_png(ps_path, png_path):
    """
    Alternative method to convert PS to PNG without Ghostscript using pygame.
    
    Creates a placeholder image when Ghostscript is not available.
    
    Args:
        ps_path (str): Path to the source PS file
        png_path (str): Path to save the converted PNG file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Method 1: Try using a temporary PDF conversion if reportlab is available
        try:
            from reportlab.graphics import renderPM
            from reportlab.graphics.shapes import Drawing
            
            print(f"Converting {ps_path} to {png_path} using alternate method...")
            
            # Create a blank image
            width, height = 500, 500  # Default size
            
            # Read some content from the PS file to create a representation
            with open(ps_path, 'r') as ps_file:
                ps_content = ps_file.read(1000)  # Read first 1000 chars to analyze
            
            # Try to extract size from PS file
            import re
            bounds_match = re.search(r'%%BoundingBox:\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', ps_content)
            if bounds_match:
                x1, y1, x2, y2 = map(int, bounds_match.groups())
                width, height = x2 - x1, y2 - y1
            
            # Create a surface
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((255, 255, 255))
            
            # Draw a representation of the PS content
            # This is very basic - in reality, PS files are complex
            font = pygame.font.Font(None, 24)
            text = font.render(f"PS content from {os.path.basename(ps_path)}", True, (0, 0, 0))
            surface.blit(text, (20, 20))
            
            # Draw a border
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, width-1, height-1), 1)
            
            # Save the image
            pygame.image.save(surface, png_path)
            
            print(f"Created representation at {png_path} (not a true conversion)")
            return True
            
        except ImportError:
            # Method 2: If reportlab isn't available, create a default image with warning
            width, height = 500, 500
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((255, 255, 255))
            
            # Create a message about the conversion
            font = pygame.font.Font(None, 24)
            lines = [
                f"PS File: {os.path.basename(ps_path)}",
                "Could not convert - Ghostscript required",
                "Install Ghostscript for proper conversion",
                "This is a placeholder image"
            ]
            
            for i, line in enumerate(lines):
                text = font.render(line, True, (0, 0, 0))
                surface.blit(text, (20, 20 + i * 30))
            
            # Draw a border
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, width-1, height-1), 1)
            
            # Save the image
            pygame.image.save(surface, png_path)
            
            print(f"Created placeholder at {png_path} (not a true conversion)")
            return True
            
    except Exception as e:
        print(f"Alternative conversion failed: {e}")
        return False

def compile_image_file():
    """
    Convert image files from PS format to PNG.
    
    This function allows batch conversion of PostScript files to PNG format.
    It requires Ghostscript to be installed for proper conversion, but includes
    a fallback method if Ghostscript is not available.
    """
    try:
        # Check if PIL is installed
        try:
            from PIL import Image
        except ImportError:
            print("Error: PIL (pillow) module is not installed. Please install it first.")
            print("You can install it using: pip install pillow")
            return
        
        # Check if Ghostscript is installed and accessible
        ghostscript_found = False
        try:
            # Try to find ghostscript using subprocess
            import subprocess
            try:
                # Try Windows command
                subprocess.run(["gswin64c", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                ghostscript_found = True
            except FileNotFoundError:
                try:
                    # Try standard command (for Unix/macOS)
                    subprocess.run(["gs", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                    ghostscript_found = True
                except FileNotFoundError:
                    ghostscript_found = False
        except Exception:
            ghostscript_found = False
            
        if not ghostscript_found:
            print("\nERROR: Ghostscript is not installed or not in your PATH.")
            print("\nTo fix this:")
            print("1. Install Ghostscript:")
            print("   - Windows: Download from https://ghostscript.com/releases/gsdnld.html")
            print("   - macOS: Use Homebrew with 'brew install ghostscript'")
            print("   - Linux: Use 'apt-get install ghostscript' or equivalent for your distribution")
            print("\n2. After installation, make sure Ghostscript is in your system PATH")
            print("\n3. Alternative: Convert your .ps files to PNG using another tool first")
            print("   - You can use online converters or other software if Ghostscript installation is problematic")
            
            use_alternative = input("\nWould you like to try an alternative method without Ghostscript? (y/n): ")
            if use_alternative.lower() != 'y':
                return
            
            print("\nUsing alternative method (may not work for all PS files)...")
            # Alternative method will be implemented below
        
        nof = input("Input number of files: ")
        try:
            nof_ = int(nof)
        except ValueError:
            print("Error: Please enter a valid number.")
            return
            
        ins_x = input("Enter first file id: ")
        try:
            x = int(ins_x)
        except ValueError:
            print("Error: Please enter a valid first file ID.")
            return
            
        donu = input("Do you have more than one file (y [Yes], n [No])? ")
        
        if donu.lower() == 'y':
            ins_y = input("Enter last file id: ")
            try:
                y = int(ins_y)
            except ValueError:
                print("Error: Please enter a valid last file ID.")
                return
        
        ins = input("Enter path of files: ")
        if not os.path.exists(ins):
            print(f"Warning: The path {ins} doesn't exist. Files might not be found.")
        
        pre = input("Enter filename-prefix: ")
        
        if nof_ > 1:
            for i in range(x, y+1):
                ixy = str(i)
                path = os.path.join(ins, f"{pre}{ixy}.ps")
                
                if not os.path.exists(path):
                    print(f"Warning: File {path} not found, skipping.")
                    continue
                    
                try:
                    if ghostscript_found:
                        # Use regular PIL with Ghostscript
                        img = Image.open(path)
                        output_path = f"{pre}{ixy}.png"
                        img.save(output_path)
                        print(f"Converted: {path} -> {output_path}")
                    else:
                        # Use alternative method
                        output_path = f"{pre}{ixy}.png"
                        alt_convert_ps_to_png(path, output_path)
                except Exception as e:
                    print(f"Error converting {path}: {e}")
        
        elif nof_ == 1:
            path = os.path.join(ins, f"{pre}{ins_x}.ps")
            
            if not os.path.exists(path):
                print(f"Warning: File {path} not found.")
                return
                
            try:
                if ghostscript_found:
                    # Use regular PIL with Ghostscript
                    img = Image.open(path)
                    output_path = f"{pre}{ins_x}.png"
                    img.save(output_path)
                    print(f"Converted: {path} -> {output_path}")
                else:
                    # Use alternative method
                    output_path = f"{pre}{ins_x}.png"
                    alt_convert_ps_to_png(path, output_path)
            except Exception as e:
                print(f"Error converting {path}: {e}")

        print("Image conversion completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def img_generator():
    """
    Generate grid-based images with custom colors.
    
    This function creates a grid of colored cells and saves them as PostScript files,
    which can later be converted to PNG using the compile_image_file function.
    """
    try:
        # Check if required modules are installed
        try:
            from tkinter import Canvas
            import random
            import math
        except ImportError as e:
            print(f"Error: Required module not found: {e}")
            print("Please install missing dependencies first.")
            return
        
        print("Random number seed:", random.random())
        
        master = tk.Tk()
        master.title("Image Generator")
        master.attributes('-fullscreen', True)
        
        print("Welcome to Image Generator\n")
        print("Tip: side width should be a factor of the image width, the same goes for the image height in relation to the side height of each pixel.")
        
        try:
            change1 = input("Enter side width of image block: ")
            change = int(change1)
            
            change2 = input("Enter side height of image block: ")
            change_h = int(change2)
            
            a1 = input("Enter width of image: ")
            a = int(a1)
            
            b1 = input("Enter height of image: ")
            b = int(b1)
        except ValueError:
            print("Error: Please enter valid numbers for dimensions.")
            master.destroy()
            return
        
        # Check if dimensions make sense
        if a % change != 0:
            print(f"Warning: Image width ({a}) is not divisible by block width ({change}).")
        if b % change_h != 0:
            print(f"Warning: Image height ({b}) is not divisible by block height ({change_h}).")
        
        pin_p1 = a / change
        pin_p2 = b / change_h
        
        w = Canvas(master, width=a, height=b)
        
        # Color selection
        c = []
        print("\nColor Selection:")
        print("Enter colors by name ('red', 'blue', etc.) or hex code ('#FF0000')")
        
        while True:
            app_end = input("Enter colour Hex with # or colour name: ")
            c.append(app_end)
            
            conti_ = input("Enter 1 to add another colour, 0 to move on: ")
            if conti_ != '1':  # Breaks the loop if input is not '1'
                break
        
        # Check if at least one color was added
        if len(c) == 0:
            print("Error: No colors were specified.")
            master.destroy()
            return
        
        # Calculate generation parameters
        xc = 0
        zerox = 0
        zeroy = 0
        p = 1
        name = 1
        cells = ((a // change) * (b // change_h))
        upper = cells - 1
        nbr_comb = math.pow(len(c), cells)
        files = int(nbr_comb)
        
        if files > 1000:
            confirm = input(f"Warning: This will generate {files} files. Continue? (y/n): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                master.destroy()
                return
        
        img_fn_prefix = input("Enter Image filename prefix (omit the file extension name): ")
        
        print(f"\nGenerating {files} image files...")
        file_count = 0
        rown = 0
        
        max_files = min(files, 1000)  # Limit to 1000 files for safety
        
        for t in range(0, max_files):
            file_count = file_count + 1
            switch = 1
            sw = 0
            x = 0
            col = cells - 1
            
            while x < cells:
                if switch == 1:
                    row = 1
                    nxleft = 0
                    nxright = change
                    nyleft = 0
                    nyright = change_h
                    zerox = 0
                    zeroy = 0
                
                c_length = len(c)    
                switch = 0
                
                rdiv = math.pow(len(c), col)
                cell = (rown / rdiv) % (len(c))
                celled = int(cell)
                
                # Create rectangle with selected color
                w.create_rectangle(zerox, nyleft, nxright, nyright, fill=c[celled], outline="black", width=0)
                
                if x <= cells:
                    col = col - 1
                
                w.grid(row=zeroy, column=zerox + change)
                if p >= pin_p1 and p % pin_p1 == 0:
                    zeroy = zeroy + change_h
                    zerox = -change
                    nxleft = change
                    nxright = 0
                    nyleft = nyleft + change_h
                    nyright = nyright + change_h
                
                zerox = zerox + change
                p = p + 1
                nxright = nxright + change
                
                if xc == 3:
                    xc = 0
                    
                x = x + 1    
            
            rown = rown + 1
            ce = str(name)
            w.update()
            
            # Save postscript
            try:
                w.postscript(file=f"{img_fn_prefix}{ce}.ps", colormode='color', x=0, y=0, width=a, height=b)
                print(f"Generated image {file_count}/{max_files}: {img_fn_prefix}{ce}.ps")
            except Exception as e:
                print(f"Error saving image {ce}: {e}")
            
            name = name + 1
            
            # Check if user wants to continue after every 10 images
            if file_count % 10 == 0 and file_count < max_files:
                cont = input(f"Generated {file_count} images. Continue? (y/n): ")
                if cont.lower() != 'y':
                    print("Image generation stopped by user.")
                    break
        
        master.destroy()
        print(f"Image generation complete. {file_count} images created.")
    
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        try:
            master.destroy()
        except:
            pass

def save_session():
    """
    Save current session data to a file.
    
    This function persists:
    - Last matrix used
    - Last cursor position
    - Command history
    - Command dictionary with parameters
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open("session_data.pkl", "wb") as f:
            pickle.dump(session_data, f)
        
        # Also save the command dictionary
        with open("command_dict.json", "w") as f:
            json.dump(command_dict, f, indent=4)
        
        print("Session saved successfully")
        return True
    except Exception as e:
        print(f"Error saving session: {e}")
        return False

def load_session():
    """
    Load session data from file if it exists.
    
    Restores:
    - Last matrix used
    - Last cursor position
    - Command history
    - Command dictionary with parameters
    """
    global session_data, command_dict
    
    try:
        if os.path.exists("session_data.pkl"):
            with open("session_data.pkl", "rb") as f:
                session_data = pickle.load(f)
            print("Session data loaded")
        else:
            print("No previous session found, starting fresh")
    except Exception as e:
        print(f"Error loading session: {e}")
    
    try:
        if os.path.exists("command_dict.json"):
            with open("command_dict.json", "r") as f:
                command_dict = json.load(f)
            print("Command dictionary loaded")
    except Exception as e:
        print(f"Error loading command dictionary: {e}")

class CommandEditor:
    """
    A Tkinter form for editing command parameters.
    
    This class provides a GUI for editing command code and parameters,
    with options to save changes and optionally execute the command.
    """
    def __init__(self, command_id, command_text, parent_window=None):
        """
        Initialize the CommandEditor.
        
        Args:
            command_id: ID of the command to edit
            command_text: Python code for the command
            parent_window: Parent Tkinter window (optional)
        """
        self.command_id = command_id
        self.command_text = command_text
        self.result = None
        
        # Create a new Tkinter window
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.root.title(f"Edit Command {command_id}")
        self.root.geometry("600x500")
        
        # Make it modal
        self.root.transient(parent_window) if parent_window else None
        self.root.grab_set()
        
        # Create a frame for the form
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Command ID display
        ttk.Label(main_frame, text=f"Command ID: {command_id}").pack(anchor=tk.W, pady=5)
        
        # Command text editor
        ttk.Label(main_frame, text="Command Python Code:").pack(anchor=tk.W, pady=(10, 0))
        self.command_text_widget = tk.Text(main_frame, height=10, width=60)
        self.command_text_widget.pack(fill=tk.BOTH, expand=True, pady=5)
        self.command_text_widget.insert(tk.END, command_text)
        
        # Parameters frame
        param_frame = ttk.LabelFrame(main_frame, text="Command Parameters", padding="10")
        param_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Extract parameters from command text
        self.parameters = self.extract_parameters(command_text)
        self.param_entries = {}
        
        for i, param in enumerate(self.parameters):
            param_label = ttk.Label(param_frame, text=f"{param}:")
            param_label.grid(row=i, column=0, sticky=tk.W, pady=2)
            
            # Get existing value from command_dict if available
            existing_value = ""
            if str(command_id) in command_dict and param in command_dict[str(command_id)]["parameters"]:
                existing_value = command_dict[str(command_id)]["parameters"][param]
            
            param_entry = ttk.Entry(param_frame, width=40)
            param_entry.insert(0, existing_value)
            param_entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.param_entries[param] = param_entry
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save & Run", command=self.save_and_run).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the main loop if this is the main window
        if not parent_window:
            self.root.mainloop()
    
    def extract_parameters(self, command_text):
        """
        Extract parameters from command text by looking for input statements.
        
        Args:
            command_text: Python code to parse for parameters
            
        Returns:
            list: List of parameter names found in the code
        """
        params = []
        lines = command_text.split('\n')
        for line in lines:
            # Look for input statements
            if "input(" in line:
                # Extract variable name before the = sign
                var_name = line.split('=')[0].strip()
                if var_name not in params:
                    params.append(var_name)
        
        # If no parameters found in input statements, check for common variable names
        if not params:
            import re
            # Look for variable assignments
            pattern = r'(\w+)\s*='
            matches = re.findall(pattern, command_text)
            # Filter out common Python keywords and built-ins
            keywords = ['if', 'else', 'elif', 'for', 'while', 'def', 'class', 'return', 'True', 'False', 'None']
            for match in matches:
                if match not in keywords and match not in params:
                    params.append(match)
        
        return params
    
    def save_command(self):
        """Save the command and parameters"""
        updated_command = self.command_text_widget.get("1.0", tk.END).strip()
        
        # Prepare parameters dictionary
        params = {}
        for param, entry in self.param_entries.items():
            params[param] = entry.get()
        
        # Update command_dict
        command_dict[str(self.command_id)] = {
            "command": updated_command,
            "parameters": params,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Print status
        print(f"Command {self.command_id} saved with parameters: {params}")
        
        self.result = {
            "command": updated_command,
            "run": False
        }
        self.root.destroy()
    
    def save_and_run(self):
        """Save the command and signal it should be run"""
        self.save_command()
        if self.result:
            self.result["run"] = True
    
    def cancel(self):
        """Cancel the editing and close the window"""
        self.result = None
        self.root.destroy()

class DictionaryViewer:
    """
    A real-time updatable viewer for the command dictionary.
    
    This class provides a UI for viewing, searching, and exporting
    commands stored in the command dictionary.
    """
    def __init__(self, parent_window=None):
        """
        Initialize the Dictionary Viewer.
        
        Args:
            parent_window: Parent Tkinter window (optional)
        """
        # Create a new Tkinter window
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.root.title("Command Dictionary Viewer")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Close", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Create search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_changed)
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5)
        
        # Create treeview for commands
        columns = ("command_id", "command", "parameters", "updated")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("command_id", text="Command ID")
        self.tree.heading("command", text="Command")
        self.tree.heading("parameters", text="Parameters")
        self.tree.heading("updated", text="Last Updated")
        
        # Define column widths
        self.tree.column("command_id", width=80)
        self.tree.column("command", width=300)
        self.tree.column("parameters", width=250)
        self.tree.column("updated", width=150)
        
        # Create scrollbars
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Place tree and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click event to open editor
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Populate treeview
        self.refresh_data()
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        if not parent_window:
            self.root.mainloop()
    
    def refresh_data(self):
        """Refresh the treeview with current command_dict data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add command_dict items to treeview
        for cmd_id, cmd_data in command_dict.items():
            # Truncate command text for display
            cmd_text = cmd_data["command"][:50] + "..." if len(cmd_data["command"]) > 50 else cmd_data["command"]
            
            # Format parameters as string
            params_str = ", ".join([f"{k}={v}" for k, v in cmd_data["parameters"].items()])
            params_str = params_str[:50] + "..." if len(params_str) > 50 else params_str
            
            # Add to treeview
            self.tree.insert("", "end", values=(cmd_id, cmd_text, params_str, cmd_data.get("last_updated", "Unknown")))
    
    def search_changed(self, *args):
        """Filter treeview based on search text"""
        search_text = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered items
        for cmd_id, cmd_data in command_dict.items():
            if (search_text in cmd_id.lower() or 
                search_text in cmd_data["command"].lower() or 
                any(search_text in param.lower() or 
                    (isinstance(val, str) and search_text in val.lower())
                    for param, val in cmd_data["parameters"].items())):
                
                # Truncate command text for display
                cmd_text = cmd_data["command"][:50] + "..." if len(cmd_data["command"]) > 50 else cmd_data["command"]
                
                # Format parameters as string
                params_str = ", ".join([f"{k}={v}" for k, v in cmd_data["parameters"].items()])
                params_str = params_str[:50] + "..." if len(params_str) > 50 else params_str
                
                # Add to treeview
                self.tree.insert("", "end", values=(cmd_id, cmd_text, params_str, cmd_data.get("last_updated", "Unknown")))
    
    def on_item_double_click(self, event):
        """Handle double-click on a treeview item"""
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Get command ID from selected item
        cmd_id = self.tree.item(selected_item[0], "values")[0]
        
        # Get command data
        cmd_data = command_dict.get(cmd_id, None)
        if not cmd_data:
            return
        
        # Open command editor
        editor = CommandEditor(cmd_id, cmd_data["command"], self.root)
        self.root.wait_window(editor.root)
        
        # Refresh data if editor made changes
        if editor.result:
            self.refresh_data()
    
    def export_data(self):
        """Export the command dictionary to a JSON file"""
        filename = simpledialog.askstring("Export Data", "Enter filename for export:", initialvalue="command_dict_export.json")
        if filename:
            try:
                with open(filename, "w") as f:
                    json.dump(command_dict, f, indent=4)
                messagebox.showinfo("Export Successful", f"Command dictionary exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting command dictionary: {e}")

def update_command_file(filename, commands):
    """
    Update the command file with the current commands.
    
    Args:
        filename (str): Path to the command file
        commands (list): List of command strings to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w') as f:
            for cmd in commands:
                f.write(cmd + "\n")
        print(f"Command file {filename} updated")
        return True
    except Exception as e:
        print(f"Error updating command file: {e}")
        return False

def generate_cmp():
    """
    Generate a command matrix template file.
    
    Creates a template file with placeholders for all 65536 possible commands,
    organized into different sections for input, variable handling, and execution.
    """
    try:
        name_m = input("Enter the name for your command matrix: ")
        with open(name_m, 'w') as f:
            # Lines 1 to 13107: string_var# = input('Enter string_var: ')
            for i in range(13107):
                f.write(f"string_var{i} = input('Enter string_var: ')\n")
            
            # Lines 13108 to 26214: var_given# = input('Enter the variable name to be used: ')
            for i in range(13107):
                f.write(f"var_given{i} = input('Enter the variable name to be used: ')\n")
            
            # Lines 26215 to 39321: var_glob# = globals()[var_given#]
            for i in range(13107):
                f.write(f"var_glob{i} = globals().get(var_given{i}, 'Variable not found')  # Error handling: 'Variable not found'\n")
            
            # Lines 39322 to 52428: exec(var_glob#)
            for i in range(13107):
                f.write(f"if isinstance(var_glob{i}, str): exec(var_glob{i})  # Error handling: Execute only if it's a string\n")
            
            # Lines 52429 to 65535: eval(var_glob#)
            for i in range(13107):
                f.write(f"if isinstance(var_glob{i}, str): result = eval(var_glob{i})  # Error handling: Evaluate only if it's a string\n")
            
            # Line 65536: Hyperlink
            f.write("import webbrowser; webbrowser.open('https://www.openai.com')")
        
        print(f"Command matrix template created: {name_m}")
    except Exception as e:
        print(f"Error generating command matrix: {e}")

def programming_engine():
    """
    Main event sequencer programming engine.
    
    This is the core function that handles:
    - Loading/saving sessions
    - Command matrix visualization and navigation
    - Command execution
    - User input handling (keyboard, mouse, controller)
    - Two-step command selection process
    
    The engine provides a visual interface for navigating a large command matrix,
    with multiple control methods and command editing capabilities.
    """
    # Load session data
    load_session()
    
    # Create a Tkinter root window for dialog boxes
    tk_root = tk.Tk()
    tk_root.withdraw()  # Hide the main window
    
    # Try to import webbrowser
    try:
        import webbrowser
    except ImportError:
        print("Warning: webbrowser module not found. Documentation access will be unavailable.")
    
    # Create a custom event type
    MY_CUSTOM_EVENT = pygame.USEREVENT + 1
    DICT_VIEWER_EVENT = pygame.USEREVENT + 2
    EDIT_COMMAND_EVENT = pygame.USEREVENT + 3
    
    # Initialize pygame
    pygame.init()
    
    # Initialize joystick module
    pygame.joystick.init()
    
    # Check if any joysticks are connected
    joystick = None
    if pygame.joystick.get_count() > 0:
        # Get the first joystick
        joystick = pygame.joystick.Joystick(0)
        # Initialize the joystick
        joystick.init()
        print("Joystick detected and initialized")
    else:
        print("No joystick detected. D-pad mode will not be fully functional.")
    
    # Set screen size
    enter = 422
    screen_width = enter
    screen_height = enter
    
    bls = 52
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Event Sequencer")
    
    # Initialize font for help text
    pygame.font.init()
    font = pygame.font.Font(None, 18)
    
    # Check if Command_Template.txt exists, create if not
    if not os.path.exists("Command_Template.txt"):
        print("Command_Template.txt not found. Creating default template...")
        bus_ = 255
        amount_ = (bus_ + 1) * (bus_ + 1)
        line_number_ = 0
                    
        create_f = open("Command_Template.txt", "w")
        while(line_number_ < amount_):
            create_f.write("print(\"[Empty Command Slot] (Change using a text-editor to Update this slot in Command_Template.txt\") #remembering to rename Command_Template.txt\n")
            line_number_ = line_number_ + 1
    
        create_f.close()
        print("Command_Template.txt created successfully")
    
    # LoadCommands
    xin = 0
    filnam = session_data.get("last_matrix", "Command_Template.txt")
    
    try:
        with open(filnam, 'r') as file:
            commands = file.readlines()
            xin = xin + 1
    except FileNotFoundError:
        print(f"Error: {filnam} not found. Falling back to Command_Template.txt")
        filnam = "Command_Template.txt"
        try:
            with open(filnam, 'r') as file:
                commands = file.readlines()
        except FileNotFoundError:
            print("Critical error: No command file found!")
            tk_root.destroy()
            pygame.quit()
            return
    
    star = [0]
    
    for i, command in enumerate(commands):
        commands[i] = command.strip()
        star.append(command)
    del star[0]
    
    # Check if Coordinates_Python.txt exists, create if not
    if not os.path.exists("Coordinates_Python.txt"):
        print("Creating Coordinates_Python.txt...")
        with open("Coordinates_Python.txt", "w") as f:
            for i in range(65536):
                x = i % 256
                y = i // 256
                f.write(f"{i},{x},{y}\n")
        print("Coordinates_Python.txt created successfully")
    
    # LoadCoordinates
    try:
        with open('Coordinates_Python.txt', 'r') as file2:
            commands2 = file2.readlines()
            
        starsx = [0]
        starsy = [0]
        
        for i2, command2 in enumerate(commands2):
            commands2[i2] = command2.strip()
            cmd2 = command2.split(",")
            starsx.append(int(cmd2[1]))
            varys = int(cmd2[2].strip())
            starsy.append(varys)
            
        del starsx[0]
        del starsy[0]
    except Exception as e:
        print(f"Error loading coordinates: {e}")
        # Create simple fallback coordinates
        starsx = list(range(256)) * 256
        starsy = [i // 256 for i in range(65536)]
    
    # Load images - create placeholders if needed
    block_images = []
    if not all(os.path.exists(f"block{i+1}.png") for i in range(256)):
        print("Block images not found. Creating placeholder images...")
        try:
            from PIL import Image, ImageDraw
            
            for i in range(256):
                # Create a simple colored block based on the index
                color = (i % 4 * 60, i % 8 * 30, i % 16 * 15)
                img = Image.new('RGB', (50, 50), color)
                draw = ImageDraw.Draw(img)
                draw.text((5, 5), str(i), fill=(255, 255, 255))
                img.save(f"block{i+1}.png")
            print("Placeholder block images created.")
        except ImportError:
            print("PIL not available. Creating basic pygame blocks...")
            for i in range(256):
                # Create basic colored surface
                surf = pygame.Surface((50, 50))
                surf.fill((i % 4 * 60, i % 8 * 30, i % 16 * 15))
                pygame.image.save(surf, f"block{i+1}.png")
    
    for i in range(256):
        try:
            block_images.append(pygame.image.load(f"block{i+1}.png"))
        except pygame.error:
            # Create a fallback image if loading fails
            surf = pygame.Surface((50, 50))
            surf.fill((100, 100, 100))
            block_images.append(surf)
            print(f"Warning: Failed to load block{i+1}.png, using fallback")
    
    # Check if player images exist, create if not
    if not os.path.exists("player.png") or not os.path.exists("player2.png"):
        print("Player images not found. Creating placeholder images...")
        try:
            from PIL import Image, ImageDraw
            
            # Create player.png (red circle)
            img = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((5, 5, 45, 45), fill=(255, 0, 0, 255))
            img.save("player.png")
            
            # Create player2.png (blue circle)
            img2 = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
            draw2 = ImageDraw.Draw(img2)
            draw2.ellipse((5, 5, 45, 45), fill=(0, 0, 255, 255))
            img2.save("player2.png")
        except ImportError:
            # Fallback to basic pygame
            surf1 = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surf1, (255, 0, 0), (25, 25), 20)
            pygame.image.save(surf1, "player.png")
            
            surf2 = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surf2, (0, 0, 255), (25, 25), 20)
            pygame.image.save(surf2, "player2.png")
            
        print("Placeholder player images created.")
    
    # Load player images
    try:
        player_image = pygame.image.load("player.png")
        player_image2 = pygame.image.load("player2.png")
    except pygame.error:
        # Create fallback surfaces if loading fails
        player_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(player_image, (255, 0, 0), (25, 25), 20)
        
        player_image2 = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(player_image2, (0, 0, 255), (25, 25), 20)
        
        print("Warning: Failed to load player images, using fallback")
    
    # Set player position from session data
    player_x, player_y = session_data.get("last_position", (0, 0))
    
    con_program = int(input("Continue? 1 [yes], 0 [no]: "))
    if con_program == 1:
        print("Ok ...")
    elif con_program == 0:
        print("Exiting ...")
        tk_root.destroy()
        pygame.quit()
        return
    else:
        print("Error: Invalid input")
        tk_root.destroy()
        pygame.quit()
        return
    
    # Set initial input type
    typei = "k"
    print("\n\nIn Local Command Mode\n\n")
    print("Navigation Modes:")
    print("- Switch Command Matrix [s]")
    print("- Mouse mode [m]")
    print("- Keyboard arrows [k]")
    print("- D-Pad (Xbox One Controller) [d]")
    print("- Press [SPACEBAR] to call a command by ID")
    print("\nD-Pad Mode Instructions:")
    print("- Use D-pad to navigate through the command matrix")
    print("- A button: Start a selection (first press) and confirm (second press)")
    print("- B button: Cancel a selection")
    print("- X button: Edit the currently selected command")
    print("- Y button: Execute the currently selected command")
    print("- Start button: Open documentation/help in web browser")
    print("- Select button: Open command dictionary viewer")
    print("- Left trigger: Navigate to previous index")
    print("- Right trigger: Navigate to next index")
    print("\nCommand Selection:")
    print("1. First click: Select an index position (sets reference point)")
    print("2. Second click: Select a specific command relative to that index")
    print("3. After selecting a command, you can choose to view/edit or execute it")
    print("\nOther Controls:")
    print("- Press [v] to view command dictionary")
    print("- Press [Ctrl+S] to save the current session")
    
    # Some input variables
    input_variable = 0
    # Add the custom event to the event queue
    pygame.event.post(pygame.event.Event(MY_CUSTOM_EVENT, {"input_variable": input_variable}))
    
    # Etch loop
    etch = 0
    
    # Maze width and height
    maze_width = 16
    maze_height = 16
    
    # Main game loop
    running = True
    
    # Screen size settings
    scale_factor_x = screen_width / maze_width
    scale_factor = scale_factor_x
    
    bls = int(bls * 0.5)
    
    scaled_block_images = []
    
    # Before the main loop
    is_selecting_submatrix = False
    submatrix_start_pos = None
    selected_command = None
    execute_command_prompt = False
    
    # Two-step selection mode
    selection_mode = "index"  # Start in index selection mode
    index_position = None     # Store the index position when selected
    
    # Status message
    status_message = ""
    status_time = 0
    
    # Scale block images
    for ni in range(256):
        s_i = pygame.transform.scale(block_images[ni], (bls, bls))
        block_images[ni] = s_i
    
    # Main loop
    try:
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save session before exiting
                    session_data["last_position"] = (player_x, player_y)
                    session_data["last_matrix"] = filnam
                    save_session()
                    running = False
        
                elif event.type == pygame.KEYDOWN:
                    # Check for key press event
                    if event.key == pygame.K_v:
                        # Open command dictionary viewer
                        tk_root.deiconify()
                        dict_viewer = DictionaryViewer(tk_root)
                        tk_root.wait_window(dict_viewer.root)
                        tk_root.withdraw()
                        status_message = "Command dictionary viewed"
                        status_time = current_time
                    
                    elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Save session with Ctrl+S
                        session_data["last_position"] = (player_x, player_y)
                        session_data["last_matrix"] = filnam
                        save_session()
                        status_message = "Session saved"
                        status_time = current_time
                    
                    elif event.key == pygame.K_m and typei != "m":
                        # Update input type
                        typei = "m"
                        selection_mode = "index"  # Reset selection mode
                        status_message = "Mouse mode activated"
                        status_time = current_time
                    
                    elif event.key == pygame.K_k and typei != "k":
                        # Update input type
                        typei = "k"
                        selection_mode = "index"  # Reset selection mode
                        status_message = "Keyboard mode activated"
                        status_time = current_time
                    
                    elif event.key == pygame.K_s and typei != "s" and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        # Update input type (not Ctrl+S)
                        typei = "s"
                        selection_mode = "index"  # Reset selection mode
                        status_message = "Matrix selection mode"
                        status_time = current_time
                    
                    elif event.key == pygame.K_d and typei != "d":
                        # Update input type
                        typei = "d"
                        selection_mode = "index"  # Reset selection mode
                        status_message = "D-pad mode activated"
                        status_time = current_time
                    
                    elif event.key == pygame.K_SPACE:
                        # Update input_type
                        typei = "n"
                        # Check for status
                        tk_root.deiconify()
                        enter_cma = simpledialog.askinteger("Execute Command", 
                                                        "Enter command? 1 [yes], 0 [no]:", 
                                                        parent=tk_root, minvalue=0, maxvalue=1)
                        if enter_cma is None:
                            typei = "k"
                            tk_root.withdraw()
                            continue
                        
                        if enter_cma == 0:
                            typei = "k"
                            player_x = 0
                            player_y = 0
                        elif enter_cma == 1:
                            input_variable = simpledialog.askinteger("Execute Command", 
                                                                "Enter command number ID (0 to 65535):", 
                                                                parent=tk_root, minvalue=0, maxvalue=65535)
                            if input_variable is None:
                                typei = "k"
                                tk_root.withdraw()
                                continue
                            
                            # Add the custom event to the event queue
                            pygame.event.post(pygame.event.Event(MY_CUSTOM_EVENT, {"input_variable": input_variable}))
                        
                        tk_root.withdraw()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Calculate cell position
                    cell_x = mouse_x // bls
                    cell_y = mouse_y // bls
                    
                    # Check if in grid bounds
                    if 0 <= cell_x < int(screen_width / bls) and 0 <= cell_y < int(screen_height / bls):
                        # Update player position for mouse mode
                        if typei == 'm':
                            # Handle two-step click selection process
                            if selection_mode == "index":
                                # First click: Set the index position
                                index_position = (cell_x, cell_y)
                                player_x = cell_x
                                player_y = cell_y
                                selection_mode = "command"
                                status_message = f"Index selected at ({cell_x}, {cell_y}). Now click a command."
                                status_time = current_time
                            
                            elif selection_mode == "command":
                                # Second click: Select the command relative to the index position
                                
                                # Calculate the relative command position
                                relative_x = cell_x - index_position[0]
                                relative_y = cell_y - index_position[1]
                                
                                # Calculate the absolute command ID
                                index_number = (index_position[1] * (int(screen_width / bls) // 16)) + (index_position[0] // 16)
                                command_position = (relative_y * 16) + relative_x
                                command_id = (index_number * 256) + command_position
                                
                                # Check if it's a valid command ID
                                if 0 <= command_id < len(star):
                                    # Show command action dialog
                                    tk_root.deiconify()
                                    command_action = simpledialog.askinteger("Command Selected", 
                                        f"Command {command_id} selected.\nWhat would you like to do?\n1: View/Edit\n2: Execute\n0: Cancel", 
                                        parent=tk_root, minvalue=0, maxvalue=2)
                                    
                                    if command_action == 1:
                                        # View/Edit the command
                                        command_text = star[command_id]
                                        editor = CommandEditor(command_id, command_text, tk_root)
                                        tk_root.wait_window(editor.root)
                                        
                                        # Handle editor result
                                        if editor.result:
                                            # Update command in the star list
                                            star[command_id] = editor.result["command"]
                                            
                                            # Update command file
                                            update_command_file(filnam, star[1:])
                                            
                                            status_message = f"Command {command_id} updated"
                                            status_time = current_time
                                            
                                            # Execute if requested
                                            if editor.result["run"]:
                                                try:
                                                    exec(editor.result["command"], globals())
                                                    status_message = f"Command {command_id} executed"
                                                    status_time = current_time
                                                    # Add to history
                                                    session_data["command_history"].append({
                                                        "command_id": command_id,
                                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                    })
                                                except Exception as e:
                                                    status_message = f"Error: {e}"
                                                    status_time = current_time
                                    
                                    elif command_action == 2:
                                        # Execute the command
                                        try:
                                            exec(star[command_id], globals())
                                            status_message = f"Command {command_id} executed"
                                            status_time = current_time
                                            # Add to history
                                            session_data["command_history"].append({
                                                "command_id": command_id,
                                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            })
                                        except Exception as e:
                                            status_message = f"Error: {e}"
                                            status_time = current_time
                                    
                                    tk_root.withdraw()
                                else:
                                    status_message = f"Invalid command ID: {command_id}"
                                    status_time = current_time
                                
                                # Reset selection mode
                                selection_mode = "index"
            
                # Check for custom event type
                if event.type == MY_CUSTOM_EVENT:
                    # Access the input variable from the event object
                    cma = event.input_variable
                    
                    if typei == 'n':
                        if cma is not None and enter_cma == 1:
                            player_x = 0
                            player_y = 0
                            
                            # Clear screen
                            screen.fill((255, 255, 255))
                            
                            try:
                                if 0 <= cma < len(star):
                                    exec(star[cma], globals())
                                    status_message = f"Command {cma} executed"
                                    status_time = current_time
                                    # Add to history
                                    session_data["command_history"].append({
                                        "command_id": cma,
                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    })
                                else:
                                    status_message = f"Command {cma} out of range"
                                    status_time = current_time
                            except Exception as e:
                                status_message = f"Error: {e}"
                                status_time = current_time
                                
                            # Update command index pointer
                            bus = 255 + 1
                            if cma <= 255:
                                cmd_index = 0
                                command_point = cma
                            elif cma > 255:
                                cmd_index = cma//bus
                                command_point = cma
                                for tip in range(0, cmd_index):
                                    command_point = command_point - (bus)
                            
                            prompt = "Executing Command " + str(cma) + " from index: " + str(cmd_index)
                            print(prompt)
                            
                            player_x = starsy[cmd_index] if cmd_index < len(starsy) else 0
                            player_y = starsx[cmd_index] if cmd_index < len(starsx) else 0
                            command_point_x = starsy[command_point] if command_point < len(starsy) else 0
                            command_point_y = starsx[command_point] if command_point < len(starsx) else 0
                            
                            # Draw blocks
                            for y in range(int(screen_height/bls)):
                                for x in range(int(screen_width /bls)):
                                    relative_x = x - player_x
                                    relative_y = y - player_y
                                    idx = relative_x + relative_y * int(screen_width/bls)
                                    idx = idx % len(block_images)  # Ensure index is in range
                                    screen.blit(block_images[idx], (x * bls, y * bls))
                            
                            if typei == 'n':
                                # Draw2 player
                                screen.blit(player_image2, (player_x * bls, player_y * bls))
                                # Draw Command pointer
                                screen.blit(player_image, (command_point_x * bls, command_point_y * bls))
                            
                            # Update display
                            pygame.display.update()
            
            # Controller input processing
            if typei == 'd':
                # Check for Xbox controller input
                if joystick:
                    try:
                        # Handle joystick movement
                        # Check for D-Pad input
                        dpad = joystick.get_hat(0)
                        if dpad == (1, 0):
                            player_x += 1
                        elif dpad == (-1, 0):
                            player_x -= 1
                        elif dpad == (0, 1):
                            player_y -= 1
                        elif dpad == (0, -1):
                            player_y += 1
                        
                        # Alternative: use analog sticks
                        # Using a deadzone of 0.2 to prevent drift
                        deadzone = 0.2
                        
                        # Left analog stick
                        left_x = joystick.get_axis(0)
                        left_y = joystick.get_axis(1)
                        
                        if abs(left_x) > deadzone or abs(left_y) > deadzone:
                            # Slow down movement with analog sticks
                            if pygame.time.get_ticks() % 10 == 0:
                                if left_x > deadzone:
                                    player_x += 1
                                elif left_x < -deadzone:
                                    player_x -= 1
                                
                                if left_y > deadzone:
                                    player_y += 1
                                elif left_y < -deadzone:
                                    player_y -= 1
                                    
                        # Keep player in bounds
                        if player_x < 0:
                            player_x = 0
                        if player_x >= int(screen_width / bls):
                            player_x = int(screen_width / bls) - 1
                        if player_y < 0:
                            player_y = 0
                        if player_y >= int(screen_height / bls):
                            player_y = int(screen_height / bls) - 1
                        
                        # Check for triggers (if available)
                        # Left trigger (navigate to previous index)
                        try:
                            left_trigger = joystick.get_axis(2)
                            if left_trigger > 0.7 and pygame.time.get_ticks() % 20 == 0:
                                # Navigate to previous index
                                player_x = max(0, player_x - 16)
                                player_y = max(0, player_y - 16)
                                status_message = f"Previous index: ({player_x}, {player_y})"
                                status_time = current_time
                        except:
                            pass
                            
                        # Right trigger (navigate to next index)
                        try:
                            right_trigger = joystick.get_axis(5)
                            if right_trigger > 0.7 and pygame.time.get_ticks() % 20 == 0:
                                # Navigate to next index
                                max_x = int(screen_width / bls) - 1
                                max_y = int(screen_height / bls) - 1
                                player_x = min(max_x, player_x + 16)
                                player_y = min(max_y, player_y + 16)
                                status_message = f"Next index: ({player_x}, {player_y})"
                                status_time = current_time
                        except:
                            pass
                        
                        # Handling button presses
                        buttons = joystick.get_numbuttons()
                        for i in range(buttons):
                            if joystick.get_button(i):
                                # A button (index 0) - Start/confirm selection
                                if i == 0:
                                    if selection_mode == "index":
                                        # First press: Set the index position
                                        index_position = (player_x, player_y)
                                        selection_mode = "command"
                                        status_message = f"Index selected at {index_position}. Use D-pad to select command."
                                        status_time = current_time
                                    
                                    elif selection_mode == "command":
                                        # Second press: Select the command
                                        # Calculate the relative command position
                                        relative_x = player_x - index_position[0]
                                        relative_y = player_y - index_position[1]
                                        
                                        # Calculate absolute command ID
                                        rows_per_index = 16
                                        cols_per_index = 16
                                        index_row = index_position[1] // rows_per_index
                                        index_col = index_position[0] // cols_per_index
                                        
                                        # Calculate the index number (0-255)
                                        index_number = index_row * (screen_width // (bls * cols_per_index)) + index_col
                                        
                                        # Calculate the relative position within the index (0-255)
                                        rel_row = relative_y % rows_per_index
                                        rel_col = relative_x % cols_per_index
                                        command_position = rel_row * cols_per_index + rel_col
                                        
                                        # Final command ID
                                        command_id = (index_number * 256) + command_position
                                        
                                        if 0 <= command_id < len(star):
                                            status_message = f"Command {command_id} selected. Press X to edit or Y to execute."
                                            status_time = current_time
                                            selected_command = command_id
                                        else:
                                            status_message = f"Invalid command ID: {command_id}"
                                            status_time = current_time
                                            selected_command = None
                                
                                # B button (index 1) - Cancel selection
                                elif i == 1:
                                    if selection_mode == "command":
                                        selection_mode = "index"
                                        index_position = None
                                        status_message = "Selection cancelled"
                                        status_time = current_time
                                    selected_command = None
                                
                                # X button (index 2) - Edit selected command
                                elif i == 2:
                                    if selected_command is not None:
                                        command_text = star[selected_command]
                                        tk_root.deiconify()
                                        editor = CommandEditor(selected_command, command_text, tk_root)
                                        tk_root.wait_window(editor.root)
                                        tk_root.withdraw()
                                        
                                        if editor.result:
                                            # Update command
                                            star[selected_command] = editor.result["command"]
                                            update_command_file(filnam, star[1:])
                                            
                                            status_message = f"Command {selected_command} updated"
                                            status_time = current_time
                                            
                                            # Execute if requested
                                            if editor.result["run"]:
                                                try:
                                                    exec(editor.result["command"], globals())
                                                    status_message = f"Command {selected_command} executed"
                                                    status_time = current_time
                                                    session_data["command_history"].append({
                                                        "command_id": selected_command,
                                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                    })
                                                except Exception as e:
                                                    status_message = f"Error: {e}"
                                                    status_time = current_time
                                
                                # Y button (index 3) - Execute selected command
                                elif i == 3:
                                    if selected_command is not None:
                                        try:
                                            exec(star[selected_command], globals())
                                            status_message = f"Command {selected_command} executed"
                                            status_time = current_time
                                            session_data["command_history"].append({
                                                "command_id": selected_command,
                                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            })
                                        except Exception as e:
                                            status_message = f"Error: {e}"
                                            status_time = current_time
                                
                                # Start button (index 7) - Open documentation
                                elif i == 7:
                                    status_message = "Opening documentation"
                                    status_time = current_time
                                    # Attempt to open docs (command 65535)
                                    try:
                                        if 65535 < len(star):
                                            exec(star[65535], globals())
                                        else:
                                            webbrowser.open("https://www.openai.com")
                                    except Exception as e:
                                        print(f"Error accessing documentation: {e}")
                                
                                # Select button (index 6) - Open command dictionary
                                elif i == 6:
                                    status_message = "Opening command dictionary"
                                    status_time = current_time
                                    tk_root.deiconify()
                                    dict_viewer = DictionaryViewer(tk_root)
                                    tk_root.wait_window(dict_viewer.root)
                                    tk_root.withdraw()
                                    
                    except Exception as e:
                        print(f"Error processing controller input: {e}")
            
            # Switch command matrix
            if typei == 's':
                # LoadCommands
                tk_root.deiconify()
                filnam = simpledialog.askstring("Command Matrix", "Enter name of Command Matrix file:", parent=tk_root)
                if not filnam:
                    typei = "k"
                    tk_root.withdraw()
                    continue
                
                quet = simpledialog.askinteger("Command Matrix", "Enter 1 if file exists [Read], 2 if new [Write]:", 
                                            parent=tk_root, minvalue=1, maxvalue=2)
                if not quet:
                    typei = "k"
                    tk_root.withdraw()
                    continue
                
                tk_root.withdraw()
                
                bus = 255
                amount = (bus + 1) * (bus + 1)
                line_number = 0
                
                if quet == 2:
                    try:
                        create_f = open(filnam, "w")
                        while line_number < amount:
                            create_f.write("print(\"[Empty Command Slot] Change using a text-editor to Update this slot in Command_Template.txt after renaming it accordingly.\")\n")
                            line_number = line_number + 1
                        
                        create_f.close()
                    except Exception as e:
                        status_message = f"Error creating file: {e}"
                        status_time = current_time
                        typei = "k"
                        continue
                
                try:
                    with open(filnam, 'r') as file:
                        commands = file.readlines()
                    
                    star = [0]
                    
                    for i, command in enumerate(commands):
                        commands[i] = command.strip()
                        star.append(command)
                    del star[0]
                    
                    # Update session data
                    session_data["last_matrix"] = filnam
                    status_message = f"Loaded matrix: {filnam}"
                    status_time = current_time
                    
                except Exception as e:
                    status_message = f"Error: {e}"
                    status_time = current_time
                
                # Reset state of matrix
                typei = "k"
                player_x = 0
                player_y = 0
                selection_mode = "index"
                index_position = None
            
            # Keyboard movement
            if typei == 'k':
                # Get user keyboard input
                keys = pygame.key.get_pressed()
                
                # Update move flag based on keyboard input
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    move = True
                else:
                    move = False
                
                # Update player position based on keyboard input
                if move:
                    if keys[pygame.K_LEFT]:
                        player_x -= 1
                    if keys[pygame.K_RIGHT]:
                        player_x += 1
                    if keys[pygame.K_UP]:
                        player_y -= 1
                    if keys[pygame.K_DOWN]:
                        player_y += 1
                    
                    # Keep player in bounds
                    if player_x < 0:
                        player_x = 0
                    if player_x >= int(screen_width / bls):
                        player_x = int(screen_width / bls) - 1
                    if player_y < 0:
                        player_y = 0
                    if player_y >= int(screen_height / bls):
                        player_y = int(screen_height / bls) - 1
            
            # Mouse hover highlight
            if typei == 'm':
                # This is just for preview/hover - actual movement is in MOUSEBUTTONDOWN
                pass
            
            # Clear screen
            screen.fill((255, 255, 255))
            
            # Draw blocks and player
            if typei in ['k', 'm', 'd']:
                for y in range(int(screen_height/bls)):
                    for x in range(int(screen_width/bls)):
                        relative_x = x - player_x
                        relative_y = y - player_y
                        
                        # Calculate command index and ensure it's in range
                        cmd_index = (relative_x + relative_y * int(screen_width // bls)) % len(block_images)
                        
                        # Draw block
                        screen.blit(block_images[cmd_index], (x * bls, y * bls))
                        
                        # Convert to string for dict lookup
                        cmd_str = str(cmd_index)
                        
                        # Highlight cells with stored commands in dictionary
                        if cmd_str in command_dict:
                            pygame.draw.rect(screen, (0, 255, 0), 
                                        (x * bls + bls - 10, y * bls, 10, 10))
                        
                        # Draw small command index on each cell
                        cmd_text = font.render(str(cmd_index), True, (0, 0, 0))
                        screen.blit(cmd_text, (x * bls + 2, y * bls + 2))
                
                # Draw player cursor
                screen.blit(player_image, (player_x * bls, player_y * bls))
                
                # If we're in command selection mode, highlight the index position
                if selection_mode == "command" and index_position:
                    # Draw a border around the index cell
                    ix, iy = index_position
                    pygame.draw.rect(screen, (255, 0, 0), 
                                  (ix * bls, iy * bls, bls, bls), 2)
                
                # If a command is selected, highlight it
                if selected_command is not None:
                    # Calculate the position of the selected command
                    sel_idx = selected_command % 256
                    sel_x = index_position[0] + (sel_idx % 16)
                    sel_y = index_position[1] + (sel_idx // 16)
                    
                    # Draw highlight
                    s = pygame.Surface((bls, bls), pygame.SRCALPHA)
                    s.fill((0, 0, 255, 128))  # Blue with alpha
                    screen.blit(s, (sel_x * bls, sel_y * bls))
                
                # If in mouse mode, highlight hovered cell
                if typei == 'm':
                    hover_x = pygame.mouse.get_pos()[0] // bls
                    hover_y = pygame.mouse.get_pos()[1] // bls
                    
                    if 0 <= hover_x < int(screen_width / bls) and 0 <= hover_y < int(screen_height / bls):
                        # Draw semi-transparent overlay
                        s = pygame.Surface((bls, bls), pygame.SRCALPHA)
                        s.fill((255, 255, 0, 128))  # Yellow with alpha
                        screen.blit(s, (hover_x * bls, hover_y * bls))
                
                # Draw submatrix selection
                if is_selecting_submatrix and submatrix_start_pos:
                    min_x = min(submatrix_start_pos[0], player_x)
                    max_x = max(submatrix_start_pos[0], player_x)
                    min_y = min(submatrix_start_pos[1], player_y)
                    max_y = max(submatrix_start_pos[1], player_y)
                    
                    # Draw semi-transparent selection rectangle
                    width = (max_x - min_x + 1) * bls
                    height = (max_y - min_y + 1) * bls
                    s = pygame.Surface((width, height), pygame.SRCALPHA)
                    s.fill((0, 128, 255, 128))  # Blue with alpha
                    screen.blit(s, (min_x * bls, min_y * bls))
                
                # Display selection mode in the status bar
                mode_status = f"Mode: {typei.upper()} | Selection: {selection_mode.capitalize()}"
                if selection_mode == "command" and index_position:
                    mode_status += f" | Index: ({index_position[0]}, {index_position[1]})"
                
                # Draw mode status in corner
                mode_text = font.render(mode_status, True, (0, 0, 0))
                screen.blit(mode_text, (5, 5))
            
            # Draw status message if recent
            if status_message and current_time - status_time < 3000:  # Show for 3 seconds
                # Draw status bar at the bottom
                status_bar = pygame.Surface((screen_width, 20))
                status_bar.fill((220, 220, 220))
                screen.blit(status_bar, (0, screen_height - 20))
                
                # Render status text
                status_text = font.render(status_message, True, (0, 0, 0))
                screen.blit(status_text, (5, screen_height - 15))
                
                # Show current mode
                mode_text = font.render(f"Mode: {typei.upper()}", True, (0, 0, 0))
                mode_width = mode_text.get_width()
                screen.blit(mode_text, (screen_width - mode_width - 5, screen_height - 15))
            
            # Update display
            if typei in ['k', 'm', 'd']:
                pygame.display.update()
            
            # Control frame rate
            pygame.time.Clock().tick(30)
    
    except Exception as e:
        print(f"Critical error in main loop: {e}")
    
    finally:
        # Save session before quitting
        session_data["last_position"] = (player_x, player_y)
        session_data["last_matrix"] = filnam
        save_session()
        
        # Destroy Tkinter root
        tk_root.destroy()
        
        # Quit pygame
        pygame.quit()

def main():
    """
    Main menu function for the Event Sequencer system.
    
    Provides a command-line interface to access all system functionality.
    """
    while True:
        print("\nEvent Sequencer - Command Matrix System")
        print("---------------------------------------")
        print("1. Run Programming Engine")
        print("2. Generate Command Matrix Template")
        print("3. View Command Dictionary")
        print("4. Generate Required Images")
        print("5. Compile Required Images (PS to PNG Conversion)")
        print("6. Install Dependencies")
        print("7. Check Ghostscript Installation (Required for PS to PNG)")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            programming_engine()
        elif choice == "2":
            generate_cmp()
        elif choice == "3":
            # Initialize Tkinter and open dictionary viewer
            load_session()  # Load existing command dictionary
            root = tk.Tk()
            root.withdraw()
            viewer = DictionaryViewer(root)
            root.mainloop()
        elif choice == "4":
            img_generator()
        elif choice == "5":
            compile_image_file()
        elif choice == "6":
            install_dependencies()
            input("Press Enter to continue...")
        elif choice == "7":
            check_ghostscript()
            input("Press Enter to continue...")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
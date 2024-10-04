import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageGrab
import json
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import tkinter.font as font

# Use TkAgg backend for matplotlib
matplotlib.use('TkAgg')

# Global variables
square_data = {}       # Dictionary to track each sub-square's data
split_squares = {}     # Track which squares are split
action_history = []    # For undo functionality
redo_stack = []        # For redo functionality
preferences = {        # Default preferences
    'default_font_size': 12,
    'default_font_type': 'Arial',
    'default_bg_color': '#F0F0F0',
    'default_font_color': '#000000'
}

# Setup mode function with GUI dialogs
def setup_mode():
    global square_size, num_rows, num_cols, root, canvas

    root = tk.Tk()
    root.withdraw()  # Hide the root window during setup

    # Use ttk for modern themed widgets
    style = ttk.Style()
    style.theme_use('clam')

    square_size = simpledialog.askinteger("Cell Size", "Enter cell size (pixels):", minvalue=50)
    if square_size is None:
        root.destroy()
        return

    # Allow user to specify rows and columns for rectangular grids
    num_rows = simpledialog.askinteger("Grid Rows", "Enter number of rows:", minvalue=1)
    if num_rows is None:
        root.destroy()
        return

    num_cols = simpledialog.askinteger("Grid Columns", "Enter number of columns:", minvalue=1)
    if num_cols is None:
        root.destroy()
        return

    window_height = square_size * num_rows
    window_width = square_size * num_cols

    root.deiconify()  # Show the root window after setup
    root.title("Mathematical Sandbox")
    root.geometry(f'{window_width}x{window_height}')
    root.resizable(True, True)

    create_menu(root)

    # Create a frame for the canvas and scrollbars
    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True)

    canvas = tk.Canvas(frame, width=window_width, height=window_height, bg='white')
    canvas.pack(side='left', fill='both', expand=True)

    # Add scrollbars
    h_scroll = ttk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
    h_scroll.pack(side='bottom', fill='x')
    v_scroll = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    v_scroll.pack(side='right', fill='y')
    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    canvas.config(scrollregion=(0, 0, window_width, window_height))

    draw_grid()  # Automatically draw the grid

    root.mainloop()

# Function to create the menu bar
def create_menu(root):
    menu_bar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_grid)
    file_menu.add_command(label="Open", command=open_grid)
    file_menu.add_command(label="Save", command=save_grid)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit Menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Undo", command=undo)
    edit_menu.add_command(label="Redo", command=redo)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # Math Menu
    math_menu = tk.Menu(menu_bar, tearoff=0)
    math_menu.add_command(label="Matrix Operations", command=open_matrix_operations)
    math_menu.add_command(label="Plot Function", command=open_plot_function)
    math_menu.add_command(label="Vector Field", command=open_vector_field)
    math_menu.add_command(label="Complex Function Visualization", command=open_complex_visualization)
    math_menu.add_command(label="Fractals", command=open_fractal_window)
    menu_bar.add_cascade(label="Math", menu=math_menu)

    # Preferences Menu
    preferences_menu = tk.Menu(menu_bar, tearoff=0)
    preferences_menu.add_command(label="Settings", command=open_preferences)
    menu_bar.add_cascade(label="Preferences", menu=preferences_menu)

    root.config(menu=menu_bar)

# Function to draw the grid and set up bindings
def draw_grid():
    global canvas
    canvas.delete('all')  # Clear the canvas
    for i in range(num_rows):
        for j in range(num_cols):
            tag = f"square_{i}_{j}"
            square = canvas.create_rectangle(j * square_size, i * square_size, (j + 1) * square_size,
                                             (i + 1) * square_size, fill=preferences['default_bg_color'], outline="gray", tags=tag)
            canvas.tag_bind(tag, '<Button-1>', lambda event, row=i, col=j: on_left_click(event, row, col))
            canvas.tag_bind(tag, '<Button-3>', lambda event, row=i, col=j: on_right_click(event, row, col))
            canvas.tag_bind(tag, '<Control-Button-1>', lambda event, row=i, col=j: on_paste_image(event, row, col))
            add_tooltip(tag, "Left-click to edit\nRight-click to split/merge\nCtrl+Click to paste image")

# Function to add a tooltip to canvas items
def add_tooltip(tag, text):
    tooltip = None

    def enter(event):
        nonlocal tooltip
        x = event.widget.winfo_pointerx()
        y = event.widget.winfo_pointery()
        tooltip = tk.Toplevel(root)
        tooltip.overrideredirect(True)
        tooltip.geometry(f"+{x+20}+{y+10}")
        label = ttk.Label(tooltip, text=text, background="#FFFFE0", relief='solid', borderwidth=1)
        label.pack()

    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    canvas.tag_bind(tag, '<Enter>', enter)
    canvas.tag_bind(tag, '<Leave>', leave)

# Function to handle left-click on a sub-square
def on_left_click(event, row, col, sub_square_id=None):
    # Open properties window
    open_properties_window(row, col, sub_square_id)

# Function to open the properties window for a sub-square
def open_properties_window(row, col, sub_square_id):
    # Determine the key for the square_data dictionary
    if sub_square_id:
        key = (row, col, sub_square_id)
    else:
        key = (row, col)

    current_data = square_data.get(key, {})
    current_text = current_data.get("text", "")
    current_color = current_data.get("color", preferences['default_bg_color'])
    current_font_size = current_data.get("font_size", preferences['default_font_size'])
    current_font_type = current_data.get("font_type", preferences['default_font_type'])
    current_font_color = current_data.get("font_color", preferences['default_font_color'])
    current_expr = current_data.get("expression", "")

    prop_win = tk.Toplevel(root)
    prop_win.title("Edit Sub-Square Properties")

    # Use ttk widgets for styling
    main_frame = ttk.Frame(prop_win, padding=10)
    main_frame.pack(fill='both', expand=True)

    # Text Entry
    ttk.Label(main_frame, text="Text:").grid(row=0, column=0, sticky='e', pady=2)
    text_var = tk.StringVar(value=current_text)
    text_entry = ttk.Entry(main_frame, textvariable=text_var, width=30)
    text_entry.grid(row=0, column=1, sticky='w', pady=2)

    # Expression Entry
    ttk.Label(main_frame, text="Expression:").grid(row=1, column=0, sticky='e', pady=2)
    expr_var = tk.StringVar(value=current_expr)
    expr_entry = ttk.Entry(main_frame, textvariable=expr_var, width=30)
    expr_entry.grid(row=1, column=1, sticky='w', pady=2)

    # Background Color Picker
    ttk.Label(main_frame, text="Background Color:").grid(row=2, column=0, sticky='e', pady=2)
    bg_color_var = tk.StringVar(value=current_color)
    bg_color_btn = ttk.Button(main_frame, text="Choose Color", command=lambda: choose_color(bg_color_var, bg_color_display))
    bg_color_btn.grid(row=2, column=1, sticky='w', pady=2)
    bg_color_display = tk.Label(main_frame, text="       ", bg=current_color)
    bg_color_display.grid(row=2, column=2, pady=2)

    # Font Size Slider
    ttk.Label(main_frame, text="Font Size:").grid(row=3, column=0, sticky='e', pady=2)
    font_size_var = tk.DoubleVar(value=current_font_size)
    font_size_slider = ttk.Scale(main_frame, from_=6, to=72, orient='horizontal', variable=font_size_var)
    font_size_slider.grid(row=3, column=1, sticky='w', pady=2)

    # Font Type Dropdown
    ttk.Label(main_frame, text="Font Type:").grid(row=4, column=0, sticky='e', pady=2)
    font_var = tk.StringVar(value=current_font_type)
    fonts = list(font.families())
    font_dropdown = ttk.Combobox(main_frame, textvariable=font_var, values=fonts, state='readonly')
    font_dropdown.grid(row=4, column=1, sticky='w', pady=2)

    # Font Color Picker
    ttk.Label(main_frame, text="Font Color:").grid(row=5, column=0, sticky='e', pady=2)
    font_color_var = tk.StringVar(value=current_font_color)
    font_color_btn = ttk.Button(main_frame, text="Choose Color", command=lambda: choose_color(font_color_var, font_color_display))
    font_color_btn.grid(row=5, column=1, sticky='w', pady=2)
    font_color_display = tk.Label(main_frame, text="       ", bg=current_font_color)
    font_color_display.grid(row=5, column=2, pady=2)

    # Apply Button
    apply_btn = ttk.Button(main_frame, text="Apply", command=lambda: [apply_properties(row, col, sub_square_id, text_var.get(), expr_var.get(), bg_color_var.get(), font_size_var.get(), font_var.get(), font_color_var.get()), prop_win.destroy()])
    apply_btn.grid(row=6, column=0, columnspan=3, pady=10)

# Function to choose a color
def choose_color(color_var, display_label):
    color = askcolor()[1]
    if color:
        color_var.set(color)
        display_label.config(bg=color)

# Function to apply properties to a sub-square
def apply_properties(row, col, sub_square_id, text, expression, bg_color, font_size, font_type, font_color):
    # Determine if we are editing a split sub-square or a main sub-square
    if sub_square_id:
        key = (row, col, sub_square_id)
    else:
        key = (row, col)

    # Save current state before applying changes
    prev_state = square_data.get(key, {}).copy()
    action_history.append((key, prev_state))
    # Clear redo stack on new action
    redo_stack.clear()

    # Update square_data
    square_data[key] = {
        "text": text,
        "expression": expression,
        "color": bg_color,
        "font_size": font_size,
        "font_type": font_type,
        "font_color": font_color,
        "image": square_data.get(key, {}).get("image")  # Preserve existing image
    }

    # Draw the sub-square
    draw_char_on_square(row, col, text, expression, bg_color, font_size, font_type, font_color, sub_square_id)

# Function to draw or update a sub-square
def draw_char_on_square(row, col, input_text, expression, color, font_size, font_type, font_color, sub_square_id=None):
    if sub_square_id:
        i, j = sub_square_id
        tag = f"square_{row}_{col}_{i}_{j}"
        new_square_size = split_squares[(row, col)]["new_square_size"]
        sub_square_x = col * square_size + j * new_square_size
        sub_square_y = row * square_size + i * new_square_size
    else:
        tag = f"square_{row}_{col}"
        sub_square_x = col * square_size
        sub_square_y = row * square_size
        new_square_size = square_size

    canvas.delete(tag)  # Remove existing elements with this tag

    # Draw the rectangle
    canvas.create_rectangle(sub_square_x, sub_square_y, sub_square_x + new_square_size,
                            sub_square_y + new_square_size, fill=color, outline='gray', tags=tag)

    # Display text or evaluate expression
    display_text = input_text
    if expression:
        try:
            # Use sympy to parse and evaluate the expression
            expr = sp.sympify(expression)
            result = expr.evalf()
            display_text = str(result)
            # Update square_data with the result
            key = (row, col, sub_square_id) if sub_square_id else (row, col)
            square_data[key]["result"] = result
        except Exception as e:
            display_text = "Error"

    # Draw the text
    canvas.create_text(sub_square_x + new_square_size / 2, sub_square_y + new_square_size / 2,
                       text=display_text, font=(font_type, int(font_size)), fill=font_color, anchor="center", width=new_square_size, tags=tag)

    # Check if there is an image to display
    key = (row, col, sub_square_id) if sub_square_id else (row, col)
    image = square_data.get(key, {}).get("image")
    if image:
        canvas.create_image(sub_square_x, sub_square_y, image=image, anchor='nw', tags=tag)

    # Rebind the events
    canvas.tag_bind(tag, '<Button-1>', lambda event, r=row, c=col: on_left_click(event, r, c, sub_square_id))
    canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=row, c=col: on_paste_image(event, r, c, sub_square_id))
    add_tooltip(tag, "Left-click to edit\nCtrl+Click to paste image")

    # Update canvas scroll region
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to handle undo action
def undo():
    if action_history:
        key, prev_state = action_history.pop()
        redo_stack.append((key, square_data.get(key, {}).copy()))
        # Restore previous state
        draw_char_on_square_from_state(key, prev_state)
    else:
        messagebox.showinfo("Undo", "Nothing to undo.", parent=root)

# Function to handle redo action
def redo():
    if redo_stack:
        key, next_state = redo_stack.pop()
        action_history.append((key, square_data.get(key, {}).copy()))
        # Apply next state
        draw_char_on_square_from_state(key, next_state)
    else:
        messagebox.showinfo("Redo", "Nothing to redo.", parent=root)

# Function to draw a sub-square from a saved state
def draw_char_on_square_from_state(key, state):
    if len(key) == 2:
        row, col = key
        sub_square_id = None
    else:
        row, col, sub_square_id = key

    if state:
        draw_char_on_square(row, col, state.get('text', ''), state.get('expression', ''), state.get('color', preferences['default_bg_color']),
                            state.get('font_size', preferences['default_font_size']), state.get('font_type', preferences['default_font_type']),
                            state.get('font_color', preferences['default_font_color']), sub_square_id)
    else:
        # Clear the square
        if sub_square_id:
            tag = f"square_{row}_{col}_{sub_square_id[0]}_{sub_square_id[1]}"
            canvas.delete(tag)
        else:
            tag = f"square_{row}_{col}"
            canvas.delete(tag)

# Function to save the grid to a file
def save_grid():
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    if file_path:
        data = {
            'square_data': square_data,
            'split_squares': split_squares,
            'num_rows': num_rows,
            'num_cols': num_cols,
            'square_size': square_size,
            'preferences': preferences
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, default=str)

# Function to open a grid from a file
def open_grid():
    global square_data, split_squares, num_rows, num_cols, square_size, preferences
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Update variables and redraw grid
        square_data = data['square_data']
        split_squares = data['split_squares']
        num_rows = data['num_rows']
        num_cols = data['num_cols']
        square_size = data['square_size']
        preferences = data.get('preferences', preferences)
        draw_grid()
        # Redraw squares
        for key, state in square_data.items():
            draw_char_on_square_from_state(key, state)

# Function to create a new grid
def new_grid():
    global square_data, split_squares, num_rows, num_cols, square_size, preferences
    if messagebox.askyesno("New Grid", "Are you sure you want to create a new grid? Unsaved changes will be lost."):
        square_data.clear()
        split_squares.clear()
        action_history.clear()
        redo_stack.clear()
        setup_mode()

# Function to open the preferences window
def open_preferences():
    pref_win = tk.Toplevel(root)
    pref_win.title("Preferences")

    main_frame = ttk.Frame(pref_win, padding=10)
    main_frame.pack(fill='both', expand=True)

    # Default Font Size
    ttk.Label(main_frame, text="Default Font Size:").grid(row=0, column=0, sticky='e', pady=2)
    font_size_var = tk.DoubleVar(value=preferences['default_font_size'])
    font_size_slider = ttk.Scale(main_frame, from_=6, to=72, orient='horizontal', variable=font_size_var)
    font_size_slider.grid(row=0, column=1, sticky='w', pady=2)

    # Default Font Type
    ttk.Label(main_frame, text="Default Font Type:").grid(row=1, column=0, sticky='e', pady=2)
    font_var = tk.StringVar(value=preferences['default_font_type'])
    fonts = list(font.families())
    font_dropdown = ttk.Combobox(main_frame, textvariable=font_var, values=fonts, state='readonly')
    font_dropdown.grid(row=1, column=1, sticky='w', pady=2)

    # Default Background Color
    ttk.Label(main_frame, text="Default Background Color:").grid(row=2, column=0, sticky='e', pady=2)
    bg_color_var = tk.StringVar(value=preferences['default_bg_color'])
    bg_color_btn = ttk.Button(main_frame, text="Choose Color", command=lambda: choose_color(bg_color_var, bg_color_display))
    bg_color_btn.grid(row=2, column=1, sticky='w', pady=2)
    bg_color_display = tk.Label(main_frame, text="       ", bg=preferences['default_bg_color'])
    bg_color_display.grid(row=2, column=2, pady=2)

    # Default Font Color
    ttk.Label(main_frame, text="Default Font Color:").grid(row=3, column=0, sticky='e', pady=2)
    font_color_var = tk.StringVar(value=preferences['default_font_color'])
    font_color_btn = ttk.Button(main_frame, text="Choose Color", command=lambda: choose_color(font_color_var, font_color_display))
    font_color_btn.grid(row=3, column=1, sticky='w', pady=2)
    font_color_display = tk.Label(main_frame, text="       ", bg=preferences['default_font_color'])
    font_color_display.grid(row=3, column=2, pady=2)

    # Apply Button
    apply_btn = ttk.Button(main_frame, text="Apply", command=lambda: [apply_preferences(font_size_var.get(), font_var.get(), bg_color_var.get(), font_color_var.get()), pref_win.destroy()])
    apply_btn.grid(row=4, column=0, columnspan=3, pady=10)

# Function to apply preferences
def apply_preferences(font_size, font_type, bg_color, font_color):
    preferences['default_font_size'] = font_size
    preferences['default_font_type'] = font_type
    preferences['default_bg_color'] = bg_color
    preferences['default_font_color'] = font_color

# Function to handle right-click (splitting or merging sub-squares)
def on_right_click(event, row, col):
    menu = tk.Menu(root, tearoff=0)
    if (row, col) in split_squares:
        menu.add_command(label="Merge Squares", command=lambda: merge_square(row, col))
    else:
        menu.add_command(label="Split Squares", command=lambda: split_square_dialog(row, col))
    menu.add_command(label="Paste Image", command=lambda: paste_image(row, col))
    menu.post(event.x_root, event.y_root)

# Function to show the split square dialog
def split_square_dialog(row, col):
    split_value = simpledialog.askstring("Split Sub-Square", "Enter split value (rows, columns):", parent=root)
    if not split_value:
        return

    try:
        rows, cols = map(int, split_value.split(','))
        if rows <= 0 or cols <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter positive integers separated by a comma.", parent=root)
        return

    on_split_square(row, col, rows, cols)

# Function to split a square into sub-squares
def on_split_square(row, col, rows, cols):
    if (row, col) in split_squares:
        messagebox.showinfo("Already Split", "This sub-square is already split.", parent=root)
        return

    new_square_size = square_size // max(rows, cols)

    for i in range(rows):
        for j in range(cols):
            sub_square_x = col * square_size + j * new_square_size
            sub_square_y = row * square_size + i * new_square_size

            tag = f"square_{row}_{col}_{i}_{j}"
            canvas.create_rectangle(sub_square_x, sub_square_y, sub_square_x + new_square_size,
                                    sub_square_y + new_square_size, fill=preferences['default_bg_color'], outline='gray', tags=tag)
            canvas.create_text(sub_square_x + new_square_size / 2, sub_square_y + new_square_size / 2, text="",
                               font=(preferences['default_font_type'], preferences['default_font_size']), anchor="center", width=new_square_size)

            # Bind left-click to edit split sub-squares after the split
            canvas.tag_bind(tag, '<Button-1>', lambda event, r=i, c=j: on_left_click(event, row, col, (r, c)))
            canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=i, c=j: on_paste_image(event, row, col, (r, c)))
            add_tooltip(tag, "Left-click to edit\nCtrl+Click to paste image")

    split_squares[(row, col)] = {
        "rows": rows,
        "cols": cols,
        "original_font_size": preferences['default_font_size'],
        "new_square_size": new_square_size
    }

    # Remove the original square
    tag = f"square_{row}_{col}"
    canvas.delete(tag)
    canvas.update()

# Function to merge split squares back into a single square
def merge_square(row, col):
    for i in range(split_squares[(row, col)]["rows"]):
        for j in range(split_squares[(row, col)]["cols"]):
            tag = f"square_{row}_{col}_{i}_{j}"
            canvas.delete(tag)
            key = (row, col, (i, j))
            square_data.pop(key, None)
    split_squares.pop((row, col))
    # Redraw the original square
    draw_char_on_square(row, col, "", "", preferences['default_bg_color'], preferences['default_font_size'], preferences['default_font_type'], preferences['default_font_color'])

# Function to handle Ctrl + left-click (pasting images)
def on_paste_image(event, row, col, sub_square_id=None):
    try:
        # Attempt to get the image from the clipboard
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            # Proceed to paste the image from the clipboard
            paste_image(row, col, sub_square_id, image)
        else:
            # No image in clipboard, open file explorer
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                image = Image.open(file_path)
                paste_image(row, col, sub_square_id, image)
            else:
                messagebox.showinfo("No Image Selected", "No image was selected.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to paste image: {e}", parent=root)

def paste_image(row, col, sub_square_id=None, image=None):
    if image is None:
        # This should not happen, but just in case
        return

    # Determine the size and position of the sub-square
    if sub_square_id:
        i, j = sub_square_id
        new_square_size = split_squares[(row, col)]["new_square_size"]
        x = col * square_size + j * new_square_size
        y = row * square_size + i * new_square_size
    else:
        new_square_size = square_size
        x = col * square_size
        y = row * square_size

    # Resize the image to fit the sub-square
    image = image.resize((new_square_size, new_square_size), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(image)

    # Store the image in the square_data dictionary
    key = (row, col, sub_square_id) if sub_square_id else (row, col)
    square_data[key] = square_data.get(key, {})
    square_data[key]["image"] = photo_image  # Store the PhotoImage

    # Draw the image on the canvas
    tag = f"square_{row}_{col}"
    if sub_square_id:
        i, j = sub_square_id
        tag += f"_{i}_{j}"
    canvas.create_image(x, y, image=photo_image, anchor='nw', tags=tag)

    # Rebind the events
    canvas.tag_bind(tag, '<Button-1>', lambda event, r=row, c=col: on_left_click(event, r, c, sub_square_id))
    canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=row, c=col: on_paste_image(event, r, c, sub_square_id))
    add_tooltip(tag, "Left-click to edit\nCtrl+Click to paste image")

# Function to open the matrix operations window
def open_matrix_operations():
    matrix_win = tk.Toplevel(root)
    matrix_win.title("Matrix Operations")

    # Matrix dimensions
    ttk.Label(matrix_win, text="Rows:").grid(row=0, column=0, sticky='e', pady=2)
    rows_var = tk.IntVar(value=3)
    rows_entry = ttk.Entry(matrix_win, textvariable=rows_var)
    rows_entry.grid(row=0, column=1, sticky='w', pady=2)

    ttk.Label(matrix_win, text="Columns:").grid(row=1, column=0, sticky='e', pady=2)
    cols_var = tk.IntVar(value=3)
    cols_entry = ttk.Entry(matrix_win, textvariable=cols_var)
    cols_entry.grid(row=1, column=1, sticky='w', pady=2)

    # Generate Button
    generate_btn = ttk.Button(matrix_win, text="Generate Matrix", command=lambda: generate_matrix(matrix_win, rows_var.get(), cols_var.get()))
    generate_btn.grid(row=2, column=0, columnspan=2, pady=5)

# Function to generate a matrix input grid
def generate_matrix(window, rows, cols):
    matrix_entries = []
    for i in range(rows):
        row_entries = []
        for j in range(cols):
            entry = ttk.Entry(window, width=5)
            entry.grid(row=i+3, column=j)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    # Operation Options
    operations = ["Determinant", "Inverse", "Transpose", "Eigenvalues"]
    op_var = tk.StringVar(value=operations[0])
    op_menu = ttk.Combobox(window, textvariable=op_var, values=operations, state='readonly')
    op_menu.grid(row=rows+4, column=0, columnspan=cols, pady=5)

    # Compute Button
    compute_btn = ttk.Button(window, text="Compute", command=lambda: compute_matrix(matrix_entries, op_var.get()))
    compute_btn.grid(row=rows+5, column=0, columnspan=cols, pady=5)

# Function to compute matrix operations
def compute_matrix(entries, operation):
    try:
        matrix = []
        for row_entries in entries:
            row = []
            for entry in row_entries:
                value = float(entry.get())
                row.append(value)
            matrix.append(row)
        np_matrix = np.array(matrix)

        result = None
        if operation == "Determinant":
            result = np.linalg.det(np_matrix)
        elif operation == "Inverse":
            result = np.linalg.inv(np_matrix)
        elif operation == "Transpose":
            result = np_matrix.T
        elif operation == "Eigenvalues":
            result = np.linalg.eigvals(np_matrix)

        # Display the result
        messagebox.showinfo("Result", f"{operation}:\n{result}", parent=root)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to compute {operation}: {e}", parent=root)

# Function to open the function plotting window
def open_plot_function():
    plot_win = tk.Toplevel(root)
    plot_win.title("Plot Function")

    # Function Entry
    ttk.Label(plot_win, text="Function of x:").grid(row=0, column=0, sticky='e', pady=2)
    func_var = tk.StringVar(value="sin(x)")
    func_entry = ttk.Entry(plot_win, textvariable=func_var, width=30)
    func_entry.grid(row=0, column=1, sticky='w', pady=2)

    # Plot Button
    plot_btn = ttk.Button(plot_win, text="Plot", command=lambda: plot_function(func_var.get()))
    plot_btn.grid(row=1, column=0, columnspan=2, pady=5)

# Function to plot the function
def plot_function(function_str):
    x = sp.symbols('x')
    try:
        func = sp.sympify(function_str)
        f = sp.lambdify(x, func, 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_title(f"Plot of {function_str}")
        ax.grid(True)

        # Display the plot in a new window
        plot_win = tk.Toplevel(root)
        plot_win.title(f"Plot of {function_str}")
        canvas_plot = FigureCanvasTkAgg(fig, master=plot_win)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to plot function: {e}", parent=root)

# Function to open vector field visualization
def open_vector_field():
    vf_win = tk.Toplevel(root)
    vf_win.title("Vector Field Visualization")

    # Vector Components
    ttk.Label(vf_win, text="F(x, y) = [P(x, y), Q(x, y)]").grid(row=0, column=0, columnspan=2, pady=2)
    ttk.Label(vf_win, text="P(x, y):").grid(row=1, column=0, sticky='e', pady=2)
    p_var = tk.StringVar(value="-y")
    p_entry = ttk.Entry(vf_win, textvariable=p_var, width=30)
    p_entry.grid(row=1, column=1, sticky='w', pady=2)

    ttk.Label(vf_win, text="Q(x, y):").grid(row=2, column=0, sticky='e', pady=2)
    q_var = tk.StringVar(value="x")
    q_entry = ttk.Entry(vf_win, textvariable=q_var, width=30)
    q_entry.grid(row=2, column=1, sticky='w', pady=2)

    # Plot Button
    plot_btn = ttk.Button(vf_win, text="Plot Vector Field", command=lambda: plot_vector_field(p_var.get(), q_var.get()))
    plot_btn.grid(row=3, column=0, columnspan=2, pady=5)

# Function to plot the vector field
def plot_vector_field(p_str, q_str):
    x, y = sp.symbols('x y')
    try:
        p_expr = sp.sympify(p_str)
        q_expr = sp.sympify(q_str)
        p_func = sp.lambdify((x, y), p_expr, 'numpy')
        q_func = sp.lambdify((x, y), q_expr, 'numpy')

        x_vals = np.linspace(-10, 10, 20)
        y_vals = np.linspace(-10, 10, 20)
        X, Y = np.meshgrid(x_vals, y_vals)
        U = p_func(X, Y)
        V = q_func(X, Y)

        fig, ax = plt.subplots()
        ax.quiver(X, Y, U, V)
        ax.set_title("Vector Field")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)

        # Display the plot in a new window
        vf_plot_win = tk.Toplevel(root)
        vf_plot_win.title("Vector Field")
        canvas_plot = FigureCanvasTkAgg(fig, master=vf_plot_win)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to plot vector field: {e}", parent=root)

# Function to open complex function visualization
def open_complex_visualization():
    cf_win = tk.Toplevel(root)
    cf_win.title("Complex Function Visualization")

    # Function Entry
    ttk.Label(cf_win, text="Function of z:").grid(row=0, column=0, sticky='e', pady=2)
    func_var = tk.StringVar(value="z**2")
    func_entry = ttk.Entry(cf_win, textvariable=func_var, width=30)
    func_entry.grid(row=0, column=1, sticky='w', pady=2)

    # Plot Button
    plot_btn = ttk.Button(cf_win, text="Visualize", command=lambda: visualize_complex_function(func_var.get()))
    plot_btn.grid(row=1, column=0, columnspan=2, pady=5)

# Function to visualize the complex function using domain coloring
def visualize_complex_function(function_str):
    try:
        # Define the complex function
        z = sp.symbols('z')
        func = sp.lambdify(z, sp.sympify(function_str), 'numpy')

        # Create a grid of complex numbers
        x_vals = np.linspace(-2, 2, 400)
        y_vals = np.linspace(-2, 2, 400)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = X + 1j * Y
        W = func(Z)

        # Calculate the magnitude and angle
        abs_W = np.abs(W)
        angle_W = np.angle(W)

        # Normalize for coloring
        abs_W_normalized = (abs_W - abs_W.min()) / (abs_W.max() - abs_W.min())

        # Create the color mapping
        hsv = np.zeros(W.shape + (3,))
        hsv[..., 0] = (angle_W + np.pi) / (2 * np.pi)  # Hue
        hsv[..., 1] = 1  # Saturation
        hsv[..., 2] = abs_W_normalized  # Value

        rgb = matplotlib.colors.hsv_to_rgb(hsv)

        fig, ax = plt.subplots()
        ax.imshow(rgb, extent=[-2, 2, -2, 2])
        ax.set_title(f"Visualization of {function_str}")
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.grid(False)

        # Display the plot in a new window
        cf_plot_win = tk.Toplevel(root)
        cf_plot_win.title(f"Visualization of {function_str}")
        canvas_plot = FigureCanvasTkAgg(fig, master=cf_plot_win)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to visualize complex function: {e}", parent=root)

# Function to open fractal visualization
def open_fractal_window():
    fractal_win = tk.Toplevel(root)
    fractal_win.title("Fractal Visualization")

    # Fractal Options
    fractal_types = ["Mandelbrot Set", "Julia Set"]
    fractal_var = tk.StringVar(value=fractal_types[0])
    ttk.Label(fractal_win, text="Select Fractal:").grid(row=0, column=0, sticky='e', pady=2)
    fractal_menu = ttk.Combobox(fractal_win, textvariable=fractal_var, values=fractal_types, state='readonly')
    fractal_menu.grid(row=0, column=1, sticky='w', pady=2)

    # Plot Button
    plot_btn = ttk.Button(fractal_win, text="Generate", command=lambda: generate_fractal(fractal_var.get()))
    plot_btn.grid(row=1, column=0, columnspan=2, pady=5)

# Function to generate and display fractals
def generate_fractal(fractal_type):
    try:
        # Set up the grid
        x_vals = np.linspace(-2, 2, 800)
        y_vals = np.linspace(-2, 2, 800)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = X + 1j * Y

        if fractal_type == "Mandelbrot Set":
            C = Z.copy()
            M = np.zeros(Z.shape, dtype=int)
            mask = np.full(Z.shape, True, dtype=bool)
            for i in range(100):
                Z[mask] = Z[mask]**2 + C[mask]
                mask_new = (np.abs(Z) < 2)
                M += mask & ~mask_new
                mask = mask_new
        elif fractal_type == "Julia Set":
            C = complex(-0.70176, -0.3842)
            M = np.zeros(Z.shape, dtype=int)
            mask = np.full(Z.shape, True, dtype=bool)
            for i in range(100):
                Z[mask] = Z[mask]**2 + C
                mask_new = (np.abs(Z) < 2)
                M += mask & ~mask_new
                mask = mask_new

        fig, ax = plt.subplots()
        ax.imshow(M, extent=[-2, 2, -2, 2], cmap='hot')
        ax.set_title(fractal_type)
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.grid(False)

        # Display the plot in a new window
        fractal_plot_win = tk.Toplevel(root)
        fractal_plot_win.title(fractal_type)
        canvas_plot = FigureCanvasTkAgg(fig, master=fractal_plot_win)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate fractal: {e}", parent=root)

# Main execution
if __name__ == '__main__':
    setup_mode()

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageGrab

square_data = {}  # Dictionary to track each sub-square's data (text, colors, fonts, images)
split_squares = {}  # Track which squares are split
font_size_default = 18

# Function to handle right click (splitting sub-squares)
def on_right_click(event, row, col):
    if (row, col) in split_squares:
        # Inform the user that the sub-square is already split
        messagebox.showinfo("Already Split", "This sub-square is already split.", parent=root)
        return

    split_value = simpledialog.askstring("Split Sub-Square", "Enter split value (rows, columns):", parent=root)
    if not split_value:
        return

    try:
        rows, cols = map(int, split_value.split(','))
        if rows <= 0 or cols <= 0:
            raise ValueError("Split values must be positive integers.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid split values.", parent=root)
        return

    new_square_size = square_size // max(rows, cols)

    for i in range(rows):
        for j in range(cols):
            sub_square_x = col * square_size + j * new_square_size
            sub_square_y = row * square_size + i * new_square_size

            tag = f"square_{row}_{col}_{i}_{j}"
            canvas.create_rectangle(sub_square_x, sub_square_y, sub_square_x + new_square_size,
                                    sub_square_y + new_square_size, fill="white", tags=tag)
            canvas.create_text(sub_square_x + new_square_size / 2, sub_square_y + new_square_size / 2, text="",
                               font=("Arial", font_size_default), anchor="center", width=new_square_size)

            # Bind left-click to edit split sub-squares after the split
            canvas.tag_bind(tag, '<Button-1>', lambda event, r=i, c=j: on_left_click(event, row, col, (r, c)))
            canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=i, c=j: on_paste_image(event, row, col, (r, c)))

    split_squares[(row, col)] = {
        "rows": rows,
        "cols": cols,
        "original_font_size": font_size_default,
        "new_square_size": new_square_size
    }

    canvas.update()

# Function to handle left click on a sub-square (editable)
def on_left_click(event, row, col, sub_square_id=None):
    # Determine if we are editing a split sub-square or a main sub-square
    if sub_square_id:
        key = (row, col, sub_square_id)
    else:
        key = (row, col)

    if key in square_data:
        current_data = square_data[key]
        current_text = current_data.get("text", "")
        current_color = current_data.get("color", "#FFFFFF")
        current_font_size = current_data.get("font_size", font_size_default)
        current_font_type = current_data.get("font_type", "Arial")
        current_font_color = current_data.get("font_color", "#000000")
    else:
        # New sub-square, initialize default values
        current_text = ""
        current_color = "#FFFFFF"  # Default white color
        current_font_size = font_size_default
        current_font_type = "Arial"
        current_font_color = "#000000"

    # Ask for user-specified text
    input_text = simpledialog.askstring("Input Text", f"Edit text for sub-square ({row}, {col}):",
                                        initialvalue=current_text, parent=root)
    if input_text is None:  # Cancel action
        return

    # Ask for user-specified background color
    color = askcolor(title="Choose background color", initialcolor=current_color, parent=root)[1]
    if color is None:  # Cancel action
        return

    # Ask for user-specified font size
    font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=current_font_size, parent=root)
    if font_size is None:  # Cancel action
        return

    # Ask for user-specified font type
    font_type = simpledialog.askstring("Font Type", "Enter font type (e.g., Arial, Courier, etc.):",
                                       initialvalue=current_font_type, parent=root)
    if font_type is None:  # Cancel action
        return

    # Ask for user-specified font color
    font_color = askcolor(title="Choose font color", initialcolor=current_font_color, parent=root)[1]
    if font_color is None:  # Cancel action
        return

    # Draw the updated sub-square
    draw_char_on_square(row, col, input_text, color, font_size, font_type, font_color, sub_square_id)

# Function to handle Ctrl + left click (pasting images)
def on_paste_image(event, row, col, sub_square_id=None):
    try:
        # Get the image from the clipboard
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
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

            # Rebind the Ctrl + left click event to allow future edits
            canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=row, c=col: on_paste_image(event, r, c, sub_square_id))
        else:
            messagebox.showerror("Error", "No image found in the clipboard.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to paste image: {e}", parent=root)

# Function to draw or update a sub-square
def draw_char_on_square(row, col, input_text, color, font_size, font_type, font_color, sub_square_id=None):
    if sub_square_id:
        i, j = sub_square_id
        tag = f"square_{row}_{col}_{i}_{j}"
        new_square_size = split_squares[(row, col)]["new_square_size"]
        sub_square_x = col * square_size + j * new_square_size
        sub_square_y = row * square_size + i * new_square_size
        canvas.create_rectangle(sub_square_x, sub_square_y, sub_square_x + new_square_size,
                                sub_square_y + new_square_size, fill=color, tags=tag)
        canvas.create_text(sub_square_x + new_square_size / 2, sub_square_y + new_square_size / 2, text=input_text,
                           font=(font_type, font_size), fill=font_color, anchor="center", width=new_square_size)

        # Check if there is an image to display
        key = (row, col, sub_square_id)
        image = square_data.get(key, {}).get("image")
        if image:
            canvas.create_image(sub_square_x, sub_square_y, image=image, anchor='nw', tags=tag)

        # Store the text, colors, font, and image for future editing
        square_data[key] = {
            "text": input_text,
            "color": color,
            "font_size": font_size,
            "font_type": font_type,
            "font_color": font_color,
            "image": image  # Preserve existing image
        }

        # Rebind the events
        canvas.tag_bind(tag, '<Button-1>', lambda event, r=row, c=col: on_left_click(event, r, c, sub_square_id))
        canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=row, c=col: on_paste_image(event, r, c, sub_square_id))
    else:
        tag = f"square_{row}_{col}"
        canvas.create_rectangle(col * square_size, row * square_size, (col + 1) * square_size,
                                (row + 1) * square_size, fill=color, tags=tag)
        canvas.create_text(col * square_size + square_size / 2, row * square_size + square_size / 2,
                           text=input_text, font=(font_type, font_size), fill=font_color, anchor="center",
                           width=square_size)

        # Check if there is an image to display
        key = (row, col)
        image = square_data.get(key, {}).get("image")
        if image:
            canvas.create_image(col * square_size, row * square_size, image=image, anchor='nw', tags=tag)

        # Store the text, colors, font, and image for future editing
        square_data[key] = {
            "text": input_text,
            "color": color,
            "font_size": font_size,
            "font_type": font_type,
            "font_color": font_color,
            "image": image  # Preserve existing image
        }

        # Rebind the events
        canvas.tag_bind(tag, '<Button-1>', lambda event, r=row, c=col: on_left_click(event, r, c))
        canvas.tag_bind(tag, '<Control-Button-1>', lambda event, r=row, c=col: on_paste_image(event, r, c))

# Function to dynamically draw the grid and set up bindings
def draw_grid():
    global canvas
    for i in range(grid_size):
        for j in range(grid_size):
            tag = f"square_{i}_{j}"
            square = canvas.create_rectangle(j * square_size, i * square_size, (j + 1) * square_size,
                                             (i + 1) * square_size, fill="white", outline="black", tags=tag)
            canvas.tag_bind(tag, '<Button-1>', lambda event, row=i, col=j: on_left_click(event, row, col))
            canvas.tag_bind(tag, '<Button-3>', lambda event, row=i, col=j: on_right_click(event, row, col))
            canvas.tag_bind(tag, '<Control-Button-1>', lambda event, row=i, col=j: on_paste_image(event, row, col))

def setup_mode():
    global square_size, grid_size, root, canvas

    square_size = int(input("Enter sub-square size: "))
    grid_size = int(input("Enter grid size by the number of sub-squares: "))

    window_height = square_size * grid_size + (square_size * 2)
    window_width = square_size * grid_size

    root = tk.Tk()
    root.title("IDE Mode")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    draw_grid()  # Automatically draw the grid

    root.mainloop()

setup_mode()

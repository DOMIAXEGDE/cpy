import raylibpy as rl
import os
import json
import calendar
from datetime import datetime

# Application settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INPUT_BUFFER = 64

# Habit list and progress (In-memory storage for now)
habits = []
progress = {}
input_text = ""
text_box_active = False
selected_day = datetime.today()
current_month = selected_day.month
current_year = selected_day.year

# Load habits from a file
def load_habits():
    global habits, progress
    if os.path.exists('habits.json'):
        with open('habits.json', 'r') as file:
            data = json.load(file)
            habits = data.get("habits", [])
            progress = data.get("progress", {habit: {} for habit in habits})
    else:
        habits = ["Exercise", "Read", "Meditate"]  # Sample habits
        progress = {habit: {} for habit in habits}

# Save habits to a file
def save_habits():
    with open('habits.json', 'w') as file:
        json.dump({"habits": habits, "progress": progress}, file)

# Function to add a new habit
def add_habit(new_habit):
    if new_habit and new_habit not in habits:
        habits.append(new_habit)
        progress[new_habit] = {}
        save_habits()

# Function to get the progress of a habit for a specific day
def get_day_progress(habit, day):
    return progress[habit].get(day.strftime('%Y-%m-%d'), False)

# Function to toggle the progress of a habit for a specific day
def toggle_day_progress(habit, day):
    day_str = day.strftime('%Y-%m-%d')
    progress[habit][day_str] = not progress[habit].get(day_str, False)
    save_habits()

# Function to draw the calendar
def draw_calendar(x, y):
    global current_month, current_year, selected_day
    rl.draw_text(f"{calendar.month_name[current_month]} {current_year}", x + 50, y - 30, 20, rl.BLACK)
    
    # Draw days of the week
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days_of_week):
        rl.draw_text(day, x + i * 40, y, 20, rl.DARKGRAY)
    
    # Draw calendar days
    month_days = calendar.monthcalendar(current_year, current_month)
    for row, week in enumerate(month_days):
        for col, day in enumerate(week):
            if day == 0:
                continue  # Skip empty days
            day_rect = rl.Rectangle(x + col * 40, y + 30 + row * 30, 30, 30)
            day_str = f"{day:02}"
            rl.draw_text(day_str, day_rect.x + 5, day_rect.y + 5, 20, rl.BLACK)
            
            # Highlight selected day
            if selected_day.day == day and selected_day.month == current_month and selected_day.year == current_year:
                rl.draw_rectangle_lines_ex(day_rect, 2, rl.RED)
            
            # Detect click on day
            if rl.check_collision_point_rec(rl.get_mouse_position(), day_rect):
                if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
                    selected_day = datetime(current_year, current_month, day)

# Function to draw the UI
def draw_ui():
    global input_text, text_box_active

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text("Habit Tracker with Calendar", 20, 20, 20, rl.DARKGRAY)

    # Draw habits and checkboxes for the selected day
    rl.draw_text(f"Habits for {selected_day.strftime('%Y-%m-%d')}", 20, 70, 20, rl.DARKGRAY)
    for i, habit in enumerate(habits):
        rl.draw_text(habit, 40, 110 + i * 40, 20, rl.BLACK)
        check_x = 200
        check_y = 110 + i * 40
        if get_day_progress(habit, selected_day):
            rl.draw_rectangle(check_x, check_y, 30, 30, rl.GREEN)
        else:
            rl.draw_rectangle_lines(check_x, check_y, 30, 30, rl.GRAY)

        # Detect click
        if rl.check_collision_point_rec(rl.get_mouse_position(), rl.Rectangle(check_x, check_y, 30, 30)):
            if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
                toggle_day_progress(habit, selected_day)

    # Draw input box for adding a new habit
    input_box_rec = rl.Rectangle(40, 400, 200, 30)
    rl.draw_rectangle_lines_ex(input_box_rec, 1, rl.LIGHTGRAY)
    
    if text_box_active:
        rl.draw_rectangle(input_box_rec.x, input_box_rec.y, input_box_rec.width, input_box_rec.height, rl.LIGHTGRAY)
    rl.draw_text(input_text, 45, 410, 20, rl.DARKGRAY)
    rl.draw_text("Add New Habit:", 40, 370, 20, rl.DARKGRAY)

    # Add habit button
    add_button_rec = rl.Rectangle(260, 400, 100, 30)
    rl.draw_rectangle_rec(add_button_rec, rl.SKYBLUE)
    rl.draw_text("Add Habit", 265, 410, 20, rl.WHITE)

    # Detect clicks for text input and button
    if rl.check_collision_point_rec(rl.get_mouse_position(), input_box_rec):
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            text_box_active = True
    else:
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            text_box_active = False

    if rl.check_collision_point_rec(rl.get_mouse_position(), add_button_rec):
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            add_habit(input_text.strip())
            input_text = ""
            text_box_active = False

    # Draw calendar view
    draw_calendar(500, 100)

    # Draw navigation buttons for calendar
    prev_button_rec = rl.Rectangle(500, 320, 50, 30)
    next_button_rec = rl.Rectangle(700, 320, 50, 30)
    rl.draw_rectangle_rec(prev_button_rec, rl.LIGHTGRAY)
    rl.draw_rectangle_rec(next_button_rec, rl.LIGHTGRAY)
    rl.draw_text("<", 515, 325, 20, rl.BLACK)
    rl.draw_text(">", 715, 325, 20, rl.BLACK)

    # Detect month navigation
    if rl.check_collision_point_rec(rl.get_mouse_position(), prev_button_rec):
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            navigate_month(-1)

    if rl.check_collision_point_rec(rl.get_mouse_position(), next_button_rec):
        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            navigate_month(1)

    rl.end_drawing()

# Function to navigate between months
def navigate_month(delta):
    global current_month, current_year
    current_month += delta
    if current_month < 1:
        current_month = 12
        current_year -= 1
    elif current_month > 12:
        current_month = 1
        current_year += 1

# Initialize window and load data
rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Habit Tracker with Calendar")
rl.set_target_fps(60)
load_habits()

# Main loop
while not rl.window_should_close():
    if text_box_active:
        key = rl.get_char_pressed()
        while key > 0:
            if key == 13:  # Enter key
                add_habit(input_text.strip())
                input_text = ""
                text_box_active = False
            elif key == 8 and len(input_text) > 0:  # Backspace key
                input_text = input_text[:-1]
            elif len(input_text) < INPUT_BUFFER and key >= 32:  # Normal characters
                input_text += chr(key)
            key = rl.get_char_pressed()

    draw_ui()

rl.close_window()

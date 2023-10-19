import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import ctypes
import sys
import json
from PIL import Image, ImageTk

# Function to load the configuration from a JSON file
def load_config():
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
        return config
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save the configuration to a JSON file
def save_config(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

# Function to start moving the window
def start_move(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

# Function to stop moving the window
def stop_move(event):
    x = root.winfo_pointerx() - start_x
    y = root.winfo_pointery() - start_y
    root.geometry(f"+{x}+{y}")

bg_image = Image.open("background.png")

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = bg_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    bg_label.config(image=photo)
    bg_label.image = photo

# Initialize the Tkinter window
root = tk.Tk()
root.title("osu! Mode Switcher")
window_width = 600
window_height = 300
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)  # The window won't be resizable
root.bind('<Configure>', resize_image)
root.configure(bg='#FFD1DC')  # Light pink
root.overrideredirect(True)  # Remove the default title bar
photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = photo

title_bar = tk.Frame(root, bg='pink', relief='raised', bd=2)  # Create a frame for the title bar
title_bar.pack(fill=tk.X)  # Place the title bar at the top of the window
title_label = tk.Label(title_bar, text="osu! Mode Switcher", bg='pink')  # Create a label for the title
title_label.pack(side=tk.LEFT)  # Place the title on the left side of the title bar
close_button = tk.Button(title_bar, text="X", bg='pink', command=root.destroy)  # Create a close button
close_button.pack(side=tk.RIGHT)  # Place the close button on the right side of the title bar
title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", stop_move)
icon_path = "C:\\Users\\samue\\Documents\\GitHub\\osudrawingtoggler\\icon.ico"  # Specify the path to your icon file
root.iconbitmap(default=icon_path)

# Load the configuration
config = load_config()

# Define default paths
default_wacom_folder = "C:\\Program Files\\Tablet\\Wacom\\"
default_open_tablet_driver_folder = "C:\\Users\\samue\\Desktop\\FOLDERS\\Open\\"
default_open_tablet_daemon_path = os.path.join(default_open_tablet_driver_folder, "OpenTabletDriver.Daemon.exe")
default_osu_path = "C:\\Users\\samue\\AppData\\Local\\osu!\\osu!.exe"

# Define the list of Wacom executables with their full paths
wacom_executables = [
    os.path.join(default_wacom_folder, "WacomHost.exe"),
    os.path.join(default_wacom_folder, "Wacom_Tablet.exe"),
    os.path.join(default_wacom_folder, "Wacom_TabletUser.exe"),
    os.path.join(default_wacom_folder, "Wacom_TouchUser.exe"),
    os.path.join(default_wacom_folder, "WTabletServicePro.exe"),
]

# Define the path to the OpenTabletDriver daemon and folder
open_tablet_daemon_path = os.path.join(default_open_tablet_driver_folder, "OpenTabletDriver.Daemon.exe")
open_tablet_driver_folder = default_open_tablet_driver_folder

# Function to update the paths and save the configuration
def update_paths():
    global wacom_folder, open_tablet_driver_folder, open_tablet_driver_path, open_tablet_daemon_path, osu_path

    # Get the paths from user input
    wacom_folder = wacom_path_entry.get()
    open_tablet_driver_folder = open_tablet_driver_path_entry.get()
    open_tablet_driver_path = os.path.join(open_tablet_driver_folder, "OpenTabletDriver.UX.Wpf.exe")
    open_tablet_daemon_path = os.path.join(open_tablet_driver_folder, "OpenTabletDriver.Daemon.exe")
    osu_path = osu_path_entry.get()

    # Update the configuration
    config["wacom_folder"] = wacom_folder
    config["open_tablet_driver_folder"] = open_tablet_driver_folder
    config["open_tablet_driver_path"] = open_tablet_driver_path
    config["open_tablet_daemon_path"] = open_tablet_daemon_path
    config["osu_path"] = osu_path

    # Save the configuration
    save_config(config)

# Function to start osu! mode
def enable_osu_mode():
    global wacom_executables, open_tablet_daemon_path, open_tablet_driver_path, osu_path
    try:
        # Stop Wacom services/drivers
        for executable in wacom_executables:
            try:
                subprocess.run(["taskkill", "/F", "/IM", os.path.basename(executable)], shell=True, check=True)
            except subprocess.CalledProcessError:
                pass

        # Start OpenTabletDriver daemon without opening a console window
        subprocess.Popen([open_tablet_daemon_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=subprocess.STARTUPINFO())

        # Start OpenTabletDriver without opening a console window
        subprocess.Popen([open_tablet_driver_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=subprocess.STARTUPINFO())

        # Start osu!
        subprocess.Popen([osu_path], shell=True)

        # Inform the user that they may need to restart the computer
        log_label.config(text="osu! mode activated. You may need to restart your computer for Wacom to work again.")
    except Exception as e:
        log_label.config(text=f"Error: {str(e)}")

# Create buttons for each mode
osu_mode_button = tk.Button(root, text="Enable osu! mode", command=enable_osu_mode)

# Create labels and entry fields for path configuration
wacom_path_label = tk.Label(root, text="Wacom Folder:")
wacom_path_entry = tk.Entry(root, width=50)
wacom_path_entry.insert(0, config.get("wacom_folder", default_wacom_folder))

open_tablet_driver_path_label = tk.Label(root, text="OpenTabletDriver Folder:")
open_tablet_driver_path_entry = tk.Entry(root, width=50)
open_tablet_driver_path_entry.insert(0, config.get("open_tablet_driver_folder", default_open_tablet_driver_folder))

osu_path_label = tk.Label(root, text="osu! Path:")
osu_path_entry = tk.Entry(root, width=50)
osu_path_entry.insert(0, config.get("osu_path", default_osu_path))

# Create buttons to update paths and save the configuration
update_paths_button = tk.Button(root, text="Update Paths", command=update_paths)

# Create a label for the log
log_label = tk.Label(root, text="", wraplength=400)

# Place buttons, labels, entry fields, and log label in the window
osu_mode_button.pack()
wacom_path_label.pack()
wacom_path_entry.pack()
open_tablet_driver_path_label.pack()
open_tablet_driver_path_entry.pack()
osu_path_label.pack()
osu_path_entry.pack()
update_paths_button.pack()
log_label.pack()

# Start the Tkinter main loop
root.mainloop()

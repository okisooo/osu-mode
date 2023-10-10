import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import ctypes

# Check if the script is running with administrator privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# If the script is not running with administrator privileges, relaunch it with admin rights
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Mode Switcher")

# Define default paths
wacom_folder = "C:\\Program Files\\Tablet\\Wacom\\"
open_tablet_driver_path = "C:\\Users\\samue\\Desktop\\FOLDERS\\Open\\OpenTabletDriver.UX.Wpf.exe"

# Define the list of Wacom executables with their full paths
wacom_executables = [
    os.path.join(wacom_folder, "WacomHost.exe"),
    os.path.join(wacom_folder, "Wacom_Tablet.exe"),
    os.path.join(wacom_folder, "Wacom_TabletUser.exe"),
    os.path.join(wacom_folder, "Wacom_TouchUser.exe"),
    os.path.join(wacom_folder, "WTabletServicePro.exe"),
]

# Function to start osu! mode
def enable_osu_mode():
    global wacom_executables, open_tablet_driver_path
    # Stop Wacom services/drivers
    for executable in wacom_executables:
        subprocess.run(["taskkill", "/F", "/IM", os.path.basename(executable)], shell=True)
    
    # Start OpenTabletDriver
    subprocess.Popen([open_tablet_driver_path], shell=True)

# Function to start Wacom mode
def enable_wacom_mode():
    global open_tablet_driver_path
    # Stop OpenTabletDriver
    subprocess.run(["taskkill", "/F", "/IM", "OpenTabletDriver.UX.Wpf.exe"], shell=True)
    
    # Start Wacom services/drivers
    for executable in wacom_executables:
        subprocess.run([executable], shell=True)

# Function to change Wacom path
def change_wacom_path():
    global wacom_folder
    wacom_folder = filedialog.askdirectory()

# Function to change OpenTabletDriver path
def change_open_tablet_driver_path():
    global open_tablet_driver_path
    open_tablet_driver_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])

# Create buttons for each mode
osu_mode_button = tk.Button(root, text="osu! mode", command=enable_osu_mode)
wacom_mode_button = tk.Button(root, text="Wacom mode", command=enable_wacom_mode)

# Create buttons to change paths
change_wacom_path_button = tk.Button(root, text="Change Wacom Path", command=change_wacom_path)
change_open_tablet_driver_button = tk.Button(root, text="Change OpenTabletDriver Path", command=change_open_tablet_driver_path)

# Place buttons in the window
osu_mode_button.pack()
wacom_mode_button.pack()
change_wacom_path_button.pack()
change_open_tablet_driver_button.pack()

# Start the Tkinter main loop
root.mainloop()

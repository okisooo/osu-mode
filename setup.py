import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # This line hides the console window on Windows

executables = [Executable(
    "toggler.py",  # Replace with your script name
    base=base,
    icon=r"C:\Users\samue\Documents\GitHub\osudrawingtoggler\icon.ico",  # Specify the path to your icon file
    targetName="osu! mode switcher.exe"  # Set the desired executable name
)]

options = {
    "build_exe": {
        "includes": ["tkinter"],
        "packages": ["tkinter", "subprocess", "os", "json"],
        "build_exe": "build_version_1"  # Change this to create a new build directory for each build
    }
}

setup(
    name="osu! Mode Switcher",
    version="1.0",
    description="Turn off Wacom drivers and run OpenTabletDriver and osu!",
    options=options,
    executables=executables
)

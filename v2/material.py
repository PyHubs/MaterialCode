from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkcode import CodeEditor
import os, tkinter as tk
import os
from subprocess import Popen, run, STDOUT, PIPE
from sys import executable
from PIL import Image, ImageTk
from ctypes import windll

"""
Components for app.py
Includes colors and other things
"""

if os.name == "nt":
    code_font = ("Jetbrains Mono", 14)
else:
    code_font = ("Consolas", 14)

# Teal colors
teal_50 = "#E0F2F1"
teal_100 = "#B2DFDB"
teal_200 = "#80CBC4"
teal_300 = "#4DB6AC"
teal_400 = "#26A69A"
teal_500 = "#009688"
teal_600 = "#00897B"
teal_700 = "#00796B"
teal_800 = "#00695C"
teal_900 = "#006064"

# Indigo colors
indigo_50 = "#E8EAF6"
indigo_100 = "#C5CAE9"
indigo_200 = "#9FA8DA"
indigo_300 = "#7986CB"
indigo_400 = "#5C6BC0"
indigo_500 = "#3F51B5"
indigo_600 = "#3949AB"
indigo_700 = "#303F9F"
indigo_800 = "#283593"
indigo_900 = "#1A237E"

# Blue grey from https://materialui.co/colors/
blue_grey_50 = "#ECEFF1"
blue_grey_100 = "#CFD8DC"
blue_grey_200 = "#B0BEC5"
blue_grey_300 = "#90A4AE"
blue_grey_400 = "#78909C"
blue_grey_500 = "#607D8B"
blue_grey_600 = "#546E7A"

blue_grey_700 = "#455A64"
blue_grey_800 = "#37474F"
blue_grey_900 = "#263238"

# Fonts
fonts = ("Product Sans", 14)

# Window configurations
def window_config(root, title, size, color):
    root.title(title)
    root.geometry(size)
    root.configure(background=color)

# If windows
if os.name == "nt":
    import ctypes as ct
    def dark_title_bar(window):
        """
        MORE INFO:
        https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                            ct.sizeof(value))



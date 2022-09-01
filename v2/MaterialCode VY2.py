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


blue_grey = "#22323A"

# Open folder
def open_folder():
    global text, tree

    path = filedialog.askdirectory()
    nodes = dict()

    text.destroy()

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "Treeview", background=deafult,  fieldbackground=deafult, foreground=blue_grey_900, activebackground=deafult,
        font=("Product Sans", 12), bd=0
    )

    style.configure("Treeview.Heading", background=deafult,  fieldbackground=deafult, foreground=blue_grey_900)

    tree.destroy()
    tree = ttk.Treeview(root, height=100)
    tree.heading('#0', text='Project tree', anchor='w')
    tree.pack(side=LEFT, fill='y')

    text = CodeEditor(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)
    text.pack(side=BOTTOM, fill=BOTH, expand=1)

    text.bind("<Control-n>", lambda event: text.delete(1.0, END))
    text.bind("<Control-o>", lambda event: open_file(root, text, open_button))
    text.bind("<Control-s>", lambda event: save_file(root, text, save_button, save_as))
    text.bind("<Control-Shift-s>", lambda event: save_as_function(root, text, save_as))
    text.bind("<Control-Shift-f>", lambda event: open_folder())

    def insert_node(parent, text, abspath):
        node = tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            nodes[node] = abspath
            tree.insert(node, 'end')

    def open_node(event):
        node = tree.focus()
        abspath = nodes.pop(node, None)
        if abspath:
            tree.delete(tree.get_children(node))
            for p in os.listdir(abspath):
                insert_node(node, p, os.path.join(abspath, p))

    def open_file(text):
        global filename
        curItem = tree.focus()
        print(tree.item(curItem))
        eee = tree.item(curItem)
        eeee = eee["text"]

        filename = f"{path}\\{eeee}"

        if os.path.isdir(eeee) == False:
            try:
                if os.path.isfile(filename):
                    if text.get(1.0, END) != open(filename, "r").read():
                        #file_label.config(text=f"  {filename}")
                        root.title(f'Material Code Editor - {filename}')
                        text.delete(1.0, END)
                        text.insert(1.0, open(filename, "r").read())
            except PermissionError: messagebox.showerror("Permission", "Permission denied")
    
            text.pack(fill='both', expand=1)

    abspath = os.path.abspath(path)
    insert_node('', abspath, abspath)
    tree.bind('<<TreeviewOpen>>', open_node)
    tree.bind("<ButtonRelease-1>", lambda event: open_file(text))

# Open file
def open_file(root, text, open_button):
    global filename
    open_button.config(bg=indigo_200)

    # Ask filename
    file = filedialog.askopenfilename(title="Open file")

    if file != '':
        try:
            text.delete(1.0, END)

            # Open file
            text_file = open(file, 'r')
            stuff = text_file.read() # Get text content

            text.insert(END, stuff)
            text_file.close()

            filename = file
            #file_label.config(text=f"  {filename}")
            root.title(f'Material Code Editor - {filename}')
        except Exception as err:
            messagebox.showerror("File Not Found", f"The file you tried to open does not exist??")

# Save as file
def save_as_function(root, text, save_as):
    global filename

    save_as.config(bg=indigo_200)
    global filename
    try:
        file = filedialog.asksaveasfilename(title="Save file")

        files = open(file, 'w')
        files.write(text.get(1.0, END))
        files.close()

        filename = file

        #file_label.config(text=f"  {filename}")
        root.title(f"Material Code Editor - Saved as {filename}")

    except Exception as urmom: print(urmom)

# Save file
def save_file(root, text, save_button, save_as):
    try:
        save_button.config(bg=indigo_200)

        content = text.get(1.0, END)
        
        writes = open(filename, "w")
        writes.write(content)
        writes.close()

        #file_label.config(text=f"  {filename}")
        root.title(f"Material Code Editor - Saved {filename}")

    except Exception as errors:
        save_as_function(root, text, save_as)

# Variables (not material ones)
filename = "Untitled File"
deafult = indigo_400

# Create a window
root = Tk()
root.config(bg=blue_grey)
window_config(root, "Material Code Editor", "750x550", blue_grey)

# Use drak_title_bar, will not work on linux
try: dark_title_bar(root)
except: pass

# Create a topbar
topbar = Frame(root, bg=deafult)
topbar.pack(side=TOP, fill=X)

# New, open, save, save as button on topbar RIGHT SIDE
# Terminal button is only available on linux (because no windows solution found)
if os.name == "posix":
    def bye_terminal():
        termf.pack_forget()
        terminal_btn.bind("<Button-1>", lambda e: run_terminal())

    def run_terminal():
        global text, termf

        terminal_btn.config(bg=indigo_200)
        prev_text = text.get(1.0, END)
        text.destroy()

        # Terminal
        h = root.winfo_screenheight()/4
        termf = Frame(root, height=h, width=root.winfo_screenwidth(), bg=blue_grey)
        termf.pack(side=BOTTOM, fill='x')

        wid = termf.winfo_id()

        text = CodeEditor(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)
        if prev_text != "": text.insert(1.0, prev_text)
        text.pack(side=BOTTOM, fill=BOTH, expand=1)

        text.bind("<Control-n>", lambda event: text.delete(1.0, END))
        text.bind("<Control-o>", lambda event: open_file(root, text, open_button))
        text.bind("<Control-s>", lambda event: save_file(root, text, save_button, save_as))
        text.bind("<Control-Shift-s>", lambda event: save_as_function(root, text, save_as))
        text.bind("<Control-Shift-f>", lambda event: open_folder())

        width = root.winfo_screenwidth()
        height = termf.winfo_screenheight()
        os.system(f"xterm -bg black -fg green -fw consolas -into %d -geometry {height}{width} -sb &" % wid)

        terminal_btn.bind("<Button-1>", lambda e: bye_terminal())

    terminal_btn = Label(topbar, text="  Terminal  ", bg=deafult, fg=blue_grey_900, font=fonts)
    terminal_btn.grid(row=1, column=6)

    terminal_btn.bind("<Enter>", lambda e: terminal_btn.config(bg=indigo_300))
    terminal_btn.bind("<Leave>", lambda e: terminal_btn.config(bg=deafult))
    terminal_btn.bind("<Button-1>", lambda e: run_terminal())
else:
    terminal_btn = Label(topbar, text="  Terminal  ", bg=deafult, fg=blue_grey_900, font=fonts)
    terminal_btn.grid(row=1, column=6)

    def windows_terminal():
        global terminal_btn
        terminal_btn.config(bg=indigo_200)
        Popen("wt.exe")

    terminal_btn.bind("<Enter>", lambda e: terminal_btn.config(bg=indigo_300))
    terminal_btn.bind("<Leave>", lambda e: terminal_btn.config(bg=deafult))
    terminal_btn.bind("<Button-1>", lambda e: windows_terminal())

# Save as
save_as = Label(topbar, text="  Save As  ", bg=deafult, fg=blue_grey_900, font=fonts)
save_as.grid(row=1, column=5)

save_as.bind("<Enter>", lambda event: save_as.config(bg=indigo_300))
save_as.bind("<Leave>", lambda event: save_as.config(bg=deafult))
save_as.bind("<Button-1>", lambda event: save_as_function(root, text, save_as))

# Save button
save_button = Label(topbar, text="  Save  ", bg=deafult, fg=blue_grey_900, font=fonts)
save_button.grid(row=1, column=4)

save_button.bind("<Enter>", lambda event: save_button.config(bg=indigo_300))
save_button.bind("<Leave>", lambda event: save_button.config(bg=deafult))
save_button.bind("<Button-1>", lambda event: save_file(root, text, save_button, save_as))

# New button
new_button = Label(topbar, text="  Clear  ", bg=deafult, fg=blue_grey_900, font=fonts)
new_button.grid(row=1, column=3)

new_button.bind("<Enter>", lambda event: new_button.config(bg=indigo_300))
new_button.bind("<Leave>", lambda event: new_button.config(bg=deafult))
new_button.bind("<Button-1>", lambda event: text.delete(1.0, END))

tree = ttk.Treeview(root, height=100)
tree.heading('#0', text='Project tree', anchor='w')

# Open button
folder_button = Label(topbar, text="  Folder  ", bg=deafult, fg=blue_grey_900, font=fonts)
folder_button.grid(row=1, column=2)

folder_button.bind("<Enter>", lambda event: folder_button.config(bg=indigo_300))
folder_button.bind("<Leave>", lambda event: folder_button.config(bg=deafult))
folder_button.bind("<Button-1>", lambda event: open_folder())

# Open button
open_button = Label(topbar, text="  Open  ", bg=deafult, fg=blue_grey_900, font=fonts)
open_button.grid(row=1, column=1)

open_button.bind("<Enter>", lambda event: open_button.config(bg=indigo_300))
open_button.bind("<Leave>", lambda event: open_button.config(bg=deafult))
open_button.bind("<Button-1>", lambda event: open_file(root, text, open_button))


# Create a code editor
text = CodeEditor(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)
text.bind("<Control-n>", lambda event: text.delete(1.0, END))
text.bind("<Control-o>", lambda event: open_file(root, text, open_button))
text.bind("<Control-s>", lambda event: save_file(root, text, save_button, save_as))
text.bind("<Control-Shift-s>", lambda event: save_as_function(root, text, save_as))
text.bind("<Control-Shift-f>", lambda event: open_folder())

text.insert(1.0, """# # Welcome to Material Code Edittor
# An flat material inspired text editor by Me.

# This editor is the evolution and an arguably nicer version of the "Orcim" which was inspired by
# gedit and looked fine in a way. However it used customtkinter

# However, this version is an huge improvement, with new features, such as sidebars and a new UI
# and line numbers, which took an painstaking amount of time which i will not share

## IMPORTANT
# - The files panel is only a view only. It does not do anything You can hide it by right
# clicking on
# - Click the sidebar button and you can choose to show/hide FILES panel and SHORTCUT sidebar
# - You can also choose to show run button
""")

text.pack(side=BOTTOM, fill=BOTH, expand=1)

if __name__ == "__main__":
    root.update()
    root.mainloop()

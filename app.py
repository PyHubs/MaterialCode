# Import components
from material import *
import os
from subprocess import Popen, run, STDOUT, PIPE
from sys import executable

blue_grey = "#22323A"

# Open file
def open_file(root, text, open_button):
    global filename
    open_button.config(bg=indigo_200)

    # Ask filename
    file = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*txt"), ("Pythonw Files", "*.pyw"), ("Python Files", "*.py"), ("All Files", "*.*")))

    if file != '':
        try:
            text.delete(1.0, END)

            # Open file
            text_file = open(file, 'r')
            stuff = text_file.read() # Get text content

            text.insert(END, stuff)
            text_file.close()

            filename = file
            root.title(f'Material Code Editor - {filename}')
        except Exception as err:
            messagebox.showerror("File Not Found", f"The file you tried to open does not exist??")

# Save as file
def save_as_function(root, text, save_as):
    global filename

    save_as.config(bg=indigo_200)
    global filename
    try:
        file = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*txt"), ("Pythonw Files", "*.pyw"), ("Python Files", "*.py"), ("All Files", "*.*")))

        files = open(file, 'w')
        files.write(text.get(1.0, END))
        files.close()

        filename = file

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

        root.title(f"Material Code Editor - Saved {filename}")

    except Exception as errors:
        save_as_function(root, text, save_as)

# Variables (not material ones)
filename = "Untitled File"
deafult = indigo_400

# Create a window
root = Tk()
root.wm_attributes("-alpha", 0.96)
root.wm_attributes("-transparentcolor", blue_grey)
window_config(root, "Material Code Editor", "750x550", blue_grey)

# Use drak_title_bar, will not work on linux
try: dark_title_bar(root)
except: pass

# Create a topbar
topbar = Frame(root, bg=deafult)
topbar.pack(side=TOP, fill=X)

# Add a file label
file_label = Label(topbar, text=filename, bg=deafult, fg=blue_grey_900, font=fonts)
file_label.pack(side=LEFT, ipadx=10)

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
        termf = Frame(root, height=h, width=root.winfo_screenwidth())
        termf.pack(side=BOTTOM, fill='x')

        wid = termf.winfo_id()

        text = CustomText(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)
        if prev_text != "": text.insert(1.0, prev_text)
        text.pack(side=BOTTOM, fill=BOTH, expand=1)

        width = root.winfo_screenwidth()
        height = termf.winfo_screenheight()
        os.system(f"xterm -bg black -fg green -fw consolas -into %d -geometry {height}{width} -sb &" % wid)

        terminal_btn.bind("<Button-1>", lambda e: bye_terminal())

    terminal_btn = Label(topbar, text="Terminal", bg=deafult, fg=blue_grey_900, font=fonts)
    terminal_btn.pack(side=RIGHT, ipadx=10)

    terminal_btn.bind("<Enter>", lambda e: terminal_btn.config(bg=indigo_300))
    terminal_btn.bind("<Leave>", lambda e: terminal_btn.config(bg=deafult))
    terminal_btn.bind("<Button-1>", lambda e: run_terminal())
else:
    terminal_btn = Label(topbar, text="Terminal", bg=deafult, fg=blue_grey_900, font=fonts)
    terminal_btn.pack(side=RIGHT, ipadx=10)

    def windows_terminal():
        global terminal_btn
        terminal_btn.config(bg=indigo_200)
        Popen("wt.exe")

    terminal_btn.bind("<Enter>", lambda e: terminal_btn.config(bg=indigo_300))
    terminal_btn.bind("<Leave>", lambda e: terminal_btn.config(bg=deafult))
    terminal_btn.bind("<Button-1>", lambda e: windows_terminal())

# Save as
save_as = Label(topbar, text="Save As", bg=deafult, fg=blue_grey_900, font=fonts)
save_as.pack(side=RIGHT, ipadx=10)

save_as.bind("<Enter>", lambda event: save_as.config(bg=indigo_300))
save_as.bind("<Leave>", lambda event: save_as.config(bg=deafult))
save_as.bind("<Button-1>", lambda event: save_as_function(root, text, save_as))

# Save button
save_button = Label(topbar, text="Save", bg=deafult, fg=blue_grey_900, font=fonts)
save_button.pack(side=RIGHT, ipadx=10)

save_button.bind("<Enter>", lambda event: save_button.config(bg=indigo_300))
save_button.bind("<Leave>", lambda event: save_button.config(bg=deafult))
save_button.bind("<Button-1>", lambda event: save_file(root, text, save_button, save_as))

# New button
new_button = Label(topbar, text="Clear", bg=deafult, fg=blue_grey_900, font=fonts)
new_button.pack(side=RIGHT, ipadx=10)

new_button.bind("<Enter>", lambda event: new_button.config(bg=indigo_300))
new_button.bind("<Leave>", lambda event: new_button.config(bg=deafult))
new_button.bind("<Button-1>", lambda event: text.delete(1.0, END))

# Open button
open_button = Label(topbar, text="Open", bg=deafult, fg=blue_grey_900, font=fonts)
open_button.pack(side=RIGHT, ipadx=10)

open_button.bind("<Enter>", lambda event: open_button.config(bg=indigo_300))
open_button.bind("<Leave>", lambda event: open_button.config(bg=deafult))
open_button.bind("<Button-1>", lambda event: open_file(root, text, open_button))

"""# Filebar
filebar = Frame(root, bg=indigo_400)
filebar.pack(side=LEFT, fill='y', anchor='e')

# Get all lists
items = os.listdir()

files_label = Label(filebar, bg=indigo_400, text="Folder", font=fonts, fg=blue_grey_900)
files_label.pack(side=TOP, fill='x')

for item in items: Label(filebar, text=item, bg=indigo_400, fg=blue_grey_900, font=fonts, bd=0, highlightthickness=0).pack(fill='x', ipadx=3, side=TOP)

# Line num frame
line_num_frame = Frame(root, bg=blue_grey_300)
line_num_frame.pack(side=LEFT, fill='y')
line_nums = 1"""

# Create a code editor
text = CustomText(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)

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

linenumbers = TextLineNumbers(root, width=30, bg=blue_grey_600, highlightthickness=0, bd=0)
linenumbers.attach(text)
linenumbers.pack(side="left", fill="y")    
text.pack(side=BOTTOM, fill=BOTH, expand=1)

def _on_change(self):
    linenumbers.redraw()

text.bind("<<Change>>", _on_change)
text.bind("<Configure>", _on_change)

if __name__ == "__main__":
    root.update()
    root.mainloop()

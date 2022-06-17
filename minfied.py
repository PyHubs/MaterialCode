from tkinter import *
from tkinter import messagebox, filedialog
from tkcode import CodeEditor
import os, tkinter as tk
if os.name == "nt": code_font = ("Jetbrains Mono", 14)
else: code_font = ("Consolas", 14)
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
fonts = ("Product Sans", 14)
def window_config(root, title, size, color):
    root.title(title)
    root.geometry(size)
    root.configure(background=color)
if os.name == "nt":
    import ctypes as ct
    def dark_title_bar(window):
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
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
    def attach(self, text_widget):
        self.textwidget = text_widget
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            if int(linenum) >= 100: self.create_text(2,y,anchor="nw", text=linenum, font=("Jebrains Mono", 10))
            else: self.create_text(2,y,anchor="nw", text=linenum, font=("Jebrains Mono", 12))
            i = self.textwidget.index("%s+1line" % i)
class CustomText(CodeEditor):
    def __init__(self, *args, **kwargs):
        CodeEditor.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.createcommand(self._w, self._proxy)
    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert")
        ):
            self.event_generate("<<Change>>", when="tail")
        return result
import os
from subprocess import Popen
blue_grey = "#22323A"
def open_file(root, text, open_button):
    global filename
    open_button.config(bg=indigo_200)
    file = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*txt"), ("Pythonw Files", "*.pyw"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if file != '':
        try:
            text.delete(1.0, END)
            text_file = open(file, 'r')
            stuff = text_file.read() # Get text content
            text.insert(END, stuff)
            text_file.close()
            filename = file
            root.title(f'Material Code Editor - {filename}')
        except Exception as err:
            messagebox.showerror("File Not Found", f"The file you tried to open does not exist??")
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
filename = "Untitled File"
deafult = indigo_400
root = Tk()
root.wm_attributes("-alpha", 0.96)
root.wm_attributes("-transparentcolor", blue_grey)
window_config(root, "Material Code Editor", "750x550", blue_grey)
try: dark_title_bar(root)
except: pass
topbar = Frame(root, bg=deafult)
topbar.pack(side=TOP, fill=X)
file_label = Label(topbar, text=filename, bg=deafult, fg=blue_grey_900, font=fonts)
file_label.pack(side=LEFT, ipadx=10)
if os.name == "posix":
    def bye_terminal():
        termf.pack_forget()
        terminal_btn.bind("<Button-1>", lambda e: run_terminal())
    def run_terminal():
        global text, termf
        terminal_btn.config(bg=indigo_200)
        prev_text = text.get(1.0, END)
        text.destroy()
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
save_as = Label(topbar, text="Save As", bg=deafult, fg=blue_grey_900, font=fonts)
save_as.pack(side=RIGHT, ipadx=10)
save_as.bind("<Enter>", lambda event: save_as.config(bg=indigo_300))
save_as.bind("<Leave>", lambda event: save_as.config(bg=deafult))
save_as.bind("<Button-1>", lambda event: save_as_function(root, text, save_as))
save_button = Label(topbar, text="Save", bg=deafult, fg=blue_grey_900, font=fonts)
save_button.pack(side=RIGHT, ipadx=10)
save_button.bind("<Enter>", lambda event: save_button.config(bg=indigo_300))
save_button.bind("<Leave>", lambda event: save_button.config(bg=deafult))
save_button.bind("<Button-1>", lambda event: save_file(root, text, save_button, save_as))
new_button = Label(topbar, text="Clear", bg=deafult, fg=blue_grey_900, font=fonts)
new_button.pack(side=RIGHT, ipadx=10)
new_button.bind("<Enter>", lambda event: new_button.config(bg=indigo_300))
new_button.bind("<Leave>", lambda event: new_button.config(bg=deafult))
new_button.bind("<Button-1>", lambda event: text.delete(1.0, END))
open_button = Label(topbar, text="Open", bg=deafult, fg=blue_grey_900, font=fonts)
open_button.pack(side=RIGHT, ipadx=10)
open_button.bind("<Enter>", lambda event: open_button.config(bg=indigo_300))
open_button.bind("<Leave>", lambda event: open_button.config(bg=deafult))
open_button.bind("<Button-1>", lambda event: open_file(root, text, open_button))
text = CustomText(root, bg=blue_grey, fg=blue_grey_900, font=code_font, wrap=WORD, insertbackground=deafult, undo=True, maxundo=100)

text.bind("<Control-o>", lambda event: open_file(root, text, open_button))
text.bind("<Control-s>", lambda event: save_file(root, text, save_button, save_as))
text.bind("<Control-Shift-S>", lambda event: save_as_function(root, text, save_as))

text.insert(1.0, """print("Hello world")
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
    try:
        root.update()
        root.mainloop()
    except TclError: 
        messagebox.showwarning("Maximum Undo", "Maximum undo hit")
        root.mainloop()

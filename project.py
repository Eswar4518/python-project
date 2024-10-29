# import tkinter as tk
# from tkinter import filedialog

# class Notepad(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Notepad")
#         self.geometry("500x400")

#         self.text_widget = tk.Text(self)
#         self.text_widget.pack(fill=tk.BOTH, expand=True)

#         self.menu_bar = tk.Menu(self)
#         self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
#         self.file_menu.add_command(label="New", command=self.new_file)
#         self.file_menu.add_command(label="Open", command=self.open_file)
#         self.file_menu.add_command(label="Save", command=self.save_file)
#         self.file_menu.add_command(label="Save As", command=self.save_as_file)
#         self.file_menu.add_separator()
#         self.file_menu.add_command(label="Exit", command=self.quit)
#         self.menu_bar.add_cascade(label="File", menu=self.file_menu)
#         self.config(menu=self.menu_bar)

#         self.filename = None

#     def new_file(self):
#         # Fix the indentation here:
#         self.text_widget.delete(1.0, tk.END)
#         self.filename = None

#     def open_file(self):
#         file_path = tk.filedialog.askopenfilename()
#         if file_path:
#             with open(file_path, 'r') as f:
#                 self.text_widget.delete(1.0, tk.END)
#                 self.text_widget.insert(1.0, f.read())
#             self.filename = file_path

#     def save_file(self):
#         if self.filename:
#             with open(self.filename, 'w') as f:
#                 f.write(self.text_widget.get(1.0, tk.END))
#         else:
#             self.save_as_file()

#     def save_as_file(self):
#         file_path = tk.filedialog.asksaveasfilename(defaultextension='.txt')
#         if file_path:
#             with open(file_path, 'w') as f:
#                 f.write(self.text_widget.get(1.0, tk.END))
#             self.filename = file_path

# if __name__ == "__main__":
#     app = Notepad()
#     app.mainloop()

import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox, simpledialog
import tkinter.font as tkFont

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class TextCrafter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Crafter")
        self.geometry("700x600")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.menu_bar = tk.Menu(self)
        self.create_file_menu()
        self.create_color_menu()
        self.create_font_menu()
        self.config(menu=self.menu_bar)
        self.add_new_tab()

    def create_file_menu(self):
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Tab", command=self.add_new_tab)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_command(label="Rename Tab", command=self.rename_tab)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

    def create_color_menu(self):
        self.color_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.color_menu.add_command(label="Background Color", command=self.change_bg_color)
        self.color_menu.add_command(label="Text Color", command=self.change_text_color)
        self.menu_bar.add_cascade(label="Color", menu=self.color_menu)

    def create_font_menu(self):
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.fonts = list(tkFont.families())  # Get all available font families
        self.font_menu.add_command(label="Change Font", command=self.open_font_selector)
        self.font_menu.add_command(label="Change Font Size", command=self.open_font_size_selector)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)

    def add_new_tab(self):
        new_frame = tk.Frame(self.notebook)
        text_widget = tk.Text(new_frame, bg="lightblue", fg="black", font=("Arial", 12))
        text_widget.pack(fill=tk.BOTH, expand=True)
        close_button = tk.Button(new_frame, text="X", command=lambda: self.close_tab(new_frame), padx=2, fg='red')
        close_button.pack(side=tk.TOP, anchor=tk.E)
        Tooltip(close_button, "Close this tab")
        self.notebook.add(new_frame, text="Untitled")
        self.notebook.select(new_frame)

    def close_tab(self, tab):
        self.notebook.forget(tab)

    def rename_tab(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        current_title = self.notebook.tab(current_tab, "text")
        new_title = simpledialog.askstring("Rename Tab", "Enter new tab name:", initialvalue=current_title)
        if new_title:
            self.notebook.tab(current_tab, text=new_title)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            new_frame = tk.Frame(self.notebook)
            text_widget = tk.Text(new_frame, bg="lightblue", fg="black", font=("Arial", 12))
            text_widget.pack(fill=tk.BOTH, expand=True)
            with open(file_path, 'r') as f:
                text_widget.insert(1.0, f.read())
            close_button = tk.Button(new_frame, text="X", command=lambda: self.close_tab(new_frame), padx=2, fg='red')
            close_button.pack(side=tk.TOP, anchor=tk.E)
            Tooltip(close_button, "Close this tab")
            self.notebook.add(new_frame, text=file_path.split('/')[-1])
            self.notebook.select(new_frame)

    def save_file(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_widget = current_tab.winfo_children()[0]
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(text_widget.get(1.0, tk.END).strip())
            self.notebook.tab(current_tab, text=file_path.split('/')[-1])

    def save_as_file(self):
        self.save_file()  # Save As uses the same function as Save

    def change_bg_color(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            current_tab = self.notebook.nametowidget(self.notebook.select())
            text_widget = current_tab.winfo_children()[0]
            text_widget.config(bg=new_color)

    def change_text_color(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            current_tab = self.notebook.nametowidget(self.notebook.select())
            text_widget = current_tab.winfo_children()[0]
            text_widget.config(fg=new_color)

    def open_font_selector(self):
        font_selector = tk.Toplevel(self)
        font_selector.title("Select Font")
        frame = tk.Frame(font_selector)
        frame.pack(padx=10, pady=10)
        listbox = tk.Listbox(frame, font=('', 12), height=15, width=30)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        for font_family in self.fonts:
            listbox.insert(tk.END, font_family)
        listbox.bind('<<ListboxSelect>>', lambda event: self.set_font_family(listbox.get(listbox.curselection())))
        font_selector.geometry("250x300")

    def open_font_size_selector(self):
        size_selector = tk.Toplevel(self)
        size_selector.title("Select Font Size")
        sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        frame = tk.Frame(size_selector)
        frame.pack(padx=10, pady=10)
        listbox = tk.Listbox(frame, font=('', 12), height=10, width=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        for size in sizes:
            listbox.insert(tk.END, size)
        listbox.bind('<<ListboxSelect>>', lambda event: self.set_font_size(listbox.get(listbox.curselection())))
        size_selector.geometry("100x200")

    def set_font_family(self, font_family):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_widget = current_tab.winfo_children()[0]
        current_size = text_widget.cget("font").split()[1]  # Get current size safely
        text_widget.config(font=(font_family, int(current_size)))

    def set_font_size(self, font_size):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        text_widget = current_tab.winfo_children()[0]
        current_family = text_widget.cget("font").split()[0]  # Get current family safely
        text_widget.config(font=(current_family, font_size))

if __name__ == "__main__":
    app = TextCrafter()
    app.mainloop()

import os
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font
from tkinter.simpledialog import askinteger

class Notepad:
    def __init__(self):
        self.root = Tk()
        self.root.title("Untitled - Notepad")
        self.root.geometry("544x544")

        self.text_area = Text(self.root, font="Helvetica 11")
        self.file = None
        self.text_area.pack(expand=True, fill=BOTH)

        self.menu_bar = Menu(self.root)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_help_menu()
        self.create_format_menu()

        self.root.config(menu=self.menu_bar)

        scroll = Scrollbar(self.text_area)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scroll.set)

    def create_file_menu(self):
        # Create the File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def create_edit_menu(self):
        # Create the Edit menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def change_font(self, font_family):
        # Change the font of the text area
        current_font = font.Font(font=self.text_area["font"])
        current_font.configure(family=font_family)
        self.text_area.configure(font=current_font)

        # Apply the font change to the selected text if it exists
        if self.text_area.tag_ranges(SEL):
            selected_text = self.text_area.get(SEL_FIRST, SEL_LAST)
            self.text_area.tag_configure("custom_font", font=current_font)
            self.text_area.tag_add("custom_font", SEL_FIRST, SEL_LAST)

    def create_format_menu(self):
        # Create the Format menu
        format_menu = Menu(self.menu_bar, tearoff=0)

        font_menu = Menu(format_menu, tearoff=0)
        font_options = ["Arial", "Helvetica", "Times New Roman", "Courier New"]
        for font_name in font_options:
            font_menu.add_command(label=font_name, command=lambda font_name=font_name: self.change_font(font_name))
        format_menu.add_cascade(label="Font", menu=font_menu)

        font_size_menu = Menu(format_menu, tearoff=0)
        font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        for size in font_sizes:
            font_size_menu.add_command(label=str(size), command=lambda size=size: self.change_font_size(size))
        font_size_menu.add_command(label="Change All", command=lambda: self.change_all_font_size())
        format_menu.add_cascade(label="Font Size", menu=font_size_menu)

        self.menu_bar.add_cascade(label="Format", menu=format_menu)

    def change_font_size(self, size):
        # Change the font size of the text area
        current_font = font.Font(font=self.text_area["font"])
        current_font.configure(size=size)
        self.text_area.tag_configure("custom_font", font=current_font)

        # Apply the custom font size to the selected text if it exists
        if self.text_area.tag_ranges(SEL):
            selected_text = self.text_area.get(SEL_FIRST, SEL_LAST)
            self.text_area.tag_add("custom_font", SEL_FIRST, SEL_LAST)

    def change_all_font_size(self):
        # Change the font size of the entire text area
        current_font = font.Font(font=self.text_area["font"])
        selected_font_size = current_font.actual()["size"]
        new_font_size = askinteger("Change All Font Size", "Enter the new font size:", initialvalue=selected_font_size)
        if new_font_size:
            current_font.configure(size=new_font_size)
            self.text_area.configure(font=current_font)

    def change_text_size(self, size):
        # Change the font size of the text area
        current_font = font.Font(font=self.text_area["font"])
        current_font.configure(size=size)
        self.text_area.tag_configure("custom_font", font=current_font)

        # Apply the custom font size to the selected text if it exists
        if self.text_area.tag_ranges(SEL):
            selected_text = self.text_area.get(SEL_FIRST, SEL_LAST)
            self.text_area.tag_add("custom_font", SEL_FIRST, SEL_LAST)

    def create_help_menu(self):
        # Create the Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=self.about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def new_file(self):
        # Create a new file
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, END)

    def open_file(self):
        # Open an existing file
        self.file = askopenfilename(defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"),
                                               ("Text Documents", "*.txt")])
        if self.file:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(1.0, END)
            with open(self.file, "r") as f:
                self.text_area.insert(1.0, f.read())

    def save_file(self):
        # Save the current file
        if not self.file:
            self.file = asksaveasfilename(initialfile='Untitled.txt',
                                          defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"),
                                                     ("Text Documents", "*.txt")])
        if self.file:
            try:
                with open(self.file, "w") as f:
                    f.write(self.text_area.get(1.0, END))
                self.root.title(os.path.basename(self.file) + " - Notepad")
                showinfo("File Saved", "File saved successfully.")
            except IOError:
                showinfo("Error", "An error occurred while saving the file.")

    def quit_app(self):
        # Quit the application
        self.root.destroy()

    def cut(self):
        # Cut the selected text
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        # Copy the selected text
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        # Paste the copied/cut text
        self.text_area.event_generate("<<Paste>>")

    def about(self):
        # Display information about the application
        showinfo("Notepad", "Notepad by code with Pouya")

    def run(self):
        # Run the application
        self.root.mainloop()


if __name__ == "__main__":
    notepad = Notepad()
    notepad.run()

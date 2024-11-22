import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
from datetime import datetime

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip_window, text=self.text, justify=tk.LEFT,
                         background="lightyellow", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 10, "normal"))
        label.pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x550")
        self.root.configure(bg="#f4f4f4")

        # Book List (Each book has Name, Author, Date, and Status)
        self.books = []

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        header_font = font.Font(family="Arial", size=16, weight="bold")
        label_font = font.Font(family="Arial", size=12)

        # Title
        title = tk.Label(self.root, text="Library Management System", font=header_font, bg="#f4f4f4")
        title.pack(pady=10)

        # Form Section
        form_frame = tk.LabelFrame(self.root, text="Add Book", font=label_font, bg="#ffffff", fg="#333333", padx=10, pady=10)
        form_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(form_frame, text="Book Name", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.book_name_entry = tk.Entry(form_frame, width=30)
        self.book_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Author", font=("Arial", 11), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.author_entry = tk.Entry(form_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Date Published", font=("Arial", 11), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.date_published_entry = tk.Entry(form_frame, width=30)
        self.date_published_entry.grid(row=2, column=1, padx=5, pady=5)

        ToolTip(self.book_name_entry, "Enter the name of the book.")
        ToolTip(self.author_entry, "Enter the author's name.")
        ToolTip(self.date_published_entry, "Enter the publication date in YYYY-MM-DD format.")

        # Buttons Section
        button_frame = tk.Frame(self.root, bg="#f4f4f4")
        button_frame.pack(pady=10)

        button_style = {
            "padx": 10, 
            "pady": 5, 
            "bg": "#66b3ff",  # Lighter blue color
            "fg": "white", 
            "font": ("Arial", 11, "bold")
        }

        add_button = tk.Button(button_frame, text="Add Book", **button_style, command=self.add_book)
        add_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Book", **button_style, command=self.delete_book)
        delete_button.grid(row=0, column=1, padx=5)

        check_out_button = tk.Button(button_frame, text="Check Out", **button_style, command=self.check_out_book)
        check_out_button.grid(row=0, column=2, padx=5)

        check_in_button = tk.Button(button_frame, text="Check In", **button_style, command=self.check_in_book)
        check_in_button.grid(row=0, column=3, padx=5)

        ToolTip(add_button, "Click to add a new book to the library.")
        ToolTip(delete_button, "Click to remove the selected book.")
        ToolTip(check_out_button, "Click to check out the selected book.")
        ToolTip(check_in_button, "Click to check in the selected book.")

        # Search Section
        search_frame = tk.LabelFrame(self.root, text="Search Books", font=label_font, bg="#ffffff", fg="#333333", padx=10, pady=10)
        search_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(search_frame, text="Search", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_frame, text="Search", **button_style, command=self.search_books)
        search_button.grid(row=0, column=2, padx=5)

        clear_search_button = tk.Button(search_frame, text="Clear Search", **button_style, command=self.clear_search)
        clear_search_button.grid(row=0, column=3, padx=5)

        ToolTip(self.search_entry, "Enter a keyword to search for books.")
        ToolTip(search_button, "Click to search for books matching the keyword.")
        ToolTip(clear_search_button, "Click to clear the search results and view all books.")

        # Book List Section
        self.book_list_frame = tk.LabelFrame(self.root, text="Books", font=label_font, bg="#ffffff", fg="#333333", padx=10, pady=10)
        self.book_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.book_list = ttk.Treeview(self.book_list_frame, columns=("Name", "Author", "Date", "Status"), show="headings", height=10)
        self.book_list.heading("Name", text="Book Name")
        self.book_list.heading("Author", text="Author")
        self.book_list.heading("Date", text="Date Published")
        self.book_list.heading("Status", text="Status")
        self.book_list.column("Name", width=200)
        self.book_list.column("Author", width=150)
        self.book_list.column("Date", width=120)
        self.book_list.column("Status", width=80)
        self.book_list.pack(fill="both", expand=True)

    # Function to validate date format
    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_book(self):
        name = self.book_name_entry.get().strip()
        author = self.author_entry.get().strip()
        date = self.date_published_entry.get().strip()

        if not name or not author or not date:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        # Validate the date format
        if not self.is_valid_date(date):
            messagebox.showwarning("Input Error", "Please enter a valid date in the format YYYY-MM-DD.")
            return

        self.books.append((name, author, date, "In"))
        self.update_book_list()
        self.book_name_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.date_published_entry.delete(0, tk.END)

    def delete_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No book selected to delete.")
            return
        for item in selected_item:
            book_data = self.book_list.item(item)["values"]
            self.books = [book for book in self.books if not (book[0] == book_data[0] and book[1] == book_data[1])]
        self.update_book_list()

    def search_books(self):
        query = self.search_entry.get().lower()
        filtered_books = [book for book in self.books if query in book[0].lower() or query in book[1].lower() or query in book[2].lower()]
        self.update_book_list(filtered_books)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.update_book_list()

    def update_book_list(self, books_to_display=None):
        for item in self.book_list.get_children():
            self.book_list.delete(item)
        books_to_display = books_to_display if books_to_display is not None else self.books
        for book in books_to_display:
            self.book_list.insert("", tk.END, values=book)

    def check_out_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No book selected for check out.")
            return
        for item in selected_item:
            book_data = self.book_list.item(item)["values"]
            if book_data[3] == "Out":
                messagebox.showwarning("Check Out Error", f"The book '{book_data[0]}' is already checked out.")
                continue
            self.books = [(book[0], book[1], book[2], "Out") if book[0] == book_data[0] and book[1] == book_data[1] else book for book in self.books]
        self.update_book_list()

    def check_in_book(self):
        selected_item = self.book_list.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No book selected for check in.")
            return
        for item in selected_item:
            book_data = self.book_list.item(item)["values"]
            if book_data[3] == "In":
                messagebox.showwarning("Check In Error", f"The book '{book_data[0]}' is already checked in.")
                continue
            self.books = [(book[0], book[1], book[2], "In") if book[0] == book_data[0] and book[1] == book_data[1] else book for book in self.books]
        self.update_book_list()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

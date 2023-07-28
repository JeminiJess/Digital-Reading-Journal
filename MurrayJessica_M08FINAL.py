"""
Author:  Jessica Murray
Date written: 07/23/23
Assignment:   Module 8 FINAL
Short Desc:   Program uses a GUI tkinter application to make a digital reading journal for a user to add
              their read/reading books to.  
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os

class ReadingJournalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Digital Reading Journal")

        # Load the images and resize them
        self.left_image = tk.PhotoImage(file="quill.png").subsample(6)  # Resize by a factor of 6
        self.right_image = tk.PhotoImage(file="book.png").subsample(16)  # Resize by a factor of 16
        self.middle_image = tk.PhotoImage(file="tablet.png").subsample(10) # Resize by a factor of 10

        # Create labels for the images with alternate text
        self.left_image_label = tk.Label(self, image=self.left_image, text="Ink and Quill Pen")
        self.right_image_label = tk.Label(self, image=self.right_image, text="Book PNG Art")
        self.middle_image_label = tk.Label(self, image=self.middle_image, text="Person with Tablet Art")

        # Add a title label
        title_label = tk.Label(self, text="My Reading Journal", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Grid the labels
        self.left_image_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.right_image_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.middle_image_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Initialize 'tree' as a class attribute
        self.tree = None

        # Check if the CSV file exists; if not, create it with headers
        if not os.path.exists("reading_journal.csv"):
            with open("reading_journal.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Author", "Date Started", "Date Finished", "Notes"])
        
        # Create the Treeview instance
        columns = ["Title", "Author", "Date Started", "Date Finished", "Notes"]
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)

        # Set column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Entry fields
        tk.Label(self, text="Book Title *").grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        tk.Label(self, text="Author *").grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        tk.Label(self, text="Date Started *").grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
        tk.Label(self, text="Date Finished *").grid(row=8, column=1, padx=5, pady=5, sticky="nsew")
        tk.Label(self, text="Notes:").grid(row=10, column=1, padx=5, pady=5, sticky="nsew")


        self.entry_title = tk.Entry(self)
        self.entry_title.grid(row=3, column=1, padx=5, pady=5, sticky="nsew") 
        self.entry_author = tk.Entry(self)
        self.entry_author.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
        self.entry_date_started = tk.Entry(self)
        self.entry_date_started.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")
        self.entry_date_finished = tk.Entry(self)
        self.entry_date_finished.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        self.entry_notes = tk.Text(self, height=6, width=30)
        self.entry_notes.grid(row=11, column=1, padx=5, pady=5, sticky="nsew")

        # Add a required label
        title_label = tk.Label(self, text="* indicates required fields", font=("Helvetica", 10, "bold"))
        title_label.grid(row=12, column=1, sticky="nsew")

        # Load the images and resize them
        self.image1 = tk.PhotoImage(file="add.png").subsample(20)  # Resize by a factor of 20
        self.image2 = tk.PhotoImage(file="close.png").subsample(16)  # Resize by a factor of 16
        self.image3 = tk.PhotoImage(file="show.png").subsample(16)  # Resize by a factor of 16

        # Create the "Add Book" button and connect it to the add_book function
        tk.Button(self, image=self.image1, text="Add Book", compound=tk.TOP, command=self.add_book).grid(row=13, column=0, padx=5, pady=5) 

        # Create the "Show Books" button and connect it to the show_books function
        tk.Button(self, image=self.image3, text="Show Books", compound=tk.TOP, command=self.show_books).grid(row=13, column=1, padx=5, pady=5)

        # Create the exit button and connect it to the exit_app function
        tk.Button(self, image=self.image2, text="Exit", compound=tk.TOP, command=self.exit_app).grid(row=13, column=2, padx=5, pady=5)

        # Configure row and column weights to make the widgets expand and fill the available space
        self.grid_rowconfigure(1, weight=1)  # Allow the middle row to expand vertically
        self.grid_columnconfigure(1, weight=1)  # Allow the middle column to expand horizontally

        # Initialize sort_reverse to False
        self.sort_reverse = False

    # Function to add a new book entry
    def add_book(self):
        # Get the input values
        title = self.entry_title.get()
        author = self.entry_author.get()
        date_started = self.entry_date_started.get()
        date_finished = self.entry_date_finished.get()
        notes = self.entry_notes.get("1.0", tk.END).strip()

        # Check if all required fields are filled
        if not (title and author and date_started and date_finished):
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        # Add the book to the CSV file
        with open("reading_journal.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([title, author, date_started, date_finished, notes])

        # Show a success message and ask for confirmation
        result = messagebox.askquestion("Confirmation", "Book added successfully!\nDo you want to add another book?")
        if result == "yes":
            # Clear the input fields for adding another book
            self.entry_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            self.entry_date_started.delete(0, tk.END)
            self.entry_date_finished.delete(0, tk.END)
            self.entry_notes.delete("1.0", tk.END)

    def sort_column(self, header):
        # Get the current data from the Treeview widget
        data = [(self.tree.set(child, header), child) for child in self.tree.get_children('')]

        # Sort the data based on the header column clicked
        data.sort(reverse=self.sort_reverse)
        self.sort_reverse = not self.sort_reverse

        # Rearrange the items in the Treeview based on the sorted data
        for index, (value, child) in enumerate(data):
            self.tree.move(child, '', index)


    # Function to display existing book entries
    def show_books(self):
        try:
            with open("reading_journal.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                books = list(reader)

            # Skip the first row (header row) in the CSV file
            books = books[1:]

            if not books:
                # If there are no books, show a message box and return without creating the window
                messagebox.showinfo("No Entries", "No books recorded yet.")
                return
              
        
            # Destroy the previous "Saved Books" window if it exists
            if hasattr(self, "show_window") and isinstance(self.show_window, tk.Toplevel):
                self.show_window.destroy()

            # Create a new window to display the books
            self.show_window = tk.Toplevel(self)
            self.show_window.title("Saved Books")

            # Create a Treeview to show the books with columns for each book detail
            columns = ["Title", "Author", "Date Started", "Date Finished", "Notes"]
            self.tree = ttk.Treeview(self.show_window, columns=columns, show="headings", height=10)
            self.tree.grid(padx=10, pady=10)

            # Set column headings
            for col in columns:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
                self.tree.column(col, width=150)

            # Grid the Treeview
            self.tree.grid(row=0, column=0, columnspan=len(columns), padx=5, pady=5, sticky="nsew")

            # Create a vertical scrollbar
            scrollbar = ttk.Scrollbar(self.show_window, orient="vertical", command=self.tree.yview)
            scrollbar.grid(row=0, column=len(columns), sticky="ns")
        
            # Configure the Treeview to use the scrollbar
            self.tree.configure(yscrollcommand=scrollbar.set)

           # Add each book to the Treeview
            for book in books:
                if len(book) == len(columns):  # Check if the book entry has all the required fields
                    self.tree.insert("", tk.END, values=book)
 

        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The reading_journal.csv file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")    

    def exit_app(self):
        # Show a confirmation message box when the user clicks the "Exit" button
        result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?")
        if result == "yes":
            self.quit()  # Exit the application if the user clicks "Yes"

if __name__ == "__main__":
    try:
        app = ReadingJournalApp()
        app.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

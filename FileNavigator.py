import tkinter as tk
from tkinter import filedialog
import pandas as pd

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        display_csv(filename)

def display_csv(filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    
    # Create a new window to display the CSV data
    csv_window = tk.Toplevel(root)
    csv_window.title("CSV Viewer")

    # Create a text widget to display the CSV data
    csv_text = tk.Text(csv_window, height=20, width=80)
    csv_text.pack(padx=10, pady=10)

    # Insert the CSV data into the text widget
    csv_text.insert(tk.END, df.to_string(index=False))

# Create the main window
root = tk.Tk()
root.title("CSV File Viewer")

# Create a button to trigger file browsing
browse_button = tk.Button(root, text="Browse CSV", command=browse_file)
browse_button.pack(pady=10)

# Run the application
root.mainloop()


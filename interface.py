import tkinter as tk
from tkinter import filedialog
import csv
import matplotlib.pyplot as plt

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        time, amplitude = [], []
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                if len(row) > 1 and all(map(lambda x: x.replace('.', '').isdigit(), row)):
                    time.append(float(row[0]))
                    amplitude.append(float(row[1]))
        plt.plot(time, amplitude)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Amplitude vs Time')
        plt.show()

root = tk.Tk()
root.title("Interface")
tk.Button(root, text="Browse", command=browse_file).pack(pady=10)
root.mainloop()

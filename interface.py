import tkinter as tk
from tkinter import filedialog, ttk
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Global variables to store the original y-axis limits and ticks
original_y_limits = None
original_y_ticks = None

def browse_file():
    global ax, original_y_limits, original_y_ticks  # Declare ax, original_y_limits, and original_y_ticks as global
    
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        time, amplitude = [], []
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                if len(row) > 1:
                    try:
                        time_value = float(row[0])
                        amplitude_value = float(row[1])
                        time.append(time_value)
                        amplitude.append(amplitude_value)
                    except ValueError:
                        pass
        
        # Plot
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(time, amplitude)
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        ax.set_title('Amplitude vs Time')
        
        # Customize grid properties
        ax.grid(True)
        
        # Set initial number of gridlines
        num_gridlines_x = 11
        num_gridlines_y = 9
        
        # Calculate initial tick spacing based on the number of gridlines
        x_spacing = (max(time) - min(time)) / (num_gridlines_x - 1)
        y_spacing = (max(amplitude) - min(amplitude)) / (num_gridlines_y - 1)
        ax.set_xticks([min(time) + i * x_spacing for i in range(num_gridlines_x)])
        
        # Calculate original y-axis limits such that only 4 grids are used vertically
        y_center = (max(amplitude) + min(amplitude)) / 2
        data_range = max(amplitude) - min(amplitude)
        y_min = y_center - (data_range / 2)
        y_max = y_center + (data_range / 2)
        ax.set_ylim(y_min, y_max)
        
        # Set original y-axis ticks
        ax.set_yticks([y_min + i * (data_range / 4) for i in range(5)])
        
        # Remove tick labels on both axes
        ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
        
        # Embed plot in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create and pack toolbar
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create vertical scrollbar
        scrollbar = ttk.Scrollbar(plot_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create tkinter window
root = tk.Tk()
root.title("Interface")

# Create frame for plot
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# Button to browse file
tk.Button(root, text="Browse", command=browse_file).pack(pady=10)

# Run tkinter event loop
root.mainloop()


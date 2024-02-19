import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk

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
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title('')
        
        # Customize grid properties
        ax.grid(True)
        
        # Set initial number of gridlines
        num_gridlines_x = 11
        num_gridlines_y = 9
        
        # Calculate initial tick spacing based on the number of gridlines
        x_spacing = (max(time) - min(time)) / (num_gridlines_x - 1)
        y_spacing = (max(amplitude) - min(amplitude)) / (num_gridlines_y - 1)
        ax.set_xticks([min(time) + i * x_spacing for i in range(num_gridlines_x)])
        ax.set_yticks([min(amplitude) + i * y_spacing for i in range(num_gridlines_y)])
        
        # Calculate original y-axis limits such that max is 2.5 divisions above center and min is 2.5 divisions below center
        y_center = (max(amplitude) + min(amplitude)) / 2
        data_range = max(amplitude) - min(amplitude)
        original_y_limits = (y_center - 2.5 * (data_range / (num_gridlines_y - 1)), y_center + 2.5 * (data_range / (num_gridlines_y - 1)))
        original_y_ticks = [min(amplitude) + i * y_spacing for i in range(num_gridlines_y)]
        
        # Set original y-axis limits and ticks
        ax.set_ylim(original_y_limits)
        ax.set_yticks(original_y_ticks)
        
        # Set the x-axis limits such that 0 coincides with the y-axis
        ax.set_xlim(0, max(time))
        
        # Customize fourth vertical grid line to be thicker
        gridlines = ax.get_xgridlines()
        for i, line in enumerate(gridlines):
            if i == 5:  # Index 5 corresponds to the sixth grid line (0-indexed)
                line.set_linewidth(2)  # Set linewidth to 2 for the fifth vertical grid line
            else:
                line.set_linewidth(0.5)  # Set default linewidth for other grid lines
        
        # Customize fourth horizontal grid line to be thicker
        gridlines = ax.get_ygridlines()
        for i, line in enumerate(gridlines):
            if i == 4:  # Index 4 corresponds to the fifth grid line (0-indexed)
                line.set_linewidth(2)  # Set linewidth to 2 for the fourth horizontal grid line
            else:
                line.set_linewidth(0.5)  # Set default linewidth for other grid lines
                
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

# Function to perform autoscale
def autoscale():
    global ax, original_y_limits, original_y_ticks  # Access ax, original_y_limits, and original_y_ticks as global
    
    # Reset y-axis limits and ticks to original values
    ax.set_ylim(original_y_limits)
    ax.set_yticks(original_y_ticks)
    
    # Redraw the plot
    plt.draw()

# Create tkinter window
root = tk.Tk()
root.title("Interface")

# Create frame for plot
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# Button to browse file
tk.Button(root, text="Browse", command=browse_file).pack(pady=10)

# Button to perform autoscale
tk.Button(root, text="Autoscale", command=autoscale).pack(pady=5)

# Run tkinter event loop
root.mainloop()



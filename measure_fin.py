import numpy as np
import tkinter as tk
import matplotlib
from tkinter import ttk, filedialog
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class OscilloscopeApp:
    def __init__(self, master):
        self.master = master
        master.title("Oscilloscope")

        # Custom ttk style with a theme and colors
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choose your preferred theme, e.g., 'clam', 'alt', 'default', etc.
        self.style.configure('.', background='lightgray')  # Background color for all elements
        self.style.configure('TButton', foreground='black', background='lightblue', font=('Helvetica', 12, 'bold'))  # Button colors

        # Create figure and axis for the waveform plot
        self.figure, self.axis = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for buttons and labels
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Plot buttons
        self.plot_waveform_button = ttk.Button(self.control_frame, text="Plot Waveform", command=self.load_data)
        self.plot_waveform_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.plot_fft_button = ttk.Button(self.control_frame, text="Plot FFT", command=self.load_data_fft)
        self.plot_fft_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        # Measure buttons
        self.measure_voltage_button = ttk.Button(self.control_frame, text="Measure Voltage", command=self.measure_voltage)
        self.measure_voltage_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.measure_time_button = ttk.Button(self.control_frame, text="Measure Time", command=self.measure_time)
        self.measure_time_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.measure_all_button = ttk.Button(self.control_frame, text="Display All", command=self.display_all)
        self.measure_all_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.clear_button = ttk.Button(self.control_frame, text="Clear Measurements", command=self.clear_measurements)
        self.clear_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.load_data_button = ttk.Button(self.control_frame, text="Load Data", command=self.load_data)
        self.load_data_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        # Label frame for measurements
        self.measurement_frame = ttk.LabelFrame(master, text="Measurements")
        self.measurement_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.voltage_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.voltage_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.time_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.time_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        master.protocol("WM_DELETE_WINDOW", self.quit_app)
    def quit_app(self):
        self.master.destroy()

    def do_fft(self, data):
        # Simulated waveform data (replace with actual data acquisition)
        # waveform_data = np.random.rand(100) * 5  # Simulating 100 samples with voltage range 0-5V

        # Compute FFT of the waveform data
        fft_result = np.fft.fft(data[:, 1])
        N = len(data[:, 0])
        n = np.arange(N)
        T = N / 1000
        freq = n / T

        return data, fft_result, freq

    
    def plot_waveform(self, data, labels):
        if len(labels) < 2:
            print("Error: Insufficient labels provided.")
            return

        x = data[:, 0]  # First column for x-axis
        y = data[:, 1]  # Second column for y-axis

        # Plot the waveform
        self.axis.clear()
        self.axis.plot(x, y, color='blue')
        self.axis.set_title(labels[0] if labels[0] else "Title")  # Title from first row of CSV
        self.axis.set_xlabel(labels[0] if labels[0] else "X-axis")  # X-axis label from first row of CSV
        self.axis.set_ylabel(labels[1] if labels[1] else "Y-axis")  # Y-axis label from second row of CSV
        self.canvas.draw()

    
    def plot_fft(self, fft_result, freq):
        # Compute FFT of the loaded data
        _, fft_result, freq = self.do_fft(self.loaded_data)

        # Plot the FFT
        self.axis.clear()
        self.axis.plot(freq, np.abs(fft_result), color='red')
        self.axis.set_title('FFT of Waveform')
        self.axis.set_xlabel('Frequency (Hz)')
        self.axis.set_ylabel('Amplitude')
        self.canvas.draw()


    def measure_voltage(self):
        if not hasattr(self, 'loaded_data'):
            print("Error: No data loaded.")
            return

        # Calculate voltage measurements
        waveform_data = self.loaded_data[:, 1]  # Assuming voltage data is in the second column
        peak_to_peak_voltage = np.max(waveform_data) - np.min(waveform_data)
        rms_voltage = np.sqrt(np.mean(waveform_data ** 2))
        vmax = np.max(waveform_data)
        vmin = np.min(waveform_data)
        vavg = np.mean(waveform_data)

        # Update label with voltage measurements
        self.voltage_label.config(text=f"Peak-to-Peak Voltage: {peak_to_peak_voltage:.2f} V\n"
                                        f"RMS Voltage: {rms_voltage:.2f} V\n"
                                        f"Vmax: {vmax:.2f} V\n"
                                        f"Vmin: {vmin:.2f} V\n"
                                        f"Vavg: {vavg:.2f} V")

    
    def measure_time(self):
        if not hasattr(self, 'loaded_data'):
            print("Error: No data loaded.")
            return

        # Assuming the data represents a time series with equal time intervals
        time_interval = self.loaded_data[1, 0] - self.loaded_data[0, 0]  # Assuming time data is in the first column
        sampling_rate = 1 / time_interval
        time_period = time_interval
        frequency = 1 / time_period

        # Update label with time measurements
        self.time_label.config(text=f"Frequency: {frequency:.2f} Hz\n"
                                    f"Time Period: {time_period:.4f} s")

    def display_all(self):
        self.measure_voltage()
        self.measure_time()

    def clear_measurements(self):
        self.voltage_label.config(text="")
        self.time_label.config(text="")

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select Data File", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            try:
                self.loaded_data = np.loadtxt(file_path, delimiter=',', skiprows=1)
                labels = np.genfromtxt(file_path, delimiter=',', max_rows=1, dtype=str)
                self.plot_waveform(self.loaded_data, labels)
            except Exception as e:
                print("Error loading data:", e)
    
    def load_data_fft(self):
        file_path = filedialog.askopenfilename(title="Select Data File", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            try:
                self.loaded_data = np.loadtxt(file_path, delimiter=',', skiprows=1)
                labels = np.genfromtxt(file_path, delimiter=',', max_rows=1, dtype=str)
                self.plot_fft(self.loaded_data, labels)
            except Exception as e:
                print("Error loading data:", e)


    def quit_app(self):
            self.master.destroy()


root = tk.Tk()
app = OscilloscopeApp(root)
root.mainloop()

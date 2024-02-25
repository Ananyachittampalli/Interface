import numpy as np
import tkinter as tk
import matplotlib
from tkinter import ttk
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
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Plot buttons
        self.plot_waveform_button = ttk.Button(self.control_frame, text="Plot Waveform", command=self.plot_waveform)
        self.plot_waveform_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.plot_fft_button = ttk.Button(self.control_frame, text="Plot FFT", command=self.plot_fft)
        self.plot_fft_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Measure buttons
        self.measure_voltage_button = ttk.Button(self.control_frame, text="Measure Voltage", command=self.measure_voltage)
        self.measure_voltage_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.measure_time_button = ttk.Button(self.control_frame, text="Measure Time", command=self.measure_time)
        self.measure_time_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.measure_all_button = ttk.Button(self.control_frame, text="Display All", command=self.display_all)
        self.measure_all_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.clear_button = ttk.Button(self.control_frame, text="Clear Measurements", command=self.clear_measurements)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Label frame for measurements
        self.measurement_frame = ttk.LabelFrame(master, text="Measurements")
        self.measurement_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.voltage_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.voltage_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.time_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.time_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

    def generate_random_data(self):
        # Simulated waveform data (replace with actual data acquisition)
        waveform_data = np.random.rand(100) * 5  # Simulating 100 samples with voltage range 0-5V

        # Compute FFT of the waveform data
        fft_result = np.fft.fft(waveform_data)
        N = len(waveform_data)
        n = np.arange(N)
        T = N / 1000
        freq = n / T

        return waveform_data, fft_result, freq

    def plot_waveform(self):
        # Generate random waveform data
        waveform_data, _, _ = self.generate_random_data()

        # Plot the waveform
        self.axis.clear()
        self.axis.plot(waveform_data, color='blue')
        self.axis.set_title('Random Waveform')
        self.canvas.draw()

    def plot_fft(self):
        # Generate random waveform data and its FFT
        _, fft_result, freq = self.generate_random_data()

        # Plot the FFT
        self.axis.clear()
        self.axis.plot(freq, np.abs(fft_result), color='red')
        self.axis.set_title('FFT of Random Waveform')
        self.canvas.draw()

    def measure_voltage(self):
        # Generate random waveform data
        waveform_data, _, _ = self.generate_random_data()

        # Calculate voltage measurements
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
        # Generate random waveform data
        _, _, freq = self.generate_random_data()

        # Calculate frequency and time period
        # Assuming a sampling rate of 1kHz (1000 samples per second)
        sampling_rate = 1000
        time_period = 1 / sampling_rate
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


root = tk.Tk()
app = OscilloscopeApp(root)
root.mainloop()

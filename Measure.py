import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class OscilloscopeApp:
    def __init__(self, master):
        self.master = master
        master.title("Oscilloscope")

        self.waveform_data = None
        self.time_data = None
        self.freq_data = None

        # Custom ttk style with a theme and colors
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='lightgray')
        self.style.configure('TButton', foreground='black', background='lightblue', font=('Helvetica', 12, 'bold'))

        # Create a frame for the graph and buttons
        self.graph_frame = tk.Frame(master)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create figure and axis for the waveform plot
        self.figure, self.axis = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a frame for buttons and checkboxes
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Plot buttons
        self.plot_waveform_button = ttk.Button(self.control_frame, text="Plot Waveform", command=self.plot_waveform)
        self.plot_waveform_button.pack(side=tk.TOP, padx=10, pady=5)

        self.plot_fft_button = ttk.Button(self.control_frame, text="Plot FFT", command=self.plot_fft)
        self.plot_fft_button.pack(side=tk.TOP, padx=10, pady=5)

        # Measurement checkboxes
        self.voltage_var = tk.IntVar()
        self.voltage_checkbox = tk.Checkbutton(self.control_frame, text="Measure Voltage", variable=self.voltage_var)
        self.voltage_checkbox.pack(side=tk.TOP, padx=10, pady=5)

        self.time_var = tk.IntVar()
        self.time_checkbox = tk.Checkbutton(self.control_frame, text="Measure Time", variable=self.time_var)
        self.time_checkbox.pack(side=tk.TOP, padx=10, pady=5)

        # Display selected and display all buttons
        self.display_selected_button = ttk.Button(self.control_frame, text="Display Selected", command=self.display_selected)
        self.display_selected_button.pack(side=tk.TOP, padx=10, pady=5)

        self.display_all_button = ttk.Button(self.control_frame, text="Display All", command=self.display_all)
        self.display_all_button.pack(side=tk.TOP, padx=10, pady=5)

        # Clear button
        self.clear_button = ttk.Button(self.control_frame, text="Clear", command=self.clear_measurements)
        self.clear_button.pack(side=tk.TOP, padx=10, pady=5)

        # Label frame for measurements
        self.measurement_frame = ttk.LabelFrame(master, text="Measurements")
        self.measurement_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.voltage_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.voltage_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        self.time_label = ttk.Label(self.measurement_frame, text="", justify="left")
        self.time_label.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        # Generate and plot sine wave upon initialization
        self.generate_sine_wave(1000, 1, 10)
        self.plot_waveform()

    def generate_sine_wave(self, num_samples, duration, frequency):
        self.time_data = np.linspace(0, duration, num_samples)  # Time values
        self.waveform_data = np.sin(2 * np.pi * frequency * self.time_data)  # Sine wave values

    def plot_waveform(self):
        if self.waveform_data is not None:
            self.axis.clear()
            self.axis.plot(self.time_data, self.waveform_data, color='blue')
            self.axis.set_title('Waveform')
            self.axis.set_xlabel('Time (s)')
            self.axis.set_ylabel('Amplitude')
            self.canvas.draw()

    def plot_fft(self):
        if self.waveform_data is not None:
            fft_result = np.fft.fft(self.waveform_data)
            self.freq_data = np.fft.fftfreq(len(self.waveform_data))
            self.axis.clear()
            self.axis.plot(self.freq_data, np.abs(fft_result), color='red')
            self.axis.set_title('FFT of Waveform')
            self.axis.set_xlabel('Frequency (Hz)')
            self.axis.set_ylabel('Magnitude')
            self.canvas.draw()

    def measure_voltage(self):
        if self.waveform_data is not None:
            peak_to_peak_voltage = np.max(self.waveform_data) - np.min(self.waveform_data)
            amplitude = peak_to_peak_voltage / 2
            rms_voltage = np.sqrt(np.mean(self.waveform_data ** 2))
            average_voltage = np.mean(self.waveform_data)
            voltage_at_specific_point = self.waveform_data[len(self.waveform_data) // 2]  # Voltage at midpoint

            self.voltage_label.config(text=f"Peak-to-Peak Voltage: {peak_to_peak_voltage:.2f} V\n"
                                            f"Amplitude: {amplitude:.2f} V\n"
                                            f"RMS Voltage: {rms_voltage:.2f} V\n"
                                            f"Average Voltage: {average_voltage:.2f} V\n"
                                            f"Voltage at Midpoint: {voltage_at_specific_point:.2f} V")

    def measure_time(self):
        if self.time_data is not None:
            time_period = self.time_data[1] - self.time_data[0]
            frequency = 1 / time_period
            # Placeholder values for rise time, fall time, pulse width, time between two events, and delay between two signals
            rise_time = 0.001
            fall_time = 0.001
            pulse_width = 0.005
            time_between_two_events = 0.01
            delay_between_two_signals = 0.002

            self.time_label.config(text=f"Frequency: {frequency:.2f} Hz\n"
                                        f"Time Period: {time_period:.4f} s\n"
                                        f"Rise Time: {rise_time:.4f} s\n"
                                        f"Fall Time: {fall_time:.4f} s\n"
                                        f"Pulse Width: {pulse_width:.4f} s\n"
                                        f"Time Between Two Events: {time_between_two_events:.4f} s\n"
                                        f"Delay Between Two Signals: {delay_between_two_signals:.4f} s")

    def display_selected(self):
        self.voltage_label.config(text="")
        self.time_label.config(text="")
        if self.voltage_var.get():
            self.measure_voltage()
        if self.time_var.get():
            self.measure_time()

    def display_all(self):
        self.voltage_label.config(text="")
        self.time_label.config(text="")
        self.measure_voltage()
        self.measure_time()

    def clear_measurements(self):
        self.voltage_label.config(text="")
        self.time_label.config(text="")


root = tk.Tk()
app = OscilloscopeApp(root)
root.mainloop()


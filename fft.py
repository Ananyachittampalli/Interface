import matplotlib.pyplot as plt
import numpy as np

# Signal generation

sampling_rate = 1000

sampling_interval = 1/sampling_rate

t = np.arange(0, 1, sampling_interval)

frequency = 3

x = 3 * np.sin(2 * np.pi * frequency * t)

frequency = 6

x += np.sin(2 * np.pi * frequency * t)

frequency = 9


x += 0.9 * np.sin(2 * np.pi * frequency * t)

# FFT of the signal


X = np.fft.fft(x)
N = len(x) # can be adjusted according to convenience
n = np.arange(N)
T = N/sampling_rate
freq = n/T




plt.figure(figsize = (10, 8))
plt.plot(freq, np.abs(X), 'b')
plt.show()

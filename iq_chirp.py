import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# Parameters
fs = 1e9            # Sampling rate: 1 GHz
T = 10e-6           # Chirp duration: 10 microseconds
B = 250e6           # Bandwidth: 250 MHz
K = B / T           # Chirp rate (Hz/s)

# Time vector
t = np.arange(0, T, 1/fs)

# Phase of LFM chirp
phi = 2 * np.pi * (0 * t + 0.5 * K * t**2)
print(phi)

# Generate I/Q signal (complex baseband)
i_signal = np.cos(phi)
q_signal = np.sin(phi)
iq_signal = i_signal + 1j * q_signal

# Instantaneous frequency (numerical derivative of phase)
inst_freq = np.gradient(phi) / (2 * np.pi * (1/fs))

# Combined IQ waveform (e.g., I - Q)
iq_combined = i_signal - q_signal

# DAC parameters (example 12-bit DAC)
dac_bits = 12
dac_max = 2**dac_bits - 1

# Convert I and Q signals to DAC values (scaled and offset to 0 to dac_max)
i_dac = np.round((i_signal + 1) / 2 * dac_max).astype(int)
q_dac = np.round((q_signal + 1) / 2 * dac_max).astype(int)

# --- Plotting ---

plt.figure(figsize=(14, 14))

# 1. I/Q signals
plt.subplot(5, 1, 1)
plt.plot(t * 1e6, i_signal, label='I (cos)')
plt.plot(t * 1e6, q_signal, label='Q (sin)', linestyle='--')
plt.title("Baseband I/Q Chirp Signal")
plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# 2. Instantaneous frequency
plt.subplot(5, 1, 2)
plt.plot(t * 1e6, inst_freq / 1e6)
plt.title("Instantaneous Frequency vs Time")
plt.xlabel("Time (µs)")
plt.ylabel("Frequency (MHz)")
plt.grid()

# 3. Spectrogram
plt.subplot(5, 1, 3)
f, tt, Sxx = spectrogram(iq_signal, fs=fs, nperseg=256, noverlap=128)
plt.pcolormesh(tt * 1e6, f / 1e6, 10 * np.log10(Sxx + 1e-12), shading='gouraud')
plt.title("Spectrogram of Chirp Signal")
plt.xlabel("Time (µs)")
plt.ylabel("Frequency (MHz)")
plt.colorbar(label='Power (dB)')

# 4. Combined IQ waveform (I - Q)
plt.subplot(5, 1, 4)
plt.plot(t * 1e6, iq_combined, label='I - Q (combined)')
plt.title("Combined IQ Waveform (Baseband, before upconversion)")
plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# 5. DAC values for I and Q signals
plt.subplot(5, 1, 5)
plt.plot(t * 1e6, i_dac, label='I DAC values')
plt.plot(t * 1e6, q_dac, label='Q DAC values', linestyle='--')
plt.title("DAC Values for I and Q Signals (12-bit)")
plt.xlabel("Time (µs)")
plt.ylabel("DAC Output (0 to 4095)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

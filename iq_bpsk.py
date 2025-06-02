import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn, firwin

# --- System Parameters ---
bitrate = 5e6             # 5 Mbps
fs = 100e6                # DAC sample rate (100 MHz)
samples_per_symbol = int(fs / bitrate)
num_bits = 100            # Number of bits to simulate

# --- Generate Random Bits and BPSK Modulation ---
bits = np.random.randint(0, 2, num_bits)

# Cos 0 and Cos 180 are 1 -1. Two phase can be represented with just i component
symbols = 2 * bits - 1    # BPSK: 0 -> -1, 1 -> +1

# --- Apply Pulse Shaping (e.g., Raised Cosine or simple FIR) ---
# Use FIR lowpass to simulate pulse shaping for 10 MHz BW
lpf_taps = firwin(101, cutoff=0.2, window="hamming")  # 0.2 * fs/2 = 10 MHz

# Upsample and filter (I channel)
i_waveform = upfirdn(lpf_taps, symbols, samples_per_symbol)
q_waveform = np.zeros_like(i_waveform)  # BPSK has no Q component

# Time vector for plotting
t = np.arange(len(i_waveform)) / fs

# --- Normalize and Convert to DAC Range (12-bit unsigned, e.g., 0–4095) ---
i_norm = (i_waveform - i_waveform.min()) / (i_waveform.max() - i_waveform.min())
i_dac = np.round(i_norm * 4095).astype(np.uint16)

# --- Plotting ---
plt.figure(figsize=(14, 8))

# 1. Bits and symbols
plt.subplot(3, 1, 1)
plt.step(np.arange(num_bits), symbols, where='mid', label='BPSK Symbols')
plt.title("Random BPSK Bitstream")
plt.xlabel("Bit Index")
plt.ylabel("Symbol")
plt.grid()
plt.legend()

# 2. I waveform
plt.subplot(3, 1, 2)
plt.plot(t * 1e6, i_waveform, label="I(t)")
plt.title("Pulse-Shaped BPSK I(t) Waveform")
plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

# 3. DAC Values
plt.subplot(3, 1, 3)
plt.plot(t * 1e6, i_dac, label="DAC Output (12-bit)")
plt.title("DAC-Ready Waveform")
plt.xlabel("Time (µs)")
plt.ylabel("DAC Value (0–4095)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

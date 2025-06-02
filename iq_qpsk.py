import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, upfirdn

# Parameters
num_bits = 100
fs = 100e6  # DAC sampling rate
symbol_rate = 10e6  # 10 Msymbols/s
samples_per_symbol = int(fs / symbol_rate)

# 1. Generate random bits
bits = np.random.randint(0, 2, num_bits)

# 2. Group bits into symbols (2 bits per symbol for QPSK)
bit_pairs = bits.reshape(-1, 2)

# 3. QPSK mapping (sequence is Gray coding)
# 00 → (+1, +1), 01 → (−1, +1), 11 → (−1, −1), 10 → (+1, −1)
mapping = {
    (0, 0): (1, 1),
    (0, 1): (-1, 1),
    (1, 1): (-1, -1),
    (1, 0): (1, -1)
}
symbols_i = []
symbols_q = []

# I⋅cos(2πft) + Q⋅sin(2πft)
for b1, b2 in bit_pairs:
    i, q = mapping[(b1, b2)]
    symbols_i.append(i)
    symbols_q.append(q)

symbols_i = np.array(symbols_i)
symbols_q = np.array(symbols_q)

# 4. Upsample and filter
lpf_taps = firwin(101, cutoff=0.2, window="hamming")  # 0.2 * fs/2 = 10 MHz

i_waveform = upfirdn(lpf_taps, symbols_i, samples_per_symbol)
q_waveform = upfirdn(lpf_taps, symbols_q, samples_per_symbol)

# 5. Create complex baseband signal (IQ)
iq_signal = i_waveform + 1j * q_waveform

# --- Plotting ---
plt.figure(figsize=(12, 8))

# I and Q waveforms
plt.subplot(3, 1, 1)
plt.plot(i_waveform, label="I")
plt.plot(q_waveform, label="Q", linestyle="--")
plt.title("QPSK I and Q Waveforms")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# Constellation
plt.subplot(3, 1, 2)
plt.plot(i_waveform[::samples_per_symbol], q_waveform[::samples_per_symbol], 'o')
plt.title("QPSK Constellation Diagram")
plt.xlabel("I")
plt.ylabel("Q")
plt.axis("equal")
plt.grid()

# Magnitude of DAC-like waveform
plt.subplot(3, 1, 3)
plt.plot(np.abs(iq_signal))
plt.title("Signal Magnitude (for Visualization)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid()

plt.tight_layout()
plt.show()

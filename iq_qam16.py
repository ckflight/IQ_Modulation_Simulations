import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn, fir_filter_design, firwin

# Parameters
num_bits = 1000                  # Total bits to send
M = 16                          # 16-QAM (16 symbols)
k = int(np.log2(M))             # Bits per symbol (4)
fs = 100e6                      # DAC sampling rate (Hz)
symbol_rate = 10e6              # Symbol rate (Hz)
samples_per_symbol = int(fs / symbol_rate)  # Upsampling factor

# Raised Cosine Filter parameters
rolloff = 0.35
span = 10  # Filter length in symbols

def raised_cosine_filter(beta, sps, span):
    N = span * sps + 1
    t = np.linspace(-span / 2, span / 2, N)
    h = np.sinc(t) * np.cos(np.pi * beta * t) / (1 - (2 * beta * t) ** 2)
    # Handle divide by zero at t=±1/(2*beta)
    singularity_points = np.where(np.abs(1 - (2 * beta * t) ** 2) < 1e-10)
    for sp in singularity_points[0]:
        h[sp] = np.pi / 4 * np.sinc(1 / (2 * beta))
    return h / np.sqrt(np.sum(h**2))  # Normalize energy

# 1. Generate random bits
bits = np.random.randint(0, 2, num_bits)

# 2. Group bits into symbols (4 bits per symbol for 16-QAM)
symbols_bits = bits[: (len(bits) // k) * k].reshape(-1, k)

# 3. Map bits to 16-QAM constellation points
# Gray coding and normalized constellation (-3,-1,1,3)
# First 2 bits determine I coordinate, last 2 bits determine Q coordinate.
def bits_to_symbol(b):
    mapping = {
        (0,0): -3,
        (0,1): -1,
        (1,1): 1,
        (1,0): 3
    }
    I = mapping[tuple(b[:2])]
    Q = mapping[tuple(b[2:])]
    return I + 1j*Q

symbols = np.array([bits_to_symbol(b) for b in symbols_bits])
symbols /= np.sqrt((10))  # Normalize power

# 4. Upsample symbols (insert zeros between samples)
upsampled = upfirdn([1], symbols, samples_per_symbol)

# 5. Generate Raised Cosine filter taps
rc_taps = raised_cosine_filter(rolloff, samples_per_symbol, span)

# 6. Pulse shape the upsampled signal
tx_signal = np.convolve(upsampled, rc_taps, mode='same')

# --- Plots ---

plt.figure(figsize=(14, 8))

# Constellation before upsampling/filtering
plt.subplot(2,2,1)
plt.scatter(symbols.real, symbols.imag, color='blue', s=10)
plt.title("16-QAM Constellation (Symbols)")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid()
plt.axis('equal')

# Constellation after pulse shaping (zoomed in to center samples)
plt.subplot(2,2,2)
center_samples = tx_signal[span*samples_per_symbol//2:span*samples_per_symbol//2 + len(symbols)*samples_per_symbol:samples_per_symbol]
plt.scatter(center_samples.real, center_samples.imag, color='red', s=10)
plt.title("16-QAM Constellation (After Pulse Shaping)")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid()
plt.axis('equal')

# Time domain waveform (real part = I channel)
plt.subplot(2,1,2)
t = np.arange(len(tx_signal)) / fs * 1e6  # microseconds
plt.plot(t, tx_signal.real, label='I Channel (Real)')
plt.plot(t, tx_signal.imag, label='Q Channel (Imag)', alpha=0.7)
plt.title("Pulse Shaped 16-QAM Baseband Waveform")
plt.xlabel("Time (µs)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Wi-Fi 802.11a-like OFDM parameters
N = 64                 # FFT size
CP = 16                # Cyclic prefix length
fs = 20e6              # Sampling rate = 20 MHz
num_symbols = 20       # Number of OFDM symbols
mod_order = 4          # QPSK modulation

# Number of active subcarriers (data + pilots)
num_active = 52

# Generate random bits
num_bits = num_active * num_symbols * int(np.log2(mod_order))
bits = np.random.randint(0, 2, num_bits)

# QPSK mapping function
def qpsk_mod(bits):
    bits = bits.reshape((-1, 2))
    mapping = {
        (0,0): 1+1j,
        (0,1): -1+1j,
        (1,1): -1-1j,
        (1,0): 1-1j
    }
    symbols = np.array([mapping[tuple(b)] for b in bits]) / np.sqrt(2)
    return symbols

# Map bits to QPSK symbols
symbols = qpsk_mod(bits)

# Reshape to symbols per OFDM symbol
symbols = symbols.reshape((num_symbols, num_active))

# Prepare OFDM frames with 64 subcarriers: insert zeros for unused carriers
ofdm_frames = np.zeros((num_symbols, N), dtype=complex)

# Wi-Fi 802.11a active subcarriers indices
active_indices = np.hstack((np.arange(1, 27), np.arange(38, 64)))

# Map QPSK symbols to active subcarriers
ofdm_frames[:, active_indices] = symbols

# IFFT to get time domain OFDM symbols
ofdm_time = np.fft.ifft(ofdm_frames, axis=1)

# Add cyclic prefix
ofdm_with_cp = np.hstack([ofdm_time[:, -CP:], ofdm_time])

# Flatten for transmission
tx_signal = ofdm_with_cp.flatten()

# Extract I and Q components (real and imaginary)
i_signal = tx_signal.real
q_signal = tx_signal.imag

# Frequency axis for full sampling rate
freq = np.fft.fftshift(np.fft.fftfreq(len(tx_signal), 1/fs)) / 1e6  # MHz

# FFT of I and Q signals
I_spectrum = np.fft.fftshift(np.fft.fft(i_signal))
Q_spectrum = np.fft.fftshift(np.fft.fft(q_signal))

# ========== Plot 1 to 6 ==========
plt.figure(figsize=(12, 8))
plt.subplot(3, 2, 1)
plt.plot(i_signal[:500], label='I (In-phase)', color='blue')
plt.plot(q_signal[:500], label='Q (Quadrature)', color='orange', alpha=0.7)
plt.title("Time Domain Signal - I and Q Components (First 500 samples)")
plt.xlabel("Sample index")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(freq, np.abs(I_spectrum), label='I Spectrum', color='blue')
plt.plot(freq, np.abs(Q_spectrum), label='Q Spectrum', color='orange', alpha=0.7)
plt.title("Frequency Spectrum - I and Q Components")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Magnitude")
plt.grid()
plt.legend()
plt.xlim(-15, 15)

plt.subplot(3, 2, 3)
plt.scatter(symbols[0].real, symbols[0].imag, color='red', s=20)
plt.title("QPSK Constellation (First OFDM Symbol)")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid()
plt.axis('equal')

f_psd, Pxx = welch(tx_signal, fs=fs, nperseg=1024)
plt.subplot(3, 2, 4)
plt.semilogy(f_psd/1e6, Pxx)
plt.title("Power Spectral Density (PSD) of OFDM Signal")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power/Frequency (dB/Hz)")
plt.grid()
plt.xlim(-15, 15)

symbol_idx = 0
ofdm_sym_with_cp = ofdm_with_cp[symbol_idx]
plt.subplot(3, 2, 5)
plt.plot(np.abs(ofdm_sym_with_cp))
plt.title("Magnitude of OFDM Symbol (with CP)")
plt.xlabel("Sample Index")
plt.ylabel("Magnitude")
plt.grid()

plt.subplot(3, 2, 6)
plt.plot(np.angle(ofdm_sym_with_cp))
plt.title("Phase of OFDM Symbol (with CP)")
plt.xlabel("Sample Index")
plt.ylabel("Phase (radians)")
plt.grid()

plt.tight_layout()
plt.show()

# ========== Plot 7 and 8: Cyclic Prefix and Main Symbol Visualization ==========
plt.figure(figsize=(10, 5))

# Extract one OFDM symbol with CP
symbol_with_cp = ofdm_with_cp[symbol_idx]
cp_part = symbol_with_cp[:CP]
main_part = symbol_with_cp[CP:]

# Plot real parts
plt.plot(np.real(symbol_with_cp), label="OFDM Symbol (Real part)", alpha=0.7)
plt.plot(np.arange(0, CP), np.real(cp_part), label="Cyclic Prefix (CP)", color='red', linewidth=2)
plt.plot(np.arange(CP, CP + len(cp_part)), np.real(main_part[-CP:]), '--', color='green', label="End of Symbol (copy in CP)")

plt.axvline(x=CP, color='black', linestyle='--', label='Start of Main Symbol')

plt.title("Cyclic Prefix and Symbol Overlap (Real Part)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# ========== Plot 9: Subcarrier Sinc Spectra (Orthogonality Visualization) ==========
# Take FFT of one OFDM symbol (without CP)
ofdm_sym = ofdm_time[symbol_idx]
ofdm_fft = np.fft.fftshift(np.fft.fft(ofdm_sym, n=1024))
freq_axis = np.fft.fftshift(np.fft.fftfreq(1024, d=1/fs)) / 1e6  # MHz

plt.figure(figsize=(10, 5))
plt.plot(freq_axis, np.abs(ofdm_fft), label="OFDM Spectrum (Single Symbol)")
plt.title("Subcarrier Sinc Spectra - Orthogonality in OFDM")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Magnitude")
plt.grid()
plt.xlim(-10, 10)
plt.legend()
plt.tight_layout()
plt.show()


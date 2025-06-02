# IQ_Modulation_Simulations
Simple but explanatory python scripths for bpsk qpsk fm(chirp) 16-qam ofdm modulations

# 📡 Digital Modulation Schemes in Python

This repository contains simulations of various digital modulation techniques using Python and NumPy/SciPy. The purpose is to visualize and understand baseband signal characteristics such as waveform shape, frequency spectrum, and constellation diagrams. Each modulation technique includes plots to illustrate its unique properties.

---

## 📁 Contents

- `iq_bpsk.py` – Binary Phase Shift Keying
- `iq_qpsk.py` – Quadrature Phase Shift Keying
- `iq_chirp.py` – Frequency Modulation using Chirp signal
- `iq_qam16.py` – 16-QAM with Raised Cosine Pulse Shaping
- `iq_ofdm.py` – OFDM using QPSK modulation (Wi-Fi 802.11a style)

---

## 1️⃣ BPSK (Binary Phase Shift Keying)

- Maps 1 → +1 and 0 → -1
- Simple real-valued signal
- Spectrum shows sinc-like shape due to rectangular pulse
- Ideal for low-complexity applications

### Explanation:
In BPSK, each bit is represented by a phase of the carrier signal: bit 1 maps to 0° phase (cosine wave), bit 0 maps to 180° phase (inverted cosine). This means only the in-phase (I) component is used; the quadrature (Q) channel remains zero. The modulation effectively flips the amplitude of the cosine carrier, causing a phase shift of π radians. Because of this simple phase inversion, BPSK is robust and easy to implement.

Cos 0 and Cos 180 are 1 -1. Two phases can be represented with just i component.
As a result we are actually flipping/changing the amplitude of the I component.

symbols = 2 * bits - 1    # BPSK: 0 -> -1, 1 -> +1

### Output:
- Time-domain waveform (real-valued)
- Frequency spectrum
- Spectrogram

![Image](https://github.com/user-attachments/assets/cdf530b6-d363-4f47-a86d-abc1ee93bc2b)

---

## 2️⃣ QPSK (Quadrature Phase Shift Keying)

- Each symbol represents 2 bits
- Symbols lie on 4-point constellation in I-Q plane
- In-phase (I) and Quadrature (Q) modulate cosine/sine carriers

### Explanation:
QPSK encodes 2 bits per symbol by using four constellation points separated by 90° phase increments: 0°, 90°, 180°, and 270°. The I component modulates a cosine carrier, while the Q component modulates a sine carrier, making them orthogonal. This way, phase shifts of the combined carrier represent 4 distinct symbol states, doubling data rate compared to BPSK without increasing bandwidth.

QPSK mapping (sequence is Gray coding)
00 → (+1, +1), 01 → (−1, +1), 11 → (−1, −1), 10 → (+1, −1)

Since the overal signal is # I⋅cos(2πft) + Q⋅sin(2πft) each mapped value is assigned to I and Q

### Output:
- Constellation diagram (4 points)
- Time-domain I and Q waveforms
- Spectrum of I and Q components

![Image](https://github.com/user-attachments/assets/cca19359-4097-4a29-863e-35546d6e53a0)

---

## 3️⃣ FM (Chirp Signal)

- Simulates Frequency Modulation using a chirp (linear frequency sweep)
- Signal sweeps from low to high frequency over time
- Not a digital modulation but included to show continuous frequency variation

### Explanation:
Frequency Modulation (FM) encodes information in the instantaneous frequency of the carrier. Here, a chirp signal linearly increases frequency over time, sweeping from a starting frequency to a higher frequency. Unlike phase shift keying, FM uses continuous frequency variation, making it a continuous modulation scheme. The complex baseband representation includes both I and Q components to capture instantaneous phase changes.

### Phase and Frequency Relationship in LFM Chirp

The phase phi(t) in a linear frequency modulated (LFM) chirp is proportional to the square of time (t²), causing the phase to accumulate faster as time increases. This quadratic increase in phase leads to a linearly increasing instantaneous frequency, because frequency is the derivative of phase with respect to time. As a result, the frequency sweeps linearly from a starting value to a higher value, creating the characteristic chirp signal.


phi = 2 * np.pi * (0 * t + 0.5 * K * t**2)

As the phase increases with t changes, the frequency has to increase for phase to change faster.

### Output:
- Time-domain signal
- Spectrogram (shows frequency sweep visually)
- Spectrum

![Image](https://github.com/user-attachments/assets/5704da78-f55b-4541-bccd-9fd2061067da)

---

## 4️⃣ 16-QAM with Raised Cosine Filtering

- 4 bits per symbol → 16 constellation points
- Each axis (I and Q) maps 2 bits via Gray coding
- Raised Cosine filter applied for pulse shaping (bandwidth control)
- Matches real-world DACs with interpolation and filtering

### Explanation:
16-QAM combines amplitude and phase modulation to transmit 4 bits per symbol, resulting in 16 distinct constellation points arranged in a 4x4 grid. Each axis (I and Q) carries 2 bits via Gray coding to minimize bit errors. Both amplitude levels and phase shifts vary to form unique symbols. Raised cosine filtering is applied to smooth the signal transitions, reducing intersymbol interference and controlling bandwidth. The upsampling simulates DAC oversampling before pulse shaping.

### Output:
- 16-QAM constellation (before and after pulse shaping)
- Real/Imaginary time-domain waveform
- Raised Cosine filter improves spectral efficiency

![Image](https://github.com/user-attachments/assets/381df506-9bcf-4f83-96f2-c37f08e2eaf2)

---

## 5️⃣ OFDM with QPSK (Wi-Fi 802.11a Style)

- Uses 64-point FFT, 52 active subcarriers (data + pilot)
- Cyclic Prefix: 16 samples (to combat multipath)
- Modulation: QPSK on each subcarrier
- Demonstrates frequency-domain orthogonality

### Explanation:
Orthogonal Frequency Division Multiplexing (OFDM) splits data across multiple orthogonal subcarriers, each modulated using QPSK. The inverse FFT (IFFT) converts frequency-domain symbols into time-domain samples, combining all subcarriers into a single composite signal. A cyclic prefix (copy of the end of the symbol) is added to mitigate intersymbol interference caused by multipath. This technique improves spectral efficiency and robustness against channel fading.

### Output:
- I/Q waveforms (time domain)
- Frequency spectrum
- QPSK constellation (for one symbol)
- Power Spectral Density (PSD)
- Cyclic Prefix visualization
- Subcarrier sinc shapes (to show orthogonality)

![Image](https://github.com/user-attachments/assets/adb04c2a-47eb-41a9-96c7-236d2cef0b38)

---

Install dependencies via pip:

```bash
pip install numpy matplotlib scipy

# IQ_Modulation_Simulations
Simple but explanatory python scripths for bpsk qpsk fm(chirp) 16-qam ofdm modulations

# 📡 Digital Modulation Schemes in Python

This repository contains simulations of various digital modulation techniques using Python and NumPy/SciPy. The purpose is to visualize and understand baseband signal characteristics such as waveform shape, frequency spectrum, and constellation diagrams. Each modulation technique includes plots to illustrate its unique properties.

---

## 📁 Contents

- `bpsk.py` – Binary Phase Shift Keying
- `qpsk.py` – Quadrature Phase Shift Keying
- `fm_chirp.py` – Frequency Modulation using Chirp signal
- `qam16_raised_cosine.py` – 16-QAM with Raised Cosine Pulse Shaping
- `ofdm_qpsk_wifi.py` – OFDM using QPSK modulation (Wi-Fi 802.11a style)

---

## 1️⃣ BPSK (Binary Phase Shift Keying)

- Maps 1 → +1 and 0 → -1
- Simple real-valued signal
- Spectrum shows sinc-like shape due to rectangular pulse
- Ideal for low-complexity applications

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

### Parameters:
- Symbol rate: 10 MHz
- DAC sampling rate: 100 MHz (10× oversampling)
- Filter: Raised Cosine (roll-off: 0.35)

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

### Parameters:
- Sampling rate: 20 MHz
- FFT size: 64
- CP length: 16
- Active subcarriers: ±26 (Wi-Fi 802.11a style)

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

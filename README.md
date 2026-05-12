# 🎵 Sound Visualizer Pro

A Python-powered real-time audio visualizer that transforms sound into stunning visual displays. Whether you're playing music, speaking into a mic, or analyzing an audio file — watch the waveform come to life.

## ✨ Features

- **Real-Time Visualization**: Live waveform and frequency spectrum display as audio plays
- **Multiple Modes**: Switch between waveform, bar spectrum, and circular visualizations
- **Microphone Input**: Visualize your voice or environment in real time
- **File Playback**: Load and visualize `.mp3`, `.wav`, and other audio files
- **Customizable**: Adjust colors, sensitivity, and visualization style

## 🛠️ Tech Stack

- Python 3.10+
- PyAudio (audio capture)
- NumPy + SciPy (FFT / signal processing)
- Pygame / Matplotlib / Tkinter (rendering)

## 📁 Project Structure

```
soundvisualizer/
├── sound-visualizer-pro/   # Main application
│   ├── main.py             # Entry point
│   ├── visualizer.py       # Rendering engine
│   ├── audio.py            # Audio capture and processing
│   ├── config.py           # Settings and constants
│   └── requirements.txt
└── sound-visualizer.zip    # Packaged release
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A working microphone (for live mode) or audio files

> **Note on PyAudio**: If you have trouble installing PyAudio on Windows, use the prebuilt wheel:
> `pip install pipwin && pipwin install pyaudio`

### Installation

```bash
git clone https://github.com/masteringmachines/soundvisualizer.git
cd soundvisualizer/sound-visualizer-pro
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

**Live microphone mode:**
```bash
python main.py --mode mic
```

**File playback mode:**
```bash
python main.py --mode file --input path/to/your/song.mp3
```

## 🎨 Visualization Modes

| Mode | Description |
|------|-------------|
| `waveform` | Classic oscilloscope-style amplitude over time |
| `spectrum` | Bar chart of frequency components (FFT) |
| `circular` | Radial spectrum — great for music visualization |

Switch modes with the keyboard:
- `W` — Waveform
- `S` — Spectrum
- `C` — Circular
- `Q` — Quit

## ⚙️ Configuration

Edit `config.py` to customize:

```python
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
BAR_COLOR = (0, 200, 255)
BACKGROUND_COLOR = (10, 10, 20)
SENSITIVITY = 1.5
```

## 🤝 Contributing

Ideas welcome: GPU-accelerated rendering, beat detection, color themes, or saving visualizations as video. Open an issue or PR!

## 📝 License

MIT

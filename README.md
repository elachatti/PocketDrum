# 🥁 PocketDrum

PocketDrum is a wearable virtual drum kit that transforms arm movements into realistic drum sounds.

Using two Arduino Nano boards equipped with MPU6050 motion sensors, the system detects arm acceleration and orientation, then converts these gestures into MIDI messages. The MIDI events are sent to Cakewalk, where the SI-Drum Kit virtual instrument produces realistic drum sounds.




# Features

- 🥁 Two independent wireless drumsticks
- 🎯 Motion-based hit detection
- ⚡ Velocity-sensitive playing
- 🧭 Drum selection based on stick orientation
- 🎹 MIDI output compatible with any DAW
- 🎵 Works with Cakewalk and SI Drum Kit
- 🔄 Expandable to more gestures and drum sounds

---

# Hardware

- 2 × Arduino Nano
- 2 × MPU6050 Accelerometer/Gyroscope
- Bluetooth Serial Modules (or USB Serial)
- Drumsticks
- Windows PC

---

# Software

- Arduino IDE
- Python 3
- PySerial
- Mido
- python-rtmidi
- loopMIDI
- Cakewalk Sonar
- SI Drum Kit

---

# Architecture

```
            Left Stick                  Right Stick
         +--------------+           +--------------+
         | Arduino Nano |           | Arduino Nano |
         |   MPU6050    |           |   MPU6050    |
         +------+-------+           +------+-------+
                |                          |
             COM4                       COM3
                \                        /
                 \                      /
                  +--------------------+
                  |   Python Program   |
                  | Hit Detection      |
                  | Velocity Mapping   |
                  | Drum Recognition   |
                  +---------+----------+
                            |
                      Virtual MIDI
                            |
                     PocketDrum 2
                            |
                      Cakewalk Sonar
                            |
                      SI Drum Kit
                            |
                         Speakers
```

---

# Project Structure

```
PocketDrum/
│
├── Arduino/
│   ├── nano_left/
│   │   └── nano_left.ino
│   └── nano_right/
│       └── nano_right.ino
│
├── Python/
│   └── code.py
│
├── Images/
│   ├── setup.jpg
│   ├── hardware.jpg
│   └── demo.gif
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# How It Works

Each Arduino continuously reads motion data from its MPU6050 sensor and sends acceleration and gyroscope measurements to the computer over the serial port.

The Python application:

- Reads data from both drumsticks
- Detects drum hits
- Computes hit velocity
- Identifies the intended drum based on stick orientation
- Sends MIDI Note On/Off messages

Cakewalk receives the MIDI events and plays the corresponding drum sounds using the SI Drum Kit virtual instrument.

---

# Drum Mapping

| Gesture | MIDI Note | Drum |
|----------|-----------|------|
| Center Hit | 38 | Snare |
| Left Swing | 49 | Crash |
| Right Swing | 51 | Ride |
| Downward | 45 | Low Tom |
| Strong Hit | 36 | Kick |
| High Swing | 42 / 46 | Closed/Open Hi-Hat |

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PocketDrum.git
cd PocketDrum
```

---

## 2. Install Python packages

```bash
pip install -r requirements.txt
```

---

## 3. Upload Arduino code

Upload:

- nano_left.ino
- nano_right.ino

using the Arduino IDE.

---

## 4. Configure serial ports

Edit the Python file:

```python
LEFT_PORT = "COM4"
RIGHT_PORT = "COM3"
```

Replace them with your Arduino COM ports.

---

## 5. Start Virtual MIDI

Launch:

- loopMIDI

Create a port named:

```
PocketDrum 2
```

---

## 6. Open Cakewalk

Load:

```
SI Drum Kit
```

Enable MIDI Input Echo.

---

## 7. Run Python

```bash
python code.py
```

Start playing.

---

# Future Improvements

- Bluetooth Low Energy communication
- Better gesture recognition
- Machine Learning for drum classification
- 3D stick visualization
- Automatic calibration
- Recording mode
- Mobile companion app

---

# Technologies

- Arduino Nano
- MPU6050
- Python
- PySerial
- Mido
- MIDI
- loopMIDI
- Cakewalk Sonar
- SI Drum Kit

---

# Author

Ela Chatti

Computer Engineering Student

ISIMM - Higher Institute of Computer Science and Mathematics of Monastir

---

# License

This project is released under the MIT License.# PocketDrum

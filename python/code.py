import serial
import mido
import time
import threading

# ============================================================
# SETTINGS
# ============================================================

LEFT_PORT = "COM4"
RIGHT_PORT = "COM3"
BAUDRATE = 115200

MIDI_PORT = "PocketDrum 2"

midi_lock = threading.Lock()
# ------------------------------------------------------------
# HIT DETECTION
# ------------------------------------------------------------

# Start around 3000-5000.
# Increase if you get false hits.
# Decrease if hits are not detected.
HIT_THRESHOLD = 4500

# Once a hit is detected, wait this long before another hit
COOLDOWN = 0.08

# Signal must fall below this before another hit can occur.
# This prevents one impact from producing multiple notes.
REARM_THRESHOLD = 1800

# ------------------------------------------------------------
# MIDI
# ------------------------------------------------------------

MIN_VELOCITY = 25
MAX_VELOCITY = 127

# Maximum acceleration expected for velocity mapping
VELOCITY_MAX = 14000


# ============================================================
# MIDI
# ============================================================

print("Available MIDI ports:")

for p in mido.get_output_names():
    print("-", p)

port = mido.open_output(MIDI_PORT)

print("Connected t  o:", MIDI_PORT)


# ============================================================
# SERIAL
# ============================================================

left = serial.Serial(
    LEFT_PORT,
    BAUDRATE,
    timeout=0.02
)

right =  serial.Serial(
    RIGHT_PORT,
    BAUDRATE,
    timeout=0.02
)

time.sleep(2)

print("Listening...")


# ============================================================
# STATE
# ============================================================




# ============================================================
# VELOCITY
# ============================================================

def acceleration_to_velocity(value):

    # Limit value
    value = min(value, VELOCITY_MAX)

    # Normalize 0 -> 1
    normalized = value / VELOCITY_MAX

    # Non-linear curve.
    # Makes soft hits easier to play while preserving
    # stronger velocity for hard hits.
    velocity = normalized ** 0.55

    velocity = MIN_VELOCITY + velocity * (
        MAX_VELOCITY - MIN_VELOCITY
    )

    return int(max(MIN_VELOCITY, min(127, velocity)))


# ============================================================
# MAIN LOOP
# ============================================================
def stick_loop(ser, stick):

    last_hit = 0
    armed = True
    peak = 0

    while True:

        try:

            line = ser.readline().decode(
                "ascii",
                errors="ignore"
            ).strip()

            if line[0] != stick:
                continue

            data = line.split(",")

            if len(data) < 8:
                continue

            dx = int(data[1])
            dy = int(data[2])
            dz = int(data[3])

            dynamic = int(data[4])

            gx = int(data[5])
            gy = int(data[6])
            gz = int(data[7])

            now = time.monotonic()

            if not armed:

                if dynamic < REARM_THRESHOLD:
                    armed = True
                    peak = 0

                continue

            if dynamic > peak:
                peak = dynamic

            if dynamic >= HIT_THRESHOLD and (now-last_hit) > COOLDOWN:

                hit_strength = max(dynamic, peak)

                velocity = acceleration_to_velocity(
                    hit_strength
                )

                # -----------------------------
                # LEFT HAND
                # -----------------------------

                if stick == "L":

                    if gx > 150:
                        note = 49
                        drum = "Crash"

                    elif gx < -150:
                        note = 45
                        drum = "Tom"

                    elif gy > 150:
                        note = 38
                        drum = "Snare"

                    else:
                        note = 42
                        drum = "HiHat"

                # -----------------------------
                # RIGHT HAND
                # -----------------------------

                else:

                    if gx > 150:
                        note = 51
                        drum = "Ride"

                    elif gx < -150:
                        note = 47
                        drum = "Mid Tom"

                    elif gy > 150:
                        note = 46
                        drum = "Open HiHat"

                    else:
                        note = 38
                        drum = "Snare"

                if hit_strength > 9000:

                    note = 36
                    drum = "Kick"

                print(
                    f"[{stick}] "
                    f"{drum:<12} "
                    f"Velocity={velocity:3} "
                    f"Hit={hit_strength:5} "
                    f"gx={gx:5} "
                    f"gy={gy:5}"
                )

                with midi_lock:
                    port.send(
                        mido.Message(
                        "note_on",
                        note=note,
                        velocity=velocity
                        )
                    )

                    time.sleep(0.01)

                    port.send(
                        mido.Message(
                        "note_off",
                        note=note
                        )
                    )

                last_hit = now

                armed = False

                peak = 0

        except Exception as e:
            print(e)

left_thread = threading.Thread(
    target=stick_loop,
    args=(left, "L"),
    daemon=True
)

right_thread = threading.Thread(
    target=stick_loop,
    args=(right, "R"),
    daemon=True
)

left_thread.start()
right_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping PocketDrum...")
    left.close()
    right.close()
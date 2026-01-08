"""Generate small test WAV files to verify audio generation code."""
import os
import wave
import struct
import math

SOUND_DIR = os.path.join("..", "assets", "sounds")
AUDIO_SAMPLE_RATE = 44100

os.makedirs(SOUND_DIR, exist_ok=True)

# simple tone generator
def gen(path, freq, duration, volume=0.3):
    n_samples = int(duration * AUDIO_SAMPLE_RATE)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(AUDIO_SAMPLE_RATE)
        for i in range(n_samples):
            t = i / AUDIO_SAMPLE_RATE
            sample = volume * math.sin(2 * math.pi * freq * t)
            val = int(sample * 32767.0)
            wf.writeframes(struct.pack("<h", val))

files = [
    ("stone_age_music.wav", [220, 246, 196, 174], 0.6),
    ("spear.wav", [1200], 0.08),
    ("hit.wav", [300], 0.12),
]

for filename, freqs, dur in files:
    path = os.path.join(SOUND_DIR, filename)
    print("Generating", path)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(AUDIO_SAMPLE_RATE)
        for f in freqs:
            n = int(dur * AUDIO_SAMPLE_RATE)
            for i in range(n):
                t = i / AUDIO_SAMPLE_RATE
                sample = 0.25 * math.sin(2 * math.pi * f * t)
                val = int(sample * 32767.0)
                wf.writeframes(struct.pack("<h", val))

print("Done")

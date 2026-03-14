import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

# --- 1. INFINITE PI GENERATOR (The Engine) ---
def pi_generator():
    """
    Spigot Algorithm: Generates digits of Pi one by one indefinitely 
    using integer arithmetic to maintain precision.
    """
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4 * q + r - t < n * t:
            yield n
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k + 2) + r * l) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr

# --- 2. MUSICAL SETUP (Pentatonic Scale) ---
# Mapping 0-9 digits to a harmonious Pentatonic scale frequencies
# C4, D4, E4, G4, A4, C5, D5, E5, G5, A5
notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00]

def play_pi_note(digit):
    fs = 44100
    duration = 0.2  # Length of each note
    t = np.linspace(0, duration, int(fs * duration))
    
    # Exponential decay envelope to mimic a Piano-like attack/release
    envelope = np.exp(-4 * t / duration)
    wave = 0.4 * np.sin(2 * np.pi * notes[digit] * t) * envelope
    
    sd.play(wave, fs)
    # sd.wait() # Uncomment to force audio-visual synchronization

# --- 3. LIVE GRAPH SETUP ---
plt.ion() # Enable Interactive Mode
fig, ax = plt.subplots(figsize=(12, 6))
window_size = 40 # Number of digits visible on screen simultaneously
data = [0] * window_size

# Initialize Bar chart
bars = ax.bar(range(window_size), data, color='cyan', edgecolor='black')

ax.set_ylim(0, 10)
ax.set_xlim(-1, window_size)
ax.set_title("Infinite Pi Music Visualizer", fontsize=16, color='white')
ax.set_facecolor('#121212') # Dark theme background
fig.patch.set_facecolor('#121212')
ax.tick_params(colors='white')

# --- 4. MAIN LOOP ---
print("Streaming Infinity... Press Ctrl+C to Stop.")
pi_gen = pi_generator()

try:
    count = 0
    for digit in pi_gen:
        # Data Update: Queue system (First-in, First-out)
        data.pop(0)
        data.append(digit)
        
        # UI Update: Update heights and colors for bars
        for i, bar in enumerate(bars):
            bar.set_height(data[i])
            # Dynamic Color Mapping: Changes based on the digit's value
            bar.set_color(plt.cm.magma(data[i] / 10))
        
        # Trigger Audio
        play_pi_note(digit)
        
        # Real-time console output
        if count == 0:
            print(f"{digit}.", end="", flush=True)
        else:
            print(digit, end="", flush=True)
        
        count += 1
        plt.pause(0.01) # Control visual frame rate
        
except KeyboardInterrupt:
    print("\n\nInfinite Music Stopped. Hope you enjoyed the journey!")
    plt.close()
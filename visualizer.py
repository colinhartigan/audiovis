import time
import magichue
import sounddevice as sd
import numpy as np
import time

colors = {
    "red":(255,0,0),
    "blue":(0,0,255),
    "green":(0,255,0),
    "orange":(255,128,0),
    "yellow":(255,255,0),
    "white":(255,255,255),
    "cyan":(0,128,255),
    "pink":(255,0,127),
    "blurple":(114,137,218),
}
duration = 1000000  # seconds

print("Connecting to lights...")
light = magichue.Light('192.168.1.156')  # led ip address
print("Connection established")

if not light.on:
    light.on = True
light.rgb = (0,255,0)
for i in range(2):
    light.rgb = (0,0,0)
    time.sleep(.25)
    light.rgb = (0,255,0)
    time.sleep(.25)

sf = int(input("\nSelect an audio scale factor: "))
bars = input("Show audio data? (Y/N): ")
mode = input("Select a mode (RGB/RAIN/COLOR): ")

if mode.lower() == "color":
    l = input('''  
Choose from the following list:
red
green
blue
white
orange
yellow
cyan
pink
blurple

> ''')
    if l.lower() in colors:
        light.rgb = colors[l]
    else:
        print("\nInvalid selection!\n")

if mode.lower() == "rain":
    light.rgb = (255,0,0)

if mode.lower() == "rgb":
    rgb = input("Select a RGB value, seperated by commas (ex. '100,200,20'): ").split(",")
    light.rgb = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
    
light.brightness = 1

def lights(indata, outdata, frames, time, status = 0):
    vn = np.linalg.norm(indata)*sf
    if vn > 1:
        n = int(vn)
        if n > 255:
            n = 255
        if bars.lower() == "y":
            print(str(n) + "> " + "|" * int(n/2))
        if n > 0:
            light.brightness = n
        else:
            light.brightness = 1
    else:
        light.brightness = 1
    if mode.lower() == "rainbow" or mode.lower() == "rain" and vn / 1000 < 1:
        light.hue = vn / 1000
    elif mode.lower() == "rainbow" or mode.lower() == "rain" and vn / 1000 > 1:
        light.hue = 1

with sd.Stream(callback=lights):
    print("\nAudio visualizer running. Close this window to stop it.")
    sd.sleep(duration * 1000)
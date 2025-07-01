import os
import time
import digitalio
import busio
from board import SCK, MOSI, MISO, CE0, D25, D24, D18
from PIL import Image
from adafruit_rgb_display import ili9341

# Initialize SPI and display
spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)
cs = digitalio.DigitalInOut(CE0)
dc = digitalio.DigitalInOut(D25)
reset = digitalio.DigitalInOut(D24)
backlight = digitalio.DigitalInOut(D18)
backlight.switch_to_output(value=True)

display = ili9341.ILI9341(spi, cs, dc, reset, width=240, height=320)

# GIF folder
gif_folder = "/home/luka/Desktop/gif_player.py"
gifs = [f for f in os.listdir(gif_folder) if f.endswith(".gif")]

# Loop through GIFs
while True:
    for gif_file in gifs:
        gif_path = os.path.join(gif_folder, gif_file)
        try:
            gif = Image.open(gif_path)
            while True:
                try:
                    gif.seek(gif.tell() + 1)
                    frame = gif.convert("RGB")
                    display.image(frame)
                    time.sleep(gif.info.get("duration", 100) / 1000.0)
                except EOFError:
                    gif.seek(0)  # Restart GIF
        except Exception as e:
            print(f"Error with {gif_file}: {e}")
            time.sleep(1)  # Skip bad GIFs
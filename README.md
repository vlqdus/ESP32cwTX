# CONFIGURE MICROPYTHON ON YOUR ESP32
The following files are firmware that should work on most ESP32-based boards with 4MiB or more of flash, including WROOM WROVER, SOLO, PICO, and MINI modules.
https://micropython.org/download/ESP32_GENERIC/
# RUNNING THE main.py FILE ON THE ESP32
1. Install Thonny, a Python IDE for beginners
   - https://thonny.org/
2. Install the ESP32 USB to UART driver
   - https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads
3. Run Thonny IDE
4. Configure the ESP32 interpreter:
   - Run > Configure interpreter > Choose MicroPython (ESP32) > Select the ESP32 COM port (or /dev/ttyACM0, /dev/ttyUSB0 if you're on linux, check with `dmesg | tail -20`, should look something like this: `usb 1-1.2: ch341-uart converter now attached to ttyUSB0`
5. Open the main.py file:
   - File > Open   and choose the main.py file
6. Once it opened, run it:
   - Run > Run current script (or press F5)
7. To stop the script, press on the red STOP button or:
   - Run > Stop/Restart backend (or press CTRL+F2)

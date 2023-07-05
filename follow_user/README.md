# Calculate Focal Distance
Focal Distance = (Width in pixels * Known Distance) / Width in cm
F = (P * D) / W

## iPad Marker
F = (60pixels x 60cm) / 5cm
F = 720

## A4 Marker
F = (167 pixels x 71 cm) / 15.2 cm
F = 780 cm

100cm
W = 5 cm
D = 100 cm
P = 37 pixels
F = (37 * 100) / 5
F = 740
D = (F * W) / P

# UART SCHEMA

Raspberry PI to ESP32

PI TX -> VERDE
PI RX -> AZUL

PI TX -> ESP32 RX
GPIO 14 -> GPIO 16
GPIO 15 -> GPIO 17


# Install
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libopenblas-dev libblas-dev libatlas-base-dev

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
import serial
import json
import time

def sendOverSerial(serial: serial.Serial, data):
    # Convert data to JSON string
    serialized = json.dumps(data)

    # Concatenate start character and end character to the serialized
    data_bytes = "<" + serialized + "\n"

    # Send image over UART
    serial.write(data_bytes.encode())

if __name__ == "__main__":
    # Configure serial port
    # RX = GPIO15, TX = GPIO14
    print("Configuring serial port...")
    ser = serial.Serial('/dev/serial0', 9600, 8, 'N', 1, timeout=1)

    while True:
        # Sample image data
        image_data = {"horizontal": 0.7, "distance": 50.2}

        sendOverSerial(ser, image_data)

        # Wait for a short time before sending the next image data
        time.sleep(1)

    # Close serial port
    ser.close()

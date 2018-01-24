from network import LoRa
import socket
import time
import binascii
import machine
import struct

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('XX XX XX XX XX XX XX XX'.replace(' ',''))
app_key = binascii.unhexlify('XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX XX'.replace(' ',''))

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet ...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

# Things to do every x seconds
while True:
    s.setblocking(True)

    # send distance
    distance1 = 22
    print("Distance (Metric System)", distance1, "cm")
    distanceString = "d" + str(distance1)
    s.send(b'' + distanceString)

    s.setblocking(False)
    time.sleep(800)
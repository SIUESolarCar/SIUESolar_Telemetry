import can
import can.interfaces.slcan
import cantools

#solarcar_bus = can.interfaces.cantact.CantactBus(channel=0, bitrate=500000)
#socketcand_bus = can.interface.Bus(interface='socketcand', host="10.0.16.15", port=29536, channel="can0")
radio_bus = can.interfaces.slcan.slcanBus(channel="COM3", tty_baudrate=115200)

#f = solarcar_bus.recv(10)


def something():
    # This does a lot of what I have done but all in one fn
    message = can_bus.recv()
    db.decode_message(message.arbitration_id, message.data)


def Something2():
    #can_bus = can.interface.Bus('vcan0', bustype='socketcan')
    data = example_message.encode({'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 1})
    message = can.Message(arbitration_id=example_message.frame_id, data=data)
    can_bus.send(message)


db = cantools.database.load_file('OrionBMS.dbc')

hex_strings = [hex(120), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54)]
# Concatenate the hexadecimal strings together into one string
combined_hex = ''.join(hex_string[2:].zfill(2) for hex_string in hex_strings)
# Convert the combined hexadecimal string into bytes
AllOfTheHex = bytes.fromhex(combined_hex)


message = can.Message(arbitration_id=971, data=AllOfTheHex)


# loop until Ctrl-C
try:
    while True:
        msg = radio_bus.recv()

        radio_bus.send(message)
        print(msg)
except KeyboardInterrupt:
    pass

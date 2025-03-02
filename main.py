import cantact
import cantools
from dotenv import load_dotenv
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import influxdatabase as indb

CANEnable = True

# ------ DB Initialization ------
load_dotenv()
token = os.getenv('Influx_Token')
org = "SIUE Solar Racing Team"
url = os.getenv('Influx_URL')

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ------ CAN BUS Initialization ------
if(CANEnable == True):
    intf = cantact.Interface() # create the interface
    intf.set_bitrate(0, 500000) # set the CAN bitrate
    intf.set_enabled(0, True) # enable channel 0
    intf.start() # start the interface

    db = cantools.database.load_file('dbc/OrionBMS.dbc') # Loads the CAN Database



    #solarcar_bus = can.interfaces.cantact.CantactBus(channel=0, bitrate=500000)
    #socketcand_bus = can.interface.Bus(interface='socketcand', host="10.0.16.15", port=29536, channel="can0")
    #radio_bus = can.interfaces.slcan.slcanBus(channel="COM3", tty_baudrate=115200)


# ------------ Main Loop ------------
while True:
    
    # ------------ CAN BUS ------------
    if(CANEnable == True):
        try:
            # wait for frame with 10 ms timeout
            f = intf.recv(10)
            if f != None:
                if hex(f['id']) == '0x3b' or hex(f['id']) == '0x3cb' or hex(f['id']) == '0x6b2' or hex(f['id']) == '0x3c': 
                    indb.MessageToInflux(db, f, write_api)
                elif hex(f['id']) == '0x3b':
                    print("control Messages")
                else:
                    print("Other Messages")
                f = None # Resets

        except KeyboardInterrupt:
            # ctrl-c pressed, close the interface
            intf.stop()
            break

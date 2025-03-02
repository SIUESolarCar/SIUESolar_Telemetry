def FrameIdList(db):
    '''
    Function to append all the FrameIds from a db to a frame id list
    '''

    FrameIdList = []

    dbc_length = len(db._messages)

    for index in range(dbc_length):
        frame_id_hex = db._messages[index].frame_id
        FrameIdList.append(frame_id_hex)

    return FrameIdList



def MessageToInflux(db, frame, write_api):
    '''
    Decodes and Sends CAN Bus message to the database
    '''

    frame_name = frame.arbitration_id

    message = db.decode_message(frame.arbitration_id, frame.data)

    keys_list = list(message.keys())

    record = influxdb_client.Point(frame_name)
    for datapoints in range(len(message)):
        record = record.field(keys_list[datapoints], message[keys_list[datapoints]])

    try:
        write_api.write(bucket, org, record)
        return 1
    except:
        return -1

import cantools
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os



db = cantools.database.load_file('SolarCar.dbc')

f = intf.recv(10) # wait for frame with 10 ms timeout
if f != None:
    

    db.decode_message(message.arbitration_id, message.data)
    MessageToInflux(db, f, write_api)
    f = None #resets







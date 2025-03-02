import cantools
import json
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "SolarCar"
org = "SIUE Solar Racing Team"

frame_id = 971
hex_strings = [hex(120), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54)]
# Concatenate the hexadecimal strings together into one string
combined_hex = ''.join(hex_string[2:].zfill(2) for hex_string in hex_strings)
# Convert the combined hexadecimal string into bytes
AllOfTheHex = bytes.fromhex(combined_hex)


db = cantools.database.load_file('OrionBMS.dbc')
#print("db._messages:")
#print(db._frame_id_to_message)

#message = db.decode_message(frame_id, AllOfTheHex)

#print(message)

#keys_list = list(message.keys())
#print(keys_list)

#test = ["LowTemperature", "HighTemperature", "SimulatedSOC", "MaxCellNumber", "PackCCL", "PackDCL"]
write_api = 0

#Pack = message['LowTemperature']






#def FrameName(db):
#    frame_name = db.get_message_by_frame_id(frame_id)._name
#    return(frame_name)

def DecodeMessage(db, data):
    message = db.decode_message(frame_id, data)
    return(message)

def UploadMessageToInflux(db, data, write_api):
    '''
    Function that takes the can message and uploads it to the database
    '''

    frame_name = FrameName(db)
    message = DecodeMessage(db, data)

    keys_list = list(message.keys())

    record = influxdb_client.Point(frame_name)
    for datapoints in range(len(message)):
        record = record.field(keys_list[datapoints], message[keys_list[datapoints]])

    print(record)

    #write_api.write(bucket, org, record)



UploadMessageToInflux(db, AllOfTheHex, write_api)
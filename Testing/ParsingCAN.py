import cantools
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os

frame_ids = [] # list of all active frames from each dbc file

def append_frame_ids(path_to_dbc_file:str, main_frame_id_list:list[str]):
    '''
    Function to append all the FrameIds from a dbc file to the main frame id list
    '''
    db = cantools.database.load_file(path_to_dbc_file)
    print(path_to_dbc_file)

    dbc_length = len(db._messages)

    for index in range(dbc_length):
        frame_id_hex = db._messages[index].frame_id
        main_frame_id_list.append(frame_id_hex)

    return main_frame_id_list, db

def append_all_frame_ids(main_frame_id_list:list[str]):
    '''
    Scans the directory for all dbc files then appends all message ids to the main frame id list
    '''
    for file in os.listdir("./"):
        if file.endswith(".dbc"):
            #print(file)
            main_frame_id_list = append_frame_ids(file, main_frame_id_list)[0]
    return(main_frame_id_list)

#print(append_all_frame_ids(frame_ids))


db = cantools.database.load_file("OrionBMS.dbc")



hex_strings = [hex(120), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54), hex(54)]
# Concatenate the hexadecimal strings together into one string
combined_hex = ''.join(hex_string[2:].zfill(2) for hex_string in hex_strings)
# Convert the combined hexadecimal string into bytes
AllOfTheHex = bytes.fromhex(combined_hex)




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


db = cantools.database.load_file('OrionBMS.dbc')

frame_name = 57

if frame_name not in FrameIdList(db):
    print("NAH")
else: 
    print("yep")




#print(list)
#print("db._messages:")
#print(db._frame_id_to_message)

message = db.decode_message(971, AllOfTheHex)

print(message)

#print(message)

#print(message['PackDCL'])

#Scan message for points
#Send Influx

#OrionBMS_PackDCL


def SendOrionBMS2():
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    .field("LowTemperature", 20)
    .field("HighTemperature", 30)
    .field("SimulatedSOC", 40)
    .field("MaxCellNumber", 50)
    .field("PackCCL", 60) # Charge Current Limit
    .field("PackDCL", 70) # Discharge Current Limit

  )
  print(point)

  test = ["LowTemperature", "HighTemperature", "SimulatedSOC", "MaxCellNumber", "PackCCL", "PackDCL"]

  p = influxdb_client.Point("OrionBMS")
  for datapoints in range(6):
      p = p.field(test[datapoints], 60)

  print(p)

  #write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

SendOrionBMS2()
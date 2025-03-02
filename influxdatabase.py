import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

bucket="SolarCar"
org="SIUE Solar Racing Team"

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
        write_api.write(bucket="SolarCar", org=org, record=record)
        return 1
    except:
        return -1

def TelemetryData(write_api):
    print("datatodatabase")

    try:
        write_api.write(bucket="Telemetry", org=org, record=point)
        return 1
    except:
        return -1
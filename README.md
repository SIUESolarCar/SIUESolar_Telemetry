# Introduction
This repository holds the code for the SIUE Solar Car's Onboard Telemetry System.

# Telemetry System Architecture
The SIUE Solar Racing Team's Telemetry System is designed to be very flexible and modular. Using a common time series database and a common database viewer the system is able to scale to the needs of the team. Currently the system consists of three components the trackside radio and the onboard collection device and the server. The system relys on the use of a onboard loRa radio to send data to the tackside radio that talks to the server.

# Onboard Architecture
We are using a Raspberry Pico as our device that is connected to the CAN bus. The main method for data transmission to the server is though the Lora Radio.

# Hardware
- Raspberry Pico W
- USB CAN Bus Module
- SparkFun LoRaSerial

# Setup Process
(Work in progress)
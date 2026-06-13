# Setting up the Raspberry Pi

## Raspberry Pi Operating System
Start by taking the SD card used for the RPi and opening Raspberry Pi Imager on a sperate computer.

1. Plug in the SD Card
2. Start Raspberry Pi Imager
3. Select the RPi used (Raspberry Pi 3)
4. Choose ```Raspberry Pi OS (64-bit)```
5. Select the SD Card
6. Set the hostname to ```SolarTelm```
7. Follow steps as needed
8. Write the Image to the SD Card

## CAN Driver Installation
Insert the module into the Raspberry Pi, modify the start-up script "config.txt".

``` bash
$ sudo nano /boot/firmware/config.txt
```

Add the following content at the end of the file: 
``` bash
#Can Bus Hat
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
```

After saving and exiting, restart the Raspberry Pi:
``` bash
$ sudo reboot
```

Open CAN:
``` bash
$ sudo ip link set can0 up type can bitrate 500000
$ sudo ifconfig can0 txqueuelen 65536
$ sudo ifconfig can0 up
```

## SocketCANd Installation

Install dependencies
``` bash
$ sudo apt-get update
$ sudo apt-get install libconfig-dev
```

Clone the socketcand repository and change to its directory:
``` bash
$ git clone https://github.com/linux-can/socketcand.git
$ cd socketcand/
```

Execute the following commands to configure, build, and install the software:
``` bash
$ meson setup -Dlibconfig=true --buildtype=release build
$ meson compile -C build
$ meson install -C build
```

## Setup the Hotspot and Configure the Network
Set Your Wi-Fi Country Code **Raspberry Pi Configuration -> Localisation tab -> Click WLAN Country**
``` bash
$ sudo raspi-config
```

Create hotspot network replacing the MyPassword placeholder with a hotspot password of your choice:
``` bash
$ sudo nmcli connection add con-name hotspot ifname wlan0 type wifi ssid "SIUESolar"
$ sudo nmcli connection modify hotspot wifi-sec.key-mgmt wpa-psk wifi-sec.psk "MyPassword"
$ sudo nmcli connection modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
$ sudo nmcli con modify hotspot 802-11-wireless-security.pmf 1
$ sudo nmcli connection up hotspot
```

## Test Run
Open CAN:
``` bash
$ sudo ip link set can0 up type can bitrate 500000
$ sudo ifconfig can0 txqueuelen 65536
$ sudo ifconfig can0 up
``` 

Start SocketCANd
``` bash
$ socketcand -v -i can0 -l eth0 -l wlan0
```

Start the TCP and the UDP Forwarder (Untested)
``` bash
$ sudo socat TCP4-LISTEN:29536,fork,reuseaddr TCP4:127.0.0.1:29536 &
$ sudo socat UDP4-RECVFROM:42000,broadcast,fork UDP4-DATAGRAM:255.255.255.255:42000,broadcast &
```
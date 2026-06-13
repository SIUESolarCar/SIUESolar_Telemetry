#!/bin/bash

# Exit immediately if any command fails
set -e

echo "========================================="
echo " Starting SolarTelm Test Runner"
echo "========================================="

# ----------------------------------------------------------------
# 1. Initialize CAN Interface
# ----------------------------------------------------------------
echo "--> Checking status of can0 interface..."

# Look for 'UP' inside the attributes of can0
if ip link show can0 2>/dev/null | grep -q "lower_up"; then
    echo "    can0 is already initialized and UP. Skipping configuration."
else
    echo "    can0 is down or uninitialized. Initializing now..."
    sudo ip link set can0 up type can bitrate 500000
    sudo ifconfig can0 txqueuelen 65536
    sudo ifconfig can0 up
    echo "    can0 is now up and configured."
fi

# ----------------------------------------------------------------
# 2. Start TCP and UDP Forwarders
# ----------------------------------------------------------------
# echo "--> Cleaning up any stale socat instances..."
# sudo killall socat || true

# echo "--> Starting TCP and UDP Forwarders in the background..."
# # TCP Forwarder
# sudo socat TCP4-LISTEN:29536,fork,reuseaddr TCP4:127.0.0.1:29536 &
# # UDP Forwarder
# sudo socat UDP4-RECVFROM:42000,broadcast,fork UDP4-DATAGRAM:255.255.255.255:42000,broadcast &

# echo "    Forwarders are running in the background."

# ----------------------------------------------------------------
# 3. Launch SocketCANd
# ----------------------------------------------------------------
echo "--> Launching SocketCANd (Foreground Mode)..."
echo "    Press CTRL+C at any time to stop the runner."
echo "---------------------------------------------------------"

# Running this without 'sudo' as per your instructions.
# Note: This runs in the foreground so you can watch live logs.
socketcand -v -i can0 -l eth0
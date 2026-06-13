#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "========================================="
echo " Starting SolarTelm Setup Script"
echo "========================================="

# ----------------------------------------------------------------
# 1. CAN Driver Configuration (Modifying config.txt)
# ----------------------------------------------------------------
echo "--> Configuring CAN Driver in config.txt..."

CONFIG_FILE="/boot/firmware/config.txt"
CAN_CONFIG=$(cat << 'EOF'

#Can Bus Hat
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
EOF
)

# Check if the configuration already exists to prevent duplicate entries
if grep -q "mcp2515-can0" "$CONFIG_FILE"; then
    echo "   CAN config already exists in $CONFIG_FILE. Skipping."
else
    echo "$CAN_CONFIG" | sudo tee -a "$CONFIG_FILE" > /dev/null
    echo "   CAN config added successfully."
fi

# ----------------------------------------------------------------
# 2. SocketCANd Installation
# ----------------------------------------------------------------
echo "--> Safely stopping any existing socketcand services..."
# If the service doesn't exist or isn't running, '|| true' ensures the script doesn't crash
systemctl stop socketcand || true

echo "--> Installing SocketCANd dependencies..."
sudo apt-get update
sudo apt-get install -y libconfig-dev git meson build-essential

echo "--> Cloning and building socketcand..."
# Clean up old directory if it exists to prevent git clone errors
if [ -d "socketcand" ]; then
    rm -rf socketcand
fi

git clone https://github.com/linux-can/socketcand.git
cd socketcand/

meson setup -Dlibconfig=true --buildtype=release build
meson compile -C build
sudo meson install -C build
cd .. # Return to original directory

# ----------------------------------------------------------------
# 3. Network & Hotspot Configuration
# ----------------------------------------------------------------
echo "--> Launching raspi-config for WLAN Country setup..."
echo "    [ACTION REQUIRED] Please navigate to: Localisation Options -> WLAN Country"
echo "    Press ENTER when you are ready to open raspi-config..."
read -r

sudo raspi-config

echo "--> Setting up the Wi-Fi Hotspot..."
read -sp "Enter the password you want to use for the 'SIUESolar' hotspot: " HOTSPOT_PWD
echo ""

# Remove existing hotspot connection if it exists to avoid conflicts
sudo nmcli connection delete hotspot || true

sudo nmcli connection add con-name hotspot ifname wlan0 type wifi ssid "SIUESolar"
sudo nmcli connection modify hotspot wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$HOTSPOT_PWD"
sudo nmcli connection modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
sudo nmcli con modify hotspot 802-11-wireless-security.pmf 1
sudo nmcli connection up hotspot

# ----------------------------------------------------------------
# 4. Finalizing & Reboot Prompt
# ----------------------------------------------------------------
echo "========================================="
echo " Setup complete!"
echo "========================================="
echo "The system needs to reboot to apply the CAN driver changes."
echo "After rebooting, you can start the interfaces and test run."
echo ""
read -p "Would you like to reboot now? (y/n): " choice
case "$choice" in 
  y|Y ) echo "Rebooting..."; sudo reboot;;
  * ) echo "Please remember to reboot manually before testing.";;
esac
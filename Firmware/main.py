import time

import MCP2512
import socketcand
import slcan

socketcan = socketcand.socketcand()
socketcan.ap_mode('NAME', 'PASSWORD')

if __name__ == '__main__':

    print("--------------------------------------------------------")
    can = MCP2512.MCP2515()
    print("init...")
    can.Init()
    print("send data...")
    id = 0x123 #max 7ff
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    dlc = 8
    can.Send(id, data, dlc)

    readbuf = []

    while(1):
        readbuf = can.Receive(id)
        print(readbuf)
        time.sleep(0.5)

    print("--------------------------------------------------------")
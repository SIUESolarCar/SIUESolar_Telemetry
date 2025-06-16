import time

import MCP2512
import socketcand
import slcan

Unconnected = True
readbuf = []

if __name__ == '__main__':
    can = MCP2512.MCP2515()
    socketcan = socketcand.socketcand()
    print("init...")
    can.Init()
    #print("send data...")
    id = 0x123 #max 7ff
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    dlc = 8
    can.Send(id, data, dlc)

    while(1):
        Unconnected = socketcan.AcceptCan(Unconnected)
        Msg = socketcan.ReadCan(Unconnected)
        print(Msg)
        readbuf = can.Receive(id)
        print(readbuf)
        #time.sleep(0.5)

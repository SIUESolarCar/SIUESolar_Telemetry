import time
import asyncio

import MCP2512
import socketcand
import slcan

Unconnected = True
readbuf = []

async def SocketCan(socketcan, Unconnected):
    Unconnected = socketcan.AcceptCan(Unconnected)
    Msg = await asyncio.wait_for(socketcan.ReadCan(Unconnected), 5)
    return Msg

async def main():
    task1 = asyncio.create_task(SocketCan(socketcan, Unconnected))
    await task1

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
        #asyncio.run(main())
        Msg, Unconnected = socketcan.ReadCan(Unconnected)
        #Msg = asyncio.run(SocketCan(socketcan, Unconnected))
        if Msg != None:
            print(Msg)
        #readbuf = can.Receive(id)
        #print(readbuf)
        #time.sleep(0.5)

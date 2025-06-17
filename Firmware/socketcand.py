import network
import time
import socket

port = 29536

request = b''

class socketcand():

  def __init__(self):
    socketcand.ap_mode(self, 'SIUE_Orion', 'PASSWORD')
    socketcand.Socket(self)

  def ap_mode(self, ssid, password):
    """
      Description: This is a function to activate AP mode

      Parameters:

      ssid[str]: The name of your internet connection
      password[str]: Password for your internet connection

      Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    #ap.ifconfig(('192.168.4.1','255.255.255.0','192.168.4.1','0.0.0.0'))
    #time.sleep(0.1)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])

  def Socket(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    self.s.bind(('', port))
    self.s.listen(5)
    self.s.settimeout(None)
    
  def AcceptCan(self, Unconnected):
    self.s.settimeout(None)
    while(Unconnected):
      try:
        self.conn, addr = self.s.accept()
      except Exception as e:
        Unconnected = True
        break
      self.conn.send("< hi >")
      print("Connected")
      request = self.conn.recv(1024)
      print(request)
      self.conn.send("< ok >")
      request = self.conn.recv(1024)
      print(request)
      self.conn.send("< ok >")
      Unconnected = False
    self.s.setblocking(False)
    return Unconnected

  def ReadCan(self, Unconnected):
    if(Unconnected == False):
      try:
        request = self.conn.recv(1024)
        if request == b'':
          Unconnected = True
      except Exception as e:
        request = None
        Unconnected = True
    return request, Unconnected
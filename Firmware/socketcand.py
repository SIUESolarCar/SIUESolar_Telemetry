import network
import time
import socket

ip = "127.0.0.1"
port = 29536

class socketcand():

  def __init__(self):
     socketcand.ap_mode(self, 'NAME', 'PASSWORD')
     
  def web_page(self):
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
              <body><h1>Hello World</h1></body></html>
          """
    return html

  # if you do not see the network you may have to power cycle
  # unplug your pico w for 10 seconds and plug it in again
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

      while ap.active() == False:
          pass
      print('AP Mode Is Active, You can Now Connect')
      print('IP Address To Connect to:: ' + ap.ifconfig()[0])

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
      #s.bind(('', 80))
      s.bind(('', port))
      s.listen(5)

      while True:
        conn, addr = s.accept()
        conn.send("< hi >")
        print("Connected")
        request = conn.recv(1024)
        print(request)
        conn.send("< ok >")
        request = conn.recv(1024)
        print(request)
        conn.send("< ok >")
        request = conn.recv(1024)
        print(request)
        conn.send("< ok >")
        request = conn.recv(1024)
        print(request)


      #s.send(b"Hello, world")
      #data = s.recv(1024)

      while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        response = self.web_page()
        conn.send(response)
        conn.close()
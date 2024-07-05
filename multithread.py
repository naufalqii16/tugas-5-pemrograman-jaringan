from socket import *
import socket
import threading
import time
import sys
import logging
from http import HttpServer

httpserver = HttpServer()

def ProcessTheClient(connection,address):
		rcv=""
		while True:
			try:
				data = connection.recv(32)
				if data:
					#merubah input dari socket (berupa bytes) ke dalam string
					#agar bisa mendeteksi \r\n
					d = data.decode()
					rcv=rcv+d
					if rcv[-2:]=='\r\n':
						#end of command, proses string
						# logging.warning("data dari client: {}" . format(rcv))
						hasil = httpserver.proses(rcv)
						#hasil akan berupa bytes
						#untuk bisa ditambahi dengan string, maka string harus di encode
						hasil=hasil+"\r\n\r\n".encode()
						# logging.warning("balas ke  client: {}" . format(hasil))
						#hasil sudah dalam bentuk bytes
						connection.sendall(hasil)
						rcv=""
						connection.close()
						return
				else:
					break
			except OSError as e:
				pass
		connection.close()
		return

def Server(portnumber=8889):
	the_clients = []
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	my_socket.bind(('0.0.0.0', portnumber))
	my_socket.listen(1)
	while True:
		connection, client_address = my_socket.accept()
		logging.warning("connection from {}".format(client_address))
		p = threading.Thread(target=ProcessTheClient, args=(connection, client_address))
		the_clients.append(p)
		p.start()


def main():
	portnumber=8000
	try:
		portnumber=int(sys.argv[1])
	except:
		pass
	svr = Server(portnumber)

if __name__=="__main__":
	main()

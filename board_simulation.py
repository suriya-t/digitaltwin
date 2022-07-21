from time import sleep
import socket
import logging
from random import randint
from sys import exit

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

HOST = "192.168.61.243"
PORT = 8585
connected = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""-------------------Functions-------------------"""

def send_data(client, message) -> int:
	"""Sends utf8 encoded data to the specified client as bytes."""
	return client.send(bytes(message, "utf8"))

def receive_data(client) -> bytes:
	"""Receives Data from client."""
	return client.recv(2)

def connect_to_server():
	global connected
	logging.info("Connection - Connecting to server...")
	while True:
		try:
			client.connect((HOST, PORT))
			connected = True
			logging.info("Connection - Connected with server")
			return
		
		except KeyboardInterrupt:
			exit()

		except socket.error:
			logging.info("Connection - Can't connect to server.")
			sleep(3)
			continue

def next():
	global connected
	i=0
	while True:
		try:
			if i==35:
				i=0
			data = "{:02d}".format(i)
			nob = send_data(client, data)
			logging.info(f"nob={nob} , data sent = {data}")
			sleep(.05)
			i+=1
			continue
		
		except KeyboardInterrupt:
			client.close()
			return
		
		except socket.error:  
				# set connection status and recreate socket  
			connected = False  
			clientSocket = socket.socket()  
			logging.info( "connection lost... reconnecting" )  
			while not connected:  
				# attempt to reconnect, otherwise sleep for 3 seconds  
				try:  
					clientSocket.connect( ( HOST, PORT ) )  
					connected = True  
					logging.info( "re-connection successful" )
					continue
				except socket.error:  
					sleep( 3 )
			continue

		# except ConnectionResetError:
		# 	# thrown by receive_data()
		# 	logging.info("Connection - Server disconnected.")
		# 	connect_to_server()

		# except Exception as e:
		# 	# any unexpected error stops program execution
		# 	logging.error(e)
		# 	logging.info("Connection - Closing the connection.")
		# 	client.close()
		# 	logging.info("Connection - Connection closed.")
		# 	logging.info("Ending the program.")
		# 	return

"""-----------------------------------------------"""

if __name__ == '__main__':
	connect_to_server()

	next()


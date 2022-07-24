# Server-Client Program
# -----Server-------

import socket
import logging
from sys import exit

PORT:int = 8585
nob:int = 0
isScreenConnected:bool = False
isBoardConnected:bool = False
screen = None
board = None

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

Server = socket.socket()
Server.bind(("0.0.0.0", PORT))
Server.listen(1)
print("Server started")

"""-------------------Functions-------------------"""

def flush(client) -> None:
	"""flushes the inputs buffer."""
	client.recv(5000)

def send_data(client, message) -> int:
	"""Sends utf8 encoded data to the specified client as bytes."""
	return client.send(message)


def receive_data(client) -> bytes:
	"""Receives Data from client."""
	return client.recv(2)


# Closes all connections made.
def closeConnections(clients:list, client=None) -> None:
	for i in range(2):
		if clients[i]:
			clients[i][0].close()
	return [None, None]

def connect(clients, board, screen):
	# Connect to board and Screen.
	global isBoardConnected
	global isScreenConnected

	if not isBoardConnected:
		clients[0] = None
		logging.info("Re-Connecting to board.")
		clients[0]=Server.accept()
		board = clients[0][0]
		logging.info(f"Connected with {clients[0][1]}")
		isBoardConnected = True

	if not isScreenConnected:
		clients[1] = None
		logging.info("Re-Connecting to screen.")
		clients[1]=Server.accept()
		screen = clients[1][0]
		logging.info(f"\nConnected with {clients[1][1]}")
		isScreenConnected = True

	return clients, board, screen

"""-----------------------------------------------"""

clients = [None, None]
clients[0]=Server.accept()
board = clients[0][0]
logging.info(f"Connected with {clients[0][1]}")
isBoardConnected = True

clients[1]=Server.accept()
screen = clients[1][0]
logging.info(f"\nConnected with {clients[1][1]}")
isScreenConnected = True

flush(board)




while True:
	try:
		data = board.recv(2)
		if data and isScreenConnected:
			try:
				nob = screen.send(data)
				logging.info(f"no_of_bits_sent = {nob} , data_sent = {str(data)}")
				if not nob:
					logging.info("No data sent to screen. Screen disconnected.")
					isScreenConnected = False
				continue

			except ConnectionResetError:
				logging.info("Screen connection broke.")
				isScreenConnected = False
				clients[1] = None
				continue

			except KeyboardInterrupt:
				exit()
			
			except socket.error:
				logging.info("Socket Error. Screen connection broke.")
				isScreenConnected = False
				clients[1] = None
				continue
		
		elif data:
			logging.info(f"data_received = {str(data)}")
			continue
			
		else:
			logging.info("Board connection broke.")
			isBoardConnected = False
			clients[0] = None
			closeConnections(clients)
			clients, board, screen = connect(clients, board, screen)
			continue
	
	except KeyboardInterrupt:
		exit()

	except socket.error:
		logging.info("Socket Error. Board connection broke.")
		isBoardConnected = False
		closeConnections(clients)
		clients, board, screen = connect(clients, board, screen)
		continue
	



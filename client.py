from time import sleep
from tkinter import *
from PIL import ImageTk
import socket
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)


WIDTH, HEIGHT = 1280, 720
HOST = "192.168.61.243"
PORT = 8585
connected = False


root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")

our_images = [
	ImageTk.PhotoImage(file="Digital_Twin\Snapshot_{:02d}.png".format(i))
	for i in range(0, 35)
]

my_canvas = Canvas(root, width=WIDTH, height=HEIGHT)
my_canvas.create_image(0, 0, image=our_images[0], anchor="nw")
my_canvas.pack(fill="both", expand=True)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""-------------------Functions-------------------"""

def receive_data(client) -> bytes:
	"""Receives Data from client."""
	return client.recv(2).strip()

def reconnect_to_server():
	global connected
	logging.info("Connection - Connecting to server...")
	while not connected:
			# attempt to reconnect, otherwise sleep for 2 seconds
			try:
				client.connect( ( HOST, PORT ) )
				connected = True
				logging.info( "Re-connection successful" )
				client.recv(2000)
			except socket.error:
				sleep( 3 )
	return

def loop():
	global connected
	global client
	try:
		data = receive_data(client)
		if data:
			logging.info(f"data = {int(data)}")
			n = int(data)
			if 0<=n<=34:
				my_canvas.create_image(0, 0, image=our_images[n], anchor="nw")
		else:
			logging.info("Connection - Connection closed by server.")
			reconnect_to_server()
		root.after(50, loop)

	except socket.error:
		# set connection status and recreate socket
		connected = False
		client = socket.socket()
		logging.info( "Connection lost. reconnecting..." )
		reconnect_to_server()
	
	except Exception as e:
		# any unexpected error stops program execution
		logging.error(e)
		logging.info("Connection - Closing the connection.")
		client.close()
		logging.info("Connection - Connection closed.")
		logging.info("Ending the program.")
		root.destroy()
		return

"""-----------------------------------------------"""

while not connected:
	# attempt to reconnect, otherwise sleep for 2 seconds
	try:
		logging.info( "Connecting to server..." )
		client.connect( ( HOST, PORT ) )
		connected = True
		logging.info( "Connection successful" )
		continue
	except socket.error:
		logging.info("Can't connect. Re-trying...")
		sleep( 3 )


# DRIVER FUNCTION
loop()

root.mainloop()

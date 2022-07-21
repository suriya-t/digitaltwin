from time import sleep
from tkinter import *
from PIL import ImageTk
import socket
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)


WIDTH, HEIGHT = 1280, 720
PORT = 8585
connected = False
client = None
count = 0


root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")

our_images = [
	ImageTk.PhotoImage(file="Digital_Twin\Snapshot_{:02d}.png".format(i))
	for i in range(0, 35)
]

my_canvas = Canvas(root, width=WIDTH, height=HEIGHT)
my_canvas.create_image(0, 0, image=our_images[0], anchor="nw")
my_canvas.pack(fill="both", expand=True)

Server = socket.socket()
Server.bind(("0.0.0.0", PORT))
Server.listen(0)
print("Server started")

"""-------------------Functions-------------------"""

def receive_data(client) -> bytes:
	"""Receives Data from connection."""
	return client.recv(2)

def reconnect_to_server():
	global connected
	global client
	while not connected:
		# attempt to reconnect, otherwise sleep for 2 seconds
		try:
			logging.info( "Waiting for connection..." )
			client, addr = Server.accept()
			connected = True
			logging.info( "Re-connection successful." )
			continue
		except socket.error:
			sleep( 3 )
	return

def loop():
	global connected
	global client
	global count

	try:
		data = receive_data(client)
		if data:
			if count > 7:
				client.recv(3000)
				count=0
			else:
				count=count+1
			logging.info(f"data = {data}")
			n = int(data)
			if 0<=n<=34:
				my_canvas.create_image(0, 0, image=our_images[n], anchor="nw")
		else:
			logging.info("Connection - Connection closed by board.")
			connected = False
			client = None
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
		logging.info( "Waiting for connection..." )
		client, addr = Server.accept()
		connected = True
		logging.info( "Connection successful." )
		continue
	except socket.error:
		logging.info("Can't connect. Re-trying...")
		sleep( 3 )


# DRIVER FUNCTION
loop()

root.mainloop()

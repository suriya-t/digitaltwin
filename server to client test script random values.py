# Server-Client Program
#-----Server-------
from datetime import datetime
import socket
import random
import time
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)


Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(('0.0.0.0',8585))
Server.listen(1)
logging.info("Server started")

"""-------------------Functions-------------------"""

#Verify the choice and call appropriate functions


#Sends Message to the opposite user.
def sendMessage(client, message:str="No message"):
    return client.send(bytes(message, 'utf8'))

#Receives message from the user.
def receiveMessage(client) -> str:
    return client.recv(1024).decode()

#Closes all connections made.
def closeConnections(client)-> int:
    return client.close()
"""-----------------------------------------------"""

clients = []
clients.append( Server.accept() )
firstClient = clients[0][0]
logging.info(f"Connected with {clients[0][1]}")




# Send functions
def random_send():
    while True:
        try:
            n = random.randint(0, 34)
            data = "{:02d}".format(n)
            nob = sendMessage(firstClient, data)
            logging.info(f"{nob} data sent = {data}")
            time.sleep(.25)
        except ConnectionResetError:
            logging.info("Client disconnected.")
            break
        except Exception as e:
            logging.info(e)
            closeConnections(firstClient)
            logging.info("Connection - Connection closed.")
            logging.info("Ending the program.")
            break
    return

def increase():
    i=0
    while True:
        try:
            if i==35:
                i=0
            data = "{:02d}".format(i)
            nob = sendMessage(firstClient, data)
            logging.info(f"{nob} data sent = {data}")
            time.sleep(.25)
            i+=1
        except ConnectionResetError:
            logging.info("Client disconnected.")
            break
        except Exception as e:
            logging.info(e)
            closeConnections(firstClient)
            logging.info("Connection - Connection closed.")
            logging.info("Ending the program.")
            break
    return

if __name__ == '__main__':
    increase()


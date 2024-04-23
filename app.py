import socket
import time
import logging
from datetime import datetime, timezone

# Configure logging
log_filename = f'logs/connection_log_{datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d")}.txt'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Server information
SERVER_HOST = 'example.com'
SERVER_PORT = 443

# Connection status
connected = False
connection_start_time = None
disconnection_start_time = None

def connect_to_server():
    global connected, connection_start_time, disconnection_start_time
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        connected = True
        connection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
        disconnection_start_time = None
        logging.info(f'Connected to {SERVER_HOST}:{SERVER_PORT}')
    except Exception as e:
        connected = False
        connection_start_time = None
        disconnection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
        logging.error(f'Failed to connect to {SERVER_HOST}:{SERVER_PORT}: {e}')

def maintain_connection():
    while True:
        if not connected:
            connect_to_server()
        else:
            try:
                # Perform any necessary operations to maintain the connection
                # For example, send a keep-alive packet or receive data
                data = sock.recv(1024)  # Receive data from the server
                if not data:
                    raise Exception("Server closed the connection")
            except Exception as e:
                connected = False
                disconnection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                logging.error(f'Disconnected from {SERVER_HOST}:{SERVER_PORT}: {e}')
                logging.info(f'Connection duration: {disconnection_start_time - connection_start_time}')
                connect_to_server()
        time.sleep(5)  # Adjust the sleep duration as needed

if __name__ == '__main__':
    maintain_connection()
import socket
import time
import logging
from datetime import datetime, timezone, timedelta

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

# Heartbeat interval (in seconds)
HEARTBEAT_INTERVAL = 60

# Timeout for receiving data (in seconds)
RECEIVE_TIMEOUT = 10

def connect_to_server():
    global connected, connection_start_time, disconnection_start_time, sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(RECEIVE_TIMEOUT)
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

def send_heartbeat():
    try:
        # Send a heartbeat message to the server
        sock.sendall(b'HEARTBEAT')
    except Exception as e:
        logging.error(f'Failed to send heartbeat: {e}')

def maintain_connection():
    global connected, connection_start_time, disconnection_start_time
    last_heartbeat_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
    while True:
        if not connected:
            connect_to_server()
        else:
            try:
                # Receive data from the server
                data = sock.recv(1024)
                if not data:
                    raise Exception("Server closed the connection")
                # Process the received data
                # ...

                # Send a heartbeat message if necessary
                current_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                if (current_time - last_heartbeat_time).total_seconds() >= HEARTBEAT_INTERVAL:
                    send_heartbeat()
                    last_heartbeat_time = current_time
            except socket.timeout:
                logging.warning(f'Timeout occurred while receiving data from {SERVER_HOST}:{SERVER_PORT}')
                connected = False
                disconnection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                logging.error(f'Disconnected from {SERVER_HOST}:{SERVER_PORT}')
                logging.info(f'Connection duration: {disconnection_start_time - connection_start_time}')
                connect_to_server()
            except Exception as e:
                connected = False
                disconnection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                logging.error(f'Disconnected from {SERVER_HOST}:{SERVER_PORT}: {e}')
                logging.info(f'Connection duration: {disconnection_start_time - connection_start_time}')
                connect_to_server()
        time.sleep(1)  # Adjust the sleep duration as needed

if __name__ == '__main__':
    maintain_connection()

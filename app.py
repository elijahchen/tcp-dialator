import socket
import time
import logging
import yaml
from datetime import datetime, timezone, timedelta
from contextlib import closing
import os
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Load server information from targets.yaml
try:
    with open('targets.yaml', 'r') as f:
        targets = yaml.safe_load(f)
    SERVER_HOSTS = targets['server_hosts']
    SERVER_PORT = targets['server_port']
except (yaml.YAMLError, KeyError) as e:
    logging.error(f'Error loading targets.yaml: {e}')
    exit(1)

# Connection pool
CONNECTION_POOL_SIZE = 10
connection_pool: List[socket.socket] = []

# Heartbeat interval (in seconds)
HEARTBEAT_INTERVAL = 60

# Timeout for socket operations (in seconds)
SOCKET_TIMEOUT = 10

# Maximum number of retries for send/receive operations
MAX_RETRIES = 3

def get_connection() -> socket.socket:
    """Get a connection from the pool or create a new one."""
    try:
        conn = connection_pool.pop()
    except IndexError:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(SOCKET_TIMEOUT)
    return conn

def release_connection(conn: socket.socket) -> None:
    """Release a connection back to the pool."""
    if len(connection_pool) < CONNECTION_POOL_SIZE:
        connection_pool.append(conn)
    else:
        conn.close()

def retry_operation(operation, *args, **kwargs):
    """Retry an operation with exponential backoff."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            retries += 1
            backoff = 2 ** retries
            logging.warning(f'Failed to perform operation: {e}. Retrying ({retries}/{MAX_RETRIES}) in {backoff} seconds...')
            time.sleep(backoff)
    logging.error(f'Failed to perform operation after {MAX_RETRIES} retries.')
    return None

def send_data(conn: socket.socket, data: bytes) -> None:
    """Send data to the server with retries."""
    retry_operation(conn.sendall, data)

def receive_data(conn: socket.socket) -> Optional[bytes]:
    """Receive data from the server with retries."""
    def receive_operation(conn):
        data = conn.recv(1024)
        if not data:
            raise Exception("Server closed the connection")
        # Validate the received data
        if not validate_data(data):
            raise Exception("Invalid data received from the server")
        return data

    return retry_operation(receive_operation, conn)

def validate_data(data: bytes) -> bool:
    """Validate the received data."""
    # Implement your data validation logic here
    return True

def send_heartbeat(conn: socket.socket) -> None:
    """Send a heartbeat message to the server."""
    send_data(conn, b'HEARTBEAT')

def maintain_connection(server_host: str) -> None:
    """Maintain a connection with the server, handling reconnections and heartbeats."""
    last_heartbeat_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
    while True:
        with closing(get_connection()) as conn:
            try:
                conn.connect((server_host, SERVER_PORT))
                logging.info(f'Connected to {server_host}:{SERVER_PORT}')
                connection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                disconnection_start_time = None

                while True:
                    # Receive data from the server
                    data = receive_data(conn)
                    if data is not None:
                        # Process the received data
                        # ...
                        pass

                    # Send a heartbeat message if necessary
                    current_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                    if (current_time - last_heartbeat_time).total_seconds() >= HEARTBEAT_INTERVAL:
                        send_heartbeat(conn)
                        last_heartbeat_time = current_time

            except Exception as e:
                logging.error(f'Disconnected from {server_host}:{SERVER_PORT}: {e}')
                disconnection_start_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                logging.info(f'Connection duration: {disconnection_start_time - connection_start_time}')
                release_connection(conn)
                time.sleep(1)  # Wait before reconnecting

if __name__ == '__main__':
    try:
        with open('targets.yaml', 'r') as f:
            targets = yaml.safe_load(f)
        for server_host in targets['server_hosts']:
            maintain_connection(server_host)
    except (yaml.YAMLError, KeyError) as e:
        logging.error(f'Error loading targets.yaml: {e}')

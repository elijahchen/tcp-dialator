# TCP Connection Maintenance Script

This Python script establishes and maintains a TCP connection with a server on port 443. It handles reconnections, sends periodic heartbeat messages, and logs connection status changes with detailed information.

## Prerequisites

- Python 3.x
- `pyyaml` library (install with `pip install pyyaml`)

## Installation

1. **Install Python**: If you don't have Python installed on your system, you can download it from the official Python website (https://www.python.org/downloads/). Make sure to download the latest version of Python 3.x.

2. **Install pip**: Pip is the package installer for Python. It comes pre-installed with Python versions 3.4 and later. If you have an older version of Python, you can install pip by following the instructions on the official pip website (https://pip.pypa.io/en/stable/installing/).

3. **Install pyyaml**: This script requires the `pyyaml` library to load the server information from the `targets.yaml` file. You can install it using pip by running the following command in your terminal or command prompt:

   ```
   pip install pyyaml
   ```

   If you encounter any permission issues during the installation, try running the command with administrative privileges:

   ```
   sudo pip install pyyaml  # On Unix/Linux
   ```

   ```
   pip install pyyaml --user  # On Windows
   ```

## Usage

1. Create a `targets.yaml` file in the same directory as the script, containing the server host and port information. For example:

   ```yaml
   server_hosts:
     - example.com
     - another.example.net
   server_port: 443
   ```

2. The script will automatically load the server information from the `targets.yaml` file.

3. Run the `app.py` script using the following command:

   ```
   python app.py
   ```

   The script will establish a connection with the specified server(s) and maintain it. It will log connection status changes, including connection duration, disconnection times, and reconnection attempts.

## Logging

The script generates log files with the following naming convention: `connection_log_YYYY-MM-DD.txt`. A new log file is created for each day based on the activity/status of the TCP 443 connection. The log files are stored in the `logs` directory and contain detailed information about the connection status, including timestamps, connection durations, and any errors or warnings.

## Configuration

You can modify the following configuration variables in the `app.py` file:

- `CONNECTION_POOL_SIZE`: The maximum number of connections to keep in the connection pool.
- `HEARTBEAT_INTERVAL`: The interval (in seconds) at which heartbeat messages are sent to the server.
- `SOCKET_TIMEOUT`: The timeout (in seconds) for socket operations.
- `MAX_RETRIES`: The maximum number of retries for send/receive operations.

## Features

- Connection pooling for improved performance.
- Periodic heartbeat messages to keep the connection open.
- Handling of response timeouts and retrying requests.
- Error code handling and reauthentication on faults.
- Data validation for improved security.
- Logging of connection status changes with detailed information.
- Timezone support (logs are generated in EST).

## License

This project is licensed under the [MIT License](LICENSE).

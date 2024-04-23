
The script will automatically load the server information from the `targets.yaml` file.

3. The script will establish a connection with the specified server and maintain it. It will log connection status changes, including connection duration, disconnection times, and reconnection attempts.

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

# TCP Connection Maintenance Script

This Python script establishes and maintains a TCP connection with a server on port 443. It handles reconnections, sends periodic heartbeat messages, and logs connection status changes with detailed information.

## Prerequisites

- Python 3.x
- `pyyaml` library (install with `pip install pyyaml`)

## Usage

1. Create a `targets.yaml` file in the same directory as the script, containing the server host and port information. For example:


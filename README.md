# Snake Redis Lite

A lightweight Redis-like server implementation in Python, supporting a subset of the Redis Serialization Protocol (RESP) for educational purposes and simple enough to serve as a foundation for more complex projects. I'm doing this for fun but I'll try to add more complex features as I go XD. 

## Features

- Basic RESP Serialization/Deserialization
- TCP/IP network communication using sockets
- Command handling for PING and ECHO
- SET and GET data commands
- Handle multiple concurrent clients using threads
- (More in progress...)

## Getting Started

### Prerequisites

- Python 3.x
- Redis client for testing (optional)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/snake-Redis.git
cd snake-Redis
```

## Running the Server
To run the Redis Lite server, execute:

```bash
python3 server.py
```

The server will start listening on 127.0.0.1:6380 by default.

## Testing
You can test the server using the redis-cli tool:

```bash
redis-cli -p 6380
```

Once connected, try the following commands:

```bash
ping
echo "Hello World"
```
# Jordan Rinne
# jrinne@uci.edu
# 16935997


import ds_client

server = "127.0.0.1"
port = 3001

result = ds_client.send(
    server,
    port,
    "jordan",
    "password123",
    "Hello from Assignment 3!"
)

print(result)
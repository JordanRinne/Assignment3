# Jordan Rinne
# jrinne@uci.edu
# 16935997


import ds_client

server = "127.0.0.1"
port = 3001
username = "jordan"
password = "password123"

print(ds_client.send(server, port, username, password, "Test post only"))
print(ds_client.send(server, port, username, password, "", "Test bio only"))
print(ds_client.send(server, port, username, password, "Test post and bio", "Updated bio"))
print(ds_client.send(server, port, "f21demo", "pwd123", "Hello World!"))
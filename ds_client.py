# Jordan Rinne
# jrinne@uci.edu
# 16935997


import socket
import ds_protocol
import time


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''

  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((server, port))

      send_file = s.makefile('w')
      recv_file = s.makefile('r')

      join = ds_protocol.join_msg(username, password)
      send_file.write(join + '\r\n')
      send_file.flush()

      response = recv_file.readline()
      #print("JOIN RESPONSE:", response)
      response_data = ds_protocol.extract_json(response)

      if response_data.type != "ok":
        print("Failed to join server.")
        return False
    
      token = response_data.token
      #print("TOKEN:", token)
      timestamp = str(time.time())

      if message is not None and message.strip() != "":
        post = ds_protocol.post_msg(token, message, timestamp)
        send_file.write(post + '\r\n')
        send_file.flush()

        response = recv_file.readline()
        #print("SERVER RESPONSE:", response)
        
        response_data = ds_protocol.extract_json(response)

        if response_data.type != "ok":
          #print("Failed to post message.")
          return False

      if bio is not None and bio.strip() != "":
        bio_msg = ds_protocol.bio_msg(token, bio, timestamp)
        send_file.write(bio_msg + '\r\n')
        send_file.flush()

        response = recv_file.readline()
        response_data = ds_protocol.extract_json(response)

        if response_data.type != "ok":
          #print("Failed to update bio.")
          return False

      return True
  except Exception as ex:
    #print(f"An error occurred: {ex}")
    return False

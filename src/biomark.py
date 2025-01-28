import os
import ast
import socket
import time


class retrieveData:
    def __init__(self, client_info):
        data = open(os.path.abspath(client_info), "r")
        self.clients = [ast.literal_eval(line.strip()) for line in data]

    def pitTags(self, port=10001):
        # Generate blank list to put output from each 
        raw_list = []
        # Loop through PIT antenna clients and grab data
        for client in self.clients:
        # Create a socket object with a timeout to prevent indefinite blocking
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Set a 3-second timeout
                s.settimeout(3)  
                try:
                    # Connect to the device
                    s.connect((client[0], port))
                    # Send the request command for 'Memory Tag Download' (MTD)
                    request_command = b'MTD\r\n'
                    s.send(request_command)
                    # Introduce a brief 3-sec delay to allow device to process command
                    time.sleep(3)
                    # Read data in chunks, printing what we get back
                    while True:
                        # Receive data in 1024-byte chunks
                        byte_data = s.recv(1024) 
                        if not byte_data:
                            break  # Exit loop if no more data is received
                                   # Should always be recieved regardless of 
                                   # tags collected or not.
                        data = byte_data.decode('utf-8')
                        # Biomark ends report with 'Complete', this will end it
                        if b'Complete' in byte_data: 
                            break
                    # Convert data from bytestring to str and return
                    raw_list.append([data, client[0], client[1], client[2]])
                # Error handling 
                except socket.timeout: # Throw exception if socket request hangs
                    print("""Timeout occurred while waiting for data.
                          Network likely down: {}""".format(
                              time.strftime("%Y-%m-%d %H:%M:%S", 
                                            time.gmtime())))
                    raise
                except Exception as e: # Log errors to service file error log
                    print(f"Error: {e}")
                    raise
        return raw_list
            
    def formatTagData(self, raw_data):
        # Blank list to append looped data to
        formatted_data = []
        # Loop through output string serial data and format
        # for clean append to postgres
        for client in raw_data:
            for info in client[0].splitlines():
                # Extract data exclusively beginning with "TAG"
                # This is how biomark denotes PIT detection serial data
                if 'TAG' in info:
                    reader_data = info.split(' ')[1:5] 
                    # Order same as readout from IS1001
                    data = [reader_data[1], reader_data[2], 
                            reader_data[0], reader_data[3], 
                            client[2], client[3], client[1]]
                    formatted_data.append(data)
        # Convert to tuple for .executemany method for psycopg
        return tuple(formatted_data)
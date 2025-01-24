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
                # Set a 3-second timeout (adjust as necessary)
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
        
        for line in raw_data:
            line[0].split(' ')[1:5] # fix this
            if 'TAG' in line[0]:
                print(line[0])
        '''
        tag_data = []
        for line in raw_data.splitlines():
            # 'TAG' included in serial out with tag data, excludes else
            if 'TAG' in line:
                # Extracts: ReaderID, Date, Time, & DEC Tag ID
                line_data = line.split(' ')[1:5]
                tag_data.append(line_data)

        # Format to tuple for .executemany method in psycopg
        return tuple(tag_data)
        '''
        return 0



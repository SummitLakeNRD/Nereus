import socket
import time


class retrieveData:
    def __init__(self, client_info):
        self.client_info = client_info

    def pitTags(self, ip_address, port=10001):
        # Create a socket object with a timeout to prevent indefinite blocking
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a 3-second timeout (adjust as necessary)
            s.settimeout(3)  

            try:
                # Connect to the device
                s.connect((ip_address, port))

                # Send the request command for 'Memory Tag Download' (MTD)
                request_command = b'MTD\r\n'
                s.send(request_command)

                # Introduce a brief 3-sec delay to allow device to process command
                time.sleep(3)

                # Read data in chunks, printing what we get back
                while True:
                    # Receive data in 1024-byte chunks
                    data = s.recv(1024)  
                    if not data:
                        break  # Exit loop if no more data is received
                               # Should always be recieved regardless of 
                               # tags collected or not.
                    
                    # Biomark ends report with 'Complete', this will end it
                    if b'Complete' in data:  
                        break

                # Convert data from bytestring to str and return
                return data.decode('utf-8')

            # Error handling 
            except socket.timeout: # Throw exception if socket request hangs
                print("Timeout occurred while waiting for data.")
                return None
            except Exception as e: # Log errors to service file error log
                print(f"Error: {e}")
                return None
            
    def formatTagData(self, raw_data):
        tag_data = []
        for line in raw_data.splitlines():
            # 'TAG' included in serial out with tag data, excludes else
            if 'TAG' in line:
                # Extracts: ReaderID, Date, Time, & DEC Tag ID
                line_data = line.split(' ')[1:5]
                tag_data.append(line_data)

        # Format to tuple for .executemany method in psycopg
        return tuple(tag_data)



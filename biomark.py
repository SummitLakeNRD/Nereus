import socket
import time

def download_pit_data(ip_address, port=10001):
    # Create a socket object with a timeout to prevent indefinite blocking
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)  # Set a 5-second timeout (adjust as necessary)
        
        try:
            # Connect to the device
            s.connect((ip_address, port))
            print(f"Connected to {ip_address}:{port}")

            # Send the request command
            request_command = b'MTD\r\n'
            s.send(request_command)
            print("Request sent to the device.")

            # Introduce a brief delay to allow device to process command
            time.sleep(1)

            # Read data in chunks, printing what we get back
            data = b''
            while True:
                chunk = s.recv(1024)  # Receive data in 1024-byte chunks (adjust if necessary)
                if not chunk:
                    break  # Exit loop if no more data is received

                print(f"Received chunk: {chunk}")  # Debugging: print the received data
                data += chunk
                
                # If we detect a known end marker, we stop receiving (e.g., '\n' or 'END')
                if b'END' in chunk:  # Adjust based on actual end marker or condition
                    break

            if data:
                print("Full data received:")
                print(data)
            else:
                print("No data received.")

            return data

        except socket.timeout:
            print("Timeout occurred while waiting for data.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# Usage
ip = '10.30.8.2'  # Replace with your Biomark IS1001 IP address
data = download_pit_data(ip)
if data:
    print("Data downloaded successfully.")
else:
    print("Failed to download data.")

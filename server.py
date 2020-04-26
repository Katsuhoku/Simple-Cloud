# Benemérita Universidad Autónoma de Puebla
# Facultad de Ciencias de la Computación
# Sistemas Operativos II
#
# Práctica (?) : Comunicación remota entre computadoras, envío de archivos
#
# Arizmendi Ramírez Esiel Kevin, 201737811
# Coria Rios Marco Antonio, 201734576
# 28/Abril/2020

import socket
from os.path import isfile

# Main function
# Main must handle communication with client
def main():
    HOST = socket.gethostname()
    PORT = 42069

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.settimeout(30)
        try:
            # Server remains available
            while True:
                s.listen()
                conn, addr = s.accept()

                # Handling new connection
                with conn:
                    print('Connected by', addr)

                    # Communication 'til client ends it
                    while True:
                        # Waiting for petitions
                        # 'u' = upload file, 'd' = downlaod file, 'r' = remove file
                        # 'e' = exit
                        op = conn.recv(1).decode('utf-8', 'replace')
                        if op == 'u':
                            upload(conn)
                        elif op == 'd':
                            download(conn)
                        elif op == 'r':
                            remove(conn)
                        elif op == 'e':
                            print('Connection ended with', addr)
                            break # finish connection
                        else:
                            pass # send error message (?)
        except socket.timeout:
            print('Timeout! No more conexions, bye!')

# Upload file: Function for saving uncoming files
# Receives: Connected socket
# Returns (to client): Confirmation, or throws (?) an error
def upload(conn):
    print('Upload')
    name = conn.recv(1024).decode('utf-8', 'replace') # Gets filename (1)
    filename = f'recv\{name}'
    # Verifies if file already exists
    if isfile(filename):
        # Reply (2)
        conn.send(b'y')
        # If exists, asks for replacement (3)
        replace = conn.recv(1).decode('utf-8', 'replace')
        if replace == 'n': return
    else: conn.send(b'n') # Reply (2)

    # New file (4)
    with open(filename, 'wb') as f:
        conn.settimeout(5)
        try:
            data = conn.recv(1024)
            while True:
                f.write(data)
                data = conn.recv(1024)
        except socket.timeout: pass
        conn.settimeout(None)

    # Confirmation (5)
    conn.send(b'100')
    print(f'Uploaded: {filename}')

# Download file: Function for obtaining data of desired file
# Receives: Connected socket
# Returns: File data, or throws (?) an error
def download(conn):
    print('Download')
    name = conn.recv(1024).decode('utf-8', 'replace') # Gets filename (1)
    filename = f'recv\{name}'
    # Verifies if file exists
    if isfile(filename):
        # Reply (2)
        conn.send(b'y')
        # If exists, asks for sending (3)
        send = conn.recv(1).decode('utf-8', 'replace')
        if send == 'n': return
        else:
            # Sending file data (4)
            with open(filename, 'rb') as f:
                print('Sending...')
                data = f.read(1024)
                while data:
                    conn.send(data)
                    data = f.read(1024)

            # Confirmation (5)
            reply = conn.recv(3).decode('utf-8', 'replace')
            if reply == '100': print('File transfered successfully to client')
            else: print("Error: Couldn't transfer file. Unknown error")
    else: conn.send(b'n') # Reply (2)

# Remove file: Function for delete a file
# Receives: Connected socket
# Return: Confirmation, or throws (?) an error
# (Provide "Recycle Bin"?)
def remove(conn):
    print('Remove')
    # Gets filename
    # Verifies if file exists
    # If doesn't, throws (?) an error
    # Else



if __name__ == '__main__':
    main()
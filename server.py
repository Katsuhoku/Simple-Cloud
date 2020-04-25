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
# Only main will use the sockets (server socket and client-connection socket)
def main():
    HOST = '127.0.0.1'
    PORT = 42069

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        # Server remains available
        while True:
            s.listen()
            conn, addr = s.accept()

            # Handling new connection
            with conn:
                print('Connected by', addr)

                # 
                while True:
                    # Waiting for petitions
                    # 'u' = upload file, 'd' = downlaod file, 'r' = remove file
                    # 'e' = exit
                    op = conn.recv(1).decode('utf-8', 'replace')
                    if op == 'u':
                        # Gets filename
                        # Verifies if file already exists
                        # If exists, asks for replacement
                        # If want replace, or if file doesn't exist:
                        upload(None, None)
                    elif op == 'd':
                        # Gets filename
                        # Verifies if file exists
                        # If doesn't, throws (?) an error
                        # Else:
                        download(None)
                    elif op == 'r':
                        # Gets filename
                        # Verifies if file exists
                        # If doesn't, throws (?) an error
                        # Else
                        remove(None)
                    elif op == 'e':
                        print('Connection ended with', addr)
                        break # finish connection
                    else:
                        pass # send error message (?)

# Upload file: Function for saving uncoming files
# Receives: File data; Filename
# * Will replace previous file if exists
# Returns: Confirmation, or throws (?) an error
def upload(data, filename):
    print('Upload')

# Download file: Function for obtaining data of desired file
# Receives: Filename
# Returns: File data, or throws (?) an error
# * File with the specified filename MUST exist
def download(filename):
    print('Download')

# Remove file: Function for delete a file
# Receives: Filename
# Return: Confirmation, or throws (?) an error
# * File with the specified filename MUSt exist
# (Provide "Recycle Bin"?)
def remove(filename):
    print('Remove')



if __name__ == '__main__':
    main()
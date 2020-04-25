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
from os import system
from os.path import isfile
from sys import platform
import subprocess as sp

connected = False

# Main Function
def main():
    global connected

    # Connect to server
    clsc()
    host, port = serverInfo()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            connected = True

            # Shows main menu
            while True:
                clsc()
                op = menu()
                if op == 1: # Upload file
                    s.send(b'u')
                    upload(s)
                elif op == 2: # Download file
                    s.send(b'd')
                    download(s)
                elif op == 3: # Remove file
                    s.send(b'r')
                    remove(s)
                else: # Exit
                    s.send(b'e')
                    break
    except ConnectionRefusedError:
        print('Error: Host unreachable')
    except:
        print('Error: Unknown error')

# Display menu: Function for show menu options and wait input
# Returns: Option selected
# Handles input errors and invalid options
def menu():
    while True:
        print ('\tCloud Server\n')
        print('Select an option:')
        print('1. Upload file')
        print('2. Download file')
        print('3. Remove file on server')
        print('4. Close connection and exit')

        try:
            op = int(input('> '))
            if op not in range(1,5):
                print('Invalid option, try again')
            else: return op
        except ValueError:
            print('Option must be a number!')

# Get information of the server: Request user for server IP and port
# Returns: Server IP and Listening Port
def serverInfo():
    print('\tCloud Server\n')
    host = input('Server IP > ')
    while True:
        port = int(input('Port > '))

        if port < 1 or port > 65535:
            print('Port must be in range from 1 to 65535')
        else: break

    return host, port

# Upload file to server: Handles the process for uploading a file
# Asks for local filename
# If local file exists, asks for filename with which will be saved on server
# If file exists on server, asks for replace or cancel operation
# If file doesn't exist, or replace, sends local file data
def upload(s):
    clsc()
    print('\tUpload File')

    lfn = input('Local filename > ')
    if not isfile(lfn):
        print(f'Cannot find "{lfn}"')
        input('Press enter to continue...')
        return

    rfn = input('Filename for server (Press enter to save with original name)\n> ')
    if not rfn: rfn = lfn

    # Sends filename (1)
    s.send(rfn)

    # Reply (2)
    exists = s.recv(1).decode('utf-8', 'replace')
    if exists == 'y':
        print(f'File "{rfn}" already exists in server')
        while True:
            replace = input('Replace? (y/n) > ')
            if replace == 'y' or replace == 'n':
                # Replacement answer (3)
                s.send(replace.encode('utf-8'))
                break
            print('(Expected "y" for replace, or "n" for cancel. Try again.)')

        if replace == 'n': return
    
    # Sending file data (4)
    lf = open(lfn, 'rb')
    data = lf.read(1024)
    while data:
        s.send(data)
        data = lf.read(1024)

    # Confirmation (5)
    reply = s.recv(3).decode('utf-8', 'replace')
    if reply != '100': print("Error: Couldn't save file on server. Unknown error")
    else: print('File saved successfully on server')



# Downlaod file from server: Handles the process for downloading a file
# Asks for filename on server
# If file exists on server, asks for the local filename
# If local filename exists, asks for replace or cancel operation
# If local file doesn't exists, or replace, gets file data from server and saves file
def download(s):
    pass

# Remove file on server: Handles the process for removing a file saved on server
# Asks for filename on server
# If file exists, request deleting
def remove(s):
    pass

def clsc():
    if platform == 'linux' or platform == 'linux2':
        tmp = sp.call('clear', shell=True)
    elif platform == 'darwin':
        tmp = sp.call('cls', shell=True)
    elif platform == 'win32':
        system('cls')
        

if __name__ == '__main__':
    main()
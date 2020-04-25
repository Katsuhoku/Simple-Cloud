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

# Main function
def main():
    HOST = '127.0.0.1'
    PORT = 69420

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        # Server remains available
        while True:
            s.listen()
            conn, addr = s.accept()

            # Handling new connection
            with conn:
                print('Connected by', addr)

                # Waiting for petitions ('u' = upload file, 'd' = downlaod file, 'r' = remove file)
                op = conn.recv(1)
                if op == 'u':
                    upload()
                elif op == 'd':
                    downlaod()
                elif op == 'r':
                    remove()
                else:
                    pass # send error message (?)

def upload():
    pass

def downlaod():
    pass

def remove():
    pass


if __name__ == '__main__':
    main()
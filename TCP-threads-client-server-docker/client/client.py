import socket
import threading
import time

# Server address and port
SERVER_HOST = 'server'
PORT = 65432

def handle_messages(sock):
    """
    Function to handle incoming messages from the server.

    :param sock: The client's socket.
    """
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("La conexión con el servidor se ha restablecido.")
            break
        except ConnectionAbortedError:
            print("La conexión con el servidor ha sido abortada.")
            break
        except Exception as e:
            print("Error durante la recepción de mensajes:", e)
            break

def main():
    """
    Main function for running the client.

    It establishes a connection with the server, sends the user's nickname,
    starts a thread to handle incoming messages, and sends user input messages to the server.
    """
    time.sleep(5)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            nickname = input("Ingrese su nickname: ")
            client.connect((SERVER_HOST, PORT))
            client.send(nickname.encode())
            print(client.recv(1024).decode())

            threading.Thread(target=handle_messages, args=(client,)).start()

            while True:
                mensaje = input()
                client.send(mensaje.encode())
                if mensaje == 'QUIT':
                    break
    except Exception as e:
        print("Error en la ejecución del cliente:", e)

if __name__ == "__main__":
    main()
import socket
import threading
import datetime

# Server address and port
HOST = '0.0.0.0'
PORT = 65432

# ANSI Colors
GREEN = '\033[92m'  
YELLOW = '\033[93m'
RESET = '\033[0m'  
CYAN = ' \033[96m' 

# Dictionary to store clients' sockets and their respective nicknames
clients = {}

def handle_client(client, addr):
    """
    Function for handling a client.

    :param client: The client's socket.
    :param addr: The client's address.
    """
    try:
        nickname = client.recv(1024).decode()
        client.send(f"{GREEN}Bienvenido al servidor {HOST}:{PORT}. Si deseas desconectarte, escribe 'QUIT'.{RESET}\n".encode())
        broadcast(f"{GREEN}{nickname} se ha conectado.{RESET}", client)
        clients[client] = nickname
        event_log(f"El cliente {nickname} se ha conectado desde {addr}")

        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    break
                if message == 'QUIT':
                    diconnect_client(client, nickname)
                    break
                else:
                    fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    full_message = f"{CYAN}[{fecha_hora}] >> {nickname}:{RESET} {message}"
                    print(full_message)
                    broadcast(full_message, client)
                    full_message = f"[{fecha_hora}] >> {nickname}: {message}"
                    save_log(full_message)
            except Exception as e:
                print(f"Error en el manejo del mensaje del cliente {nickname}: {e}")
                diconnect_client(client, nickname)
                break
    except Exception as e:
        print(f"Error al manejar la conexión del cliente {addr}: {e}")
        diconnect_client(client, "Desconocido")
        

def diconnect_client(client, nickname):
    """
    Function to disconnect a client.

    :param client: The client's socket.
    :param nickname: The client's nickname.
    """
    try:
        client.close()
        del clients[client]
        broadcast(f"{YELLOW}{nickname} se ha desconectado.{RESET}\n", client)
        event_log(f"El cliente {nickname} se ha desconectado.")
    except Exception as e:
        print(f"Error al desconectar al cliente {nickname}: {e}")

def broadcast(message, sender):
    """
    Function to send a message to all clients except the sender.

    :param message: The message to broadcast.
    :param sender: The sender's socket.
    """
    for client in list(clients.keys()):
        try:
            if client != sender:
                client.send(message.encode())
        except Exception as e:
            print(f"Error al enviar mensaje a un cliente: {e}")
            client.close()
            del clients[client]

def save_log(message):
    """
    Function to save a message to a log file.

    :param message: The message to save.
    """
    try:
        with open("log.txt", "ab") as file:  
            file.write(message.encode('utf-8') + b"\n")  
    except Exception as e:
        print(f"Error al guardar en el archivo de registro: {e}")

def event_log(evento):
    """
    Function for logging events.

    :param event: The event to log.
    """
    fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f"[{fecha_hora}] {evento}"
    print(message)
    save_log(message)


def main():
    """
    Main function for starting the server.

    It logs the event of server initialization, creates a server socket, binds it to the specified
    host and port, listens for incoming connections, and starts a new thread for each client that connects.

    :raises: Any exception that occurs during server operation.
    """
    try:
        event_log("Servidor iniciado")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen()

            print(f"Servidor escuchando en {HOST}:{PORT}")

            while True:
                client, addr = server.accept()
                threading.Thread(target=handle_client, args=(client, addr)).start()
    except Exception as e:
        print(f"Error en el servidor: {e}")
            

if __name__ == "__main__":
    main()
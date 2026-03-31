import socket
import ssl
import threading

HOST = "10.1.17.245"
PORT = 5000


def receive_messages(client):

    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            print("\nReceived:", message.decode().strip())

        except:
            break


def main():
    # FIX: Added cafile. Without this, the subscriber would reject the self-signed cert.
    # Adjust the path if your subscriber is in a different directory relative to the cert.
    context = ssl.create_default_context(cafile="broker/server.crt")
    
    # FIX: Disable hostname checking here as well
    context.check_hostname = False

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client = context.wrap_socket(raw_socket, server_hostname=HOST)

    client.connect((HOST, PORT))

    print("Secure subscriber connected")

    topic = input("Topic to subscribe: ").strip()

    client.send(f"SUBSCRIBE:{topic}\n".encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    try:
        thread.join()
    except KeyboardInterrupt:
        pass

    finally:
        client.close()


if __name__ == "__main__":
    main()
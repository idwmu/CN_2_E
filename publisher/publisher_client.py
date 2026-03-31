import socket
import ssl

HOST = "10.1.20.187"
PORT = 5000


def main():
    # Ensure the path to your server.crt is correct based on your folder structure
    context = ssl.create_default_context(cafile="broker/server.crt")
    
    # FIX: Disable hostname checking to prevent the '127.0.0.1' mismatch error
    context.check_hostname = False

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client = context.wrap_socket(raw_socket, server_hostname=HOST)

    client.connect((HOST, PORT))

    print("Secure publisher connected")

    try:
        while True:

            topic = input("Topic: ").strip()
            message = input("Message: ").strip()

            if not topic or not message:
                print("Invalid input")
                continue

            publish_msg = f"PUBLISH:{topic}:{message}\n"

            client.send(publish_msg.encode())

            response = client.recv(1024)

            print("Server:", response.decode())

    except KeyboardInterrupt:
        print("Publisher exiting")

    finally:
        client.close()


if __name__ == "__main__":
    main()
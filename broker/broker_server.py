import socket
import ssl
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

topics = {}
clients = set()
lock = threading.Lock()

messages_processed = 0
start_time = time.time()


def remove_client(conn):
    with lock:
        clients.discard(conn)
        for topic in topics:
            if conn in topics[topic]:
                topics[topic].remove(conn)


def handle_client(conn, addr):
    global messages_processed

    print(f"[CONNECTED] {addr}")

    with lock:
        clients.add(conn)

    try:
        while True:
            data = conn.recv(2048)

            if not data:
                break

            try:
                message = data.decode().strip()
            except:
                continue

            parts = message.split(":")

            if len(parts) < 2:
                conn.send(b"ERROR:INVALID_FORMAT\n")
                continue

            command = parts[0]

            if command == "SUBSCRIBE":

                topic = parts[1]

                with lock:
                    if topic not in topics:
                        topics[topic] = set()

                    topics[topic].add(conn)

                conn.send(f"SUBSCRIBED:{topic}\n".encode())

                print(f"{addr} subscribed to {topic}")

            elif command == "PUBLISH":

                if len(parts) < 3:
                    conn.send(b"ERROR:INVALID_PUBLISH\n")
                    continue

                topic = parts[1]
                msg = parts[2]

                with lock:
                    subscribers = topics.get(topic, set()).copy()

                payload = f"MESSAGE:{topic}:{msg}\n".encode()

                for sub in subscribers:
                    try:
                        sub.send(payload)
                    except:
                        remove_client(sub)

                messages_processed += 1

                conn.send(b"OK\n")

            else:
                conn.send(b"ERROR:UNKNOWN_COMMAND\n")

    except Exception as e:
        print("Client error:", e)

    finally:
        remove_client(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def performance_monitor():
    while True:
        time.sleep(10)

        elapsed = time.time() - start_time

        if elapsed == 0:
            continue

        throughput = messages_processed / elapsed

        print("\n===== PERFORMANCE =====")
        print("Active clients:", len(clients))
        print("Topics:", len(topics))
        print("Messages processed:", messages_processed)
        print("Throughput:", round(throughput, 2), "msg/sec")
        print("=======================\n")


def start_server():

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt",keyfile="server.key")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # FIX: Allows you to restart the broker instantly without port binding errors
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    sock.bind((HOST, PORT))
    sock.listen(10)

    print("Secure Broker Server running...")

    monitor_thread = threading.Thread(target=performance_monitor, daemon=True)
    monitor_thread.start()

    while True:
        conn, addr = sock.accept()

        try:
            tls_conn = context.wrap_socket(conn, server_side=True)
        except ssl.SSLError as e:
            print(f"SSL Handshake failed for {addr}: {e}")
            conn.close()
            continue

        thread = threading.Thread(target=handle_client, args=(tls_conn, addr))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server()
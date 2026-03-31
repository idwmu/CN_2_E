# 🔐 Secure Pub/Sub Message Broker (TLS Enabled)

## 📌 Overview

This project implements a secure Publish-Subscribe (Pub/Sub) messaging system using Python sockets, threading, and TLS encryption.

The system consists of:
- Broker Server – Handles message routing between clients
- Publisher Client – Sends messages to topics
- Subscriber Client – Receives messages from subscribed topics

All communication is secured using TLS (SSL) with a server certificate and private key.

---

## 🧠 Features

- Secure communication using TLS
- Multi-client support using threading
- Topic-based Pub/Sub messaging
- Real-time message delivery
- Performance monitoring (throughput, active clients)
- Error handling and client cleanup

---

## 🏗️ Architecture

Publisher ---> Broker Server ---> Subscriber

- Publishers send messages to topics
- Subscribers receive messages from topics
- Broker manages all routing and connections

---

## 📡 Communication Protocol

The system uses a text-based protocol:

Subscribe:
SUBSCRIBE:<topic>

Publish:
PUBLISH:<topic>:<message>

Message Delivery:
MESSAGE:<topic>:<message>

Responses:
SUBSCRIBED:<topic>
OK
ERROR:<type>

---

## 📁 Project Structure

project/
│
├── broker_server.py
├── publisher_client.py
├── subscriber_client.py
├── server.crt
├── server.key
└── README.md

---

## ⚙️ Requirements

- Python 3.x
- OpenSSL (for certificate generation)

---

## 🔐 Generating SSL Certificate

Run the following commands:

openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048

openssl req -new -key server.key -out server.csr

openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365

---

## 🚀 Setup Instructions

1. Clone Repository

git clone <your-repo-link>
cd <repo-folder>

2. Start Broker Server

python broker_server.py

You should see:
Secure Broker Server running...

3. Start Subscriber

Open a new terminal:
python subscriber_client.py

Enter topic:
Topic to subscribe: sports

4. Start Publisher

Open another terminal:
python publisher_client.py

Enter:
Topic: sports
Message: Hello World

---

## 📊 Performance Monitoring

The broker prints metrics every 10 seconds:

- Active clients
- Topics
- Messages processed
- Throughput (messages/sec)

---

## 🧪 Example Workflow

1. Subscriber subscribes to "sports"
2. Publisher sends message to "sports"
3. Broker forwards message to all subscribers
4. Subscriber receives message in real-time

---

## ⚠️ Limitations

- Uses blocking sockets (not async)
- No persistent storage
- No authentication for clients
- Message format is simple (colon-delimited)

---

## 🚀 Future Improvements

- Async (asyncio) based implementation
- Message persistence
- Authentication and authorization
- JSON-based protocol
- Load balancing for scalability

---

## 🧠 Key Concepts Used

- Socket Programming
- TLS/SSL Encryption
- Multithreading
- Synchronization (Locks)
- Pub/Sub Architecture

---

## 👨‍💻 Conclusion

This project demonstrates a secure, scalable messaging system with real-time communication and concurrency handling. It highlights core distributed systems concepts and secure network programming.

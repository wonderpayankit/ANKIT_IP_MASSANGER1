import socket
import threading
import os

BROADCAST_PORT = 2425

class NetworkHandler:
    def __init__(self, username, on_message_received):
        self.username = username
        self.on_message_received = on_message_received

        # UDP socket for discovery and messaging
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("", BROADCAST_PORT))

        # Start listening for messages
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def send_message(self, message):
        packet = f"1:12345:{self.username}:localhost:32:{message}"
        self.udp_socket.sendto(packet.encode(), ("<broadcast>", BROADCAST_PORT))

    def send_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        packet = f"1:12345:{self.username}:localhost:64:{file_name}:{file_size}"
        self.udp_socket.sendto(packet.encode(), ("<broadcast>", BROADCAST_PORT))

        # Send the actual file over TCP
        threading.Thread(target=self._send_file_tcp, args=(file_path,)).start()

    def _send_file_tcp(self, file_path):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(("", 0))
        tcp_socket.listen(1)
        port = tcp_socket.getsockname()[1]

        with open(file_path, "rb") as file:
            conn, _ = tcp_socket.accept()
            while chunk := file.read(1024):
                conn.send(chunk)
            conn.close()
        tcp_socket.close()

    def listen_for_messages(self):
        while True:
            data, addr = self.udp_socket.recvfrom(1024)
            message = data.decode()
            parts = message.split(":")
            if len(parts) > 5:
                sender = parts[2]
                content = parts[5]
                self.on_message_received(sender, content)

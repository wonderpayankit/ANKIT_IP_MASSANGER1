from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget, QFileDialog)
from PySide6.QtCore import Qt
import network
import database


class ChatApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LAN Messenger")
        self.setGeometry(100, 100, 600, 400)

        # UI Components
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.file_button = QPushButton("Send File")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.chat_area)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.file_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Signals
        self.send_button.clicked.connect(self.send_message)
        self.file_button.clicked.connect(self.send_file)

        # Networking setup
        self.username = "User"
        self.network_handler = network.NetworkHandler(self.username,
                                                      self.update_chat)

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.network_handler.send_message(message)
            self.chat_area.append(f"You: {message}")
            database.save_message("You", message)
            self.message_input.clear()

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.network_handler.send_file(file_path)
            self.chat_area.append(f"You sent a file: {file_path}")

    def update_chat(self, sender, message):
        self.chat_area.append(f"{sender}: {message}")
        database.save_message(sender, message)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())

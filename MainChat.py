# MainChat.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QScrollArea)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon

class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, client, text):
        super().__init__()
        self.client = client
        self.text = text

    def run(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": self.text}]
        )
        answer = response.choices[0].message.content
        self.finished.emit(answer)


class ChatWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.worker = None
        self.initUI()

    def send_message(self):
        text = self.textbox.text()
        if not text.strip():
            return
        self.button.setEnabled(False)
        if self.worker is not None and self.worker.isRunning():
            return
        self.worker = Worker(self.client, text)
        self.worker.finished.connect(self.show_answer)
        self.worker.start()

    def show_answer(self, answer):
        self.label.setText(answer)
        self.button.setEnabled(True)
        self.textbox.clear()

    def initUI(self):
        self.setStyleSheet("background-color:#424045")
        self.setWindowTitle("AI Chat Bot")
        self.setGeometry(100, 100, 1000, 700)
        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText("Enter your prompt...")
        self.textbox.setStyleSheet("background:#EEEEF0; height:30px; width:100px; border:none;border-radius:3px;color:black;")
        self.button = QPushButton("Send")
        self.button.setIcon(QIcon("fa-solid-comment.svg"))
        self.button.clicked.connect(self.send_message)
        self.button.setStyleSheet("background-color : #919192;height:30px; width:100px; border:none;border-radius:3px;")
        self.label = QLabel()
        self.label.setStyleSheet("padding:10px;background-color : #919192")
        self.label.setWordWrap(True)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.textbox)
        top_layout.addWidget(self.button)

        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(700)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(scroll_area)
        main_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

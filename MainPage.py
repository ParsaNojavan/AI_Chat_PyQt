from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from MainChat import ChatWindow  
from dotenv import load_dotenv
from openai import OpenAI
import sys
import os

load_dotenv()  # فایل .env رو بارگذاری می‌کنه

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key 
)

class HoverWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.normal_width = 100
        self.expanded_width = 150
        self.setFixedWidth(self.normal_width)

    def enterEvent(self, event):
        self.setFixedWidth(self.expanded_width)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setFixedWidth(self.normal_width)
        super().leaveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def open_dialog(self):
        self.chat_window = ChatWindow(client)
        self.chat_window.show()
        self.close()  

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Main Menu")
        self.setStyleSheet("background-color:#424045;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_widget = HoverWidget()
        left_layout = QVBoxLayout(left_widget)

        btn_Enter = QPushButton("AI Chat")
        btn_Enter.clicked.connect(self.open_dialog)
        btn_Enter.setStyleSheet("background:#919192; height:30px; width:100px; border:none;border-radius:3px;")

        left_layout.addWidget(btn_Enter)
        left_layout.addStretch()

        main_layout.addWidget(left_widget)

        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #787878; border-radius: 3px;")
        right_layout = QVBoxLayout(right_widget)

        main_layout.addWidget(right_widget)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

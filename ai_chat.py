from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, 
    QLineEdit, QPushButton
)
from ..widgets.gpt_handler import GPTHandler

class AIChatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.gpt = GPTHandler()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        
        btn_send = QPushButton("Send")
        btn_send.clicked.connect(self.send_message)
        
        layout.addWidget(self.chat_history)
        layout.addWidget(self.input_field)
        layout.addWidget(btn_send)
        self.setLayout(layout)
        
    def send_message(self):
        # Implementation for chat with AI
        pass
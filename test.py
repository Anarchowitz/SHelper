import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from openai import OpenAI

class AiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(180, 80, 721, 461)
        self.setWindowTitle("Chat with AI")

        # Создание виджетов
        self.textEdit = QTextEdit(self)
        self.sendButton = QPushButton("Send", self)
        self.responseEdit = QTextEdit(self)
        self.responseEdit.setReadOnly(True)

        # Установка компоновки
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.sendButton)
        layout.addWidget(self.responseEdit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Подключение кнопки к функции
        self.sendButton.clicked.connect(self.handle_send_button)

    def handle_send_button(self):
        user_message = self.textEdit.toPlainText()
        self.display_user_message(user_message)
        response = self.ai_message(user_message)
        self.display_ai_message(response)

    def display_user_message(self, message):
        self.responseEdit.append(f"You: {message}")
        self.textEdit.clear()  # Очистка текстового поля после отправки

    def display_ai_message(self, message):
        self.responseEdit.append(f"AI: {message}")

    def ai_message(self, user_message):
        client = OpenAI(
            api_key="sk-aitunnel-jJbl5JiPBgCygbIwCRpUFnK3PP0VHe8M",
            base_url="https://api.aitunnel.ru/v1/",
        )
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"{user_message}"}],
            max_tokens=1025,
            model="gpt-4o-mini"
        )
        end_message = completion.choices[0].message.content
        return end_message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AiWindow()
    window.show()
    sys.exit(app.exec_())
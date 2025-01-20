import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
import openai
import docx

class EssayGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Article Generator")
        self.setGeometry(300, 300, 1700, 1000)

        topic_label = QLabel('Enter the topic:', self)
        topic_label.move(20, 40)

        self.topic_input = QLineEdit(self)
        self.topic_input.move(20, 100)
        self.topic_input.resize(1200, 50)

        length_label = QLabel('Select Article Length:', self)
        length_label.move(320, 40)

        self.length_dropdown = QComboBox(self)
        self.length_dropdown.move(600, 40)
        self.length_dropdown.addItems(["500", "1000", "2000", "3000", "4000"])

        self.essay_output = QTextEdit(self)
        self.essay_output.move(20, 200)
        self.essay_output.resize(1500, 500)

        generate_button = QPushButton("Generate Essay", self)
        generate_button.move(1250, 100)
        generate_button.clicked.connect(self.generate_essay)

        save_button = QPushButton("Save", self)
        save_button.move(20, 750)
        save_button.clicked.connect(self.save_essay)

    def generate_essay(self):
        topic = self.topic_input.text()

        length = int(self.length_dropdown.currentText())

        openai.api_key = "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"
        engine = "text-davinci-003"

        prompt = "Write an article on the following topic: " + topic + "\n\n"

        response = openai.Completion.create(engine=engine, prompt=prompt, max_tokens=length)
        essay = response.choices[0].text

        self.essay_output.setText(essay)

    def save_essay(self):
        topic = self.topic_input.text()
        final_text = self.essay_output.toPlainText()

        document = docx.Document()
        document.add_paragraph(final_text)
        document.save(topic + ".docx")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssayGenerator()
    ex.show()
    sys.exit(app.exec_())





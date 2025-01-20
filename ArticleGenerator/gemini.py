import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                           QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QFrame,
                           QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
import requests
import json
import docx

class ModernFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            ModernFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

class EssayGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Modern Article Generator")
        self.setGeometry(300, 300, 1200, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                color: #1a1a1a;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit, QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4a90e2;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 8px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 12px 25px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d6da3;
            }
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 5px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_frame = ModernFrame()
        header_layout = QVBoxLayout(header_frame)
        title_label = QLabel("Article Generator", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title_label)
        main_layout.addWidget(header_frame)

        # Input section
        input_frame = ModernFrame()
        input_layout = QVBoxLayout(input_frame)

        # Topic input
        topic_layout = QHBoxLayout()
        topic_label = QLabel('Topic:', self)
        self.topic_input = QLineEdit(self)
        self.topic_input.setPlaceholderText("Enter your article topic here...")
        topic_layout.addWidget(topic_label, 1)
        topic_layout.addWidget(self.topic_input, 4)
        input_layout.addLayout(topic_layout)

        # Length selection
        length_layout = QHBoxLayout()
        length_label = QLabel('Length:', self)
        self.length_dropdown = QComboBox(self)
        self.length_dropdown.addItems(["500 words", "1000 words", "2000 words", "3000 words", "4000 words"])
        length_layout.addWidget(length_label, 1)
        length_layout.addWidget(self.length_dropdown, 4)
        input_layout.addLayout(length_layout)

        main_layout.addWidget(input_frame)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Output section
        output_frame = ModernFrame()
        output_layout = QVBoxLayout(output_frame)
        output_label = QLabel('Generated Article:', self)
        self.essay_output = QTextEdit(self)
        self.essay_output.setReadOnly(True)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.essay_output)
        main_layout.addWidget(output_frame)

        # Buttons
        button_layout = QHBoxLayout()
        generate_button = QPushButton("Generate Article")
        generate_button.clicked.connect(self.generate_essay)
        save_button = QPushButton("Save as Word")
        save_button.clicked.connect(self.save_essay)
        button_layout.addWidget(generate_button)
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def show_progress(self):
        self.progress_bar.setVisible(True)
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):
        self.progress += 5
        self.progress_bar.setValue(self.progress)
        if self.progress >= 100:
            self.timer.stop()
            self.progress_bar.setVisible(False)

    def generate_essay(self):
        if not self.topic_input.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a topic first!")
            return

        self.show_progress()
        topic = self.topic_input.text()
        length = int(self.length_dropdown.currentText().split()[0])
        gemini_api_key = "AIzaSyAAadKS6jNSX_s_1KadF1oyF6g7cXTOAfs"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{
                    "text": f"Write a {length}-word article on the following topic: {topic}\n\n"
                }]
            }]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                essay = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                self.essay_output.setText(essay)
            else:
                QMessageBox.critical(self, "Error", f"API Error: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def save_essay(self):
        if not self.essay_output.toPlainText():
            QMessageBox.warning(self, "Warning", "No article to save!")
            return

        try:
            topic = self.topic_input.text()
            final_text = self.essay_output.toPlainText()
            document = docx.Document()
            document.add_paragraph(final_text)
            filename = f"{topic.replace(' ', '_')}.docx"
            document.save(filename)
            QMessageBox.information(self, "Success", f"Article saved as {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save article: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssayGenerator()
    ex.show()
    sys.exit(app.exec_())
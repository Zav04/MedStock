from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit, QFrame
from PyQt5.QtCore import Qt
from APP.UI.ui_styles import Style
from APP.UI.WindowFunctions import WindowFunctions

class RejectionDialog(QDialog):
    def __init__(self, requerimento_id: int, parent=None):
        super().__init__(parent)
        self.requerimento_id = requerimento_id
        self.reason = ""
        self.was_cancelled = False

        WindowFunctions.removeTitleBar(self, True)

        container = QFrame(self)
        container.setStyleSheet(
            "border-radius: 10px;"
            "padding: 10px;"
            "background-color: #F3F3F3;"
        )
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(5)

        WindowFunctions.enableWindowDragging(self, container)

        title_label = QLabel(f"Rejeitar Requerimento: REQ-{self.requerimento_id}")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        container_layout.addWidget(title_label)

        instruction_label = QLabel("Escreva o motivo da rejeição:")
        instruction_label.setStyleSheet("font-size: 16px; color: black;")
        container_layout.addWidget(instruction_label)

        self.reason_box = QTextEdit()
        self.reason_box.setStyleSheet("font-size: 14px; color: black; border: 1px solid #ccc; border-radius: 5px;")
        self.reason_box.textChanged.connect(self.update_send_button_state)
        container_layout.addWidget(self.reason_box)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.cancel_rejection)
        self.cancel_button.setStyleSheet(Style.style_bt_QPushButton_Cancel)
        button_layout.addWidget(self.cancel_button)

        self.send_button = QPushButton("Rejeitar")
        self.send_button.clicked.connect(self.submit_rejection)
        self.send_button.setStyleSheet(Style.style_bt_QPushButton_Delete)
        self.send_button.setEnabled(False)
        button_layout.addWidget(self.send_button)

        container_layout.addLayout(button_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)

    def update_send_button_state(self):
        self.send_button.setEnabled(len(self.reason_box.toPlainText().strip()) >= 4)

    def submit_rejection(self):
        self.reason = self.reason_box.toPlainText().strip()
        self.accept()

    def cancel_rejection(self):
        self.was_cancelled = True
        self.reject()

    def get_reason(self):
        return self.reason

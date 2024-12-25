from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpinBox, QCheckBox, QPushButton, QTextEdit, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from Class.Requerimento import Requerimento
from APP.UI.ui_styles import Style
from APP.UI.WindowFunctions import WindowFunctions

class ValidationDialog(QDialog):
    def __init__(self, requerimento: Requerimento, parent=None):
        super().__init__(parent)
        self.requerimento = requerimento
        self.rejected_items = []
        self.observations = ""
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

        title_label = QLabel(f"Validar Requerimento: REQ-{requerimento.requerimento_id}")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        container_layout.addWidget(title_label)

        items_layout = QGridLayout()
        items_layout.setHorizontalSpacing(15)
        items_layout.setVerticalSpacing(10)

        header_label_item = QLabel("Consumivel")
        header_label_item.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        items_layout.addWidget(header_label_item, 0, 0)

        header_label_quantity = QLabel("Quantidade Recebida")
        header_label_quantity.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        items_layout.addWidget(header_label_quantity, 0, 1)

        header_label_validated = QLabel("Validado")
        header_label_validated.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        items_layout.addWidget(header_label_validated, 0, 2)
        
        # Adicionar itens na grade
        self.item_widgets = []
        for row, item in enumerate(requerimento.itens_pedidos, start=1):
            
            item_label = QLabel(f"{item.nome_item} (Solicitado: {item.quantidade})")
            item_label.setStyleSheet("font-size: 16px; color: black;")
            items_layout.addWidget(item_label, row, 0)

            spin_box = QSpinBox()
            spin_box.setMinimum(0)
            spin_box.setMaximum(99999)
            spin_box.setValue(item.quantidade)
            spin_box.setStyleSheet(Style.style_SpinBox)
            items_layout.addWidget(spin_box, row, 1)

            check_box = QCheckBox()
            check_box.setStyleSheet(Style.style_checkbox)
            items_layout.addWidget(check_box, row, 2,alignment=Qt.AlignCenter)
            
            spin_box.valueChanged.connect(self.update_buttons_state)
            check_box.stateChanged.connect(self.update_buttons_state)

            self.item_widgets.append((item, spin_box, check_box))

        container_layout.addLayout(items_layout)

        observation_label = QLabel("Observações:")
        observation_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        container_layout.addWidget(observation_label)

        self.observation_box = QTextEdit()
        self.observation_box.setStyleSheet("font-size: 14px; color: black; border: 1px solid #ccc; border-radius: 5px;")
        container_layout.addWidget(self.observation_box)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.cancel_validation)
        self.cancel_button.setStyleSheet(Style.style_bt_QPushButton_Cancel)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton("Validar")
        self.submit_button.clicked.connect(self.submit_validation)
        self.submit_button.setStyleSheet(Style.style_bt_QPushButton)
        self.submit_button.setEnabled(False)
        button_layout.addWidget(self.submit_button)

        self.reject_button = QPushButton("Rejeitar")
        self.reject_button.clicked.connect(self.reject_validation)
        self.reject_button.setEnabled(False)
        self.reject_button.setStyleSheet(Style.style_bt_QPushButton_Delete)
        
        button_layout.addWidget(self.reject_button)

        container_layout.addLayout(button_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)

    def update_buttons_state(self):
        all_valid = True
        any_rejected = False

        for item, spin_box, check_box in self.item_widgets:
            quantidade_correta = spin_box.value() == item.quantidade
            validado = check_box.isChecked()

            if not quantidade_correta or not validado:
                all_valid = False
            if not quantidade_correta and validado:
                any_rejected = True

        self.submit_button.setEnabled(all_valid)
        self.reject_button.setEnabled(any_rejected)


    def submit_validation(self):
        self.observations = self.observation_box.toPlainText()
        self.accept()

    def reject_validation(self):
        self.rejected_items = [
            {
                "consumivel_nome": item.nome_item,
                "quantidade_pedida": item.quantidade,
                "quantidade_recebida": spin_box.value(),
            }
            for item, spin_box, _ in self.item_widgets
            if spin_box.value() != item.quantidade
        ]

        self.observations = self.observation_box.toPlainText()
        self.reject()

    def cancel_validation(self):
        self.was_cancelled = True
        self.reject()
    def get_rejected_items(self):
        return self.rejected_items

    def get_observations(self):
        return self.observations

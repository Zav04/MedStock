from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QColor, QIcon
import sys

class AlertOverlay(QWidget):
    active_alerts = []

    def __init__(self, message, alert_type="success", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Configurações de cores e ícone de acordo com o tipo de alerta
        if alert_type == "error":
            bgcolor = QColor("#ffcccc")
            border_color = QColor("#cc0000")
            icon_path = "./icons/MaterialIcons/error.png"  # Use o caminho do ícone de erro
        elif alert_type == "success":
            bgcolor = QColor("#ccffcc")
            border_color = QColor("#00cc00")
            icon_path = "./icons/MaterialIcons/warning.png"  # Use o caminho do ícone de sucesso
        elif alert_type == "warning":
            bgcolor = QColor("#ffffcc")
            border_color = QColor("#ffcc00")
            icon_path = "./icons/MaterialIcons/warning.png"  # Use o caminho do ícone de aviso

        # Layout e estilo do container
        layout = QVBoxLayout()
        self.setStyleSheet(f"""
            background-color: {bgcolor.name()};
            border: 2px solid {border_color.name()};
            border-radius: 8px;
            padding: 10px;
            min-width: 300px;
        """)

        # Ícone e mensagem
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(30, 30))
        message_label = QLabel(message)

        # Botão de fechamento
        close_button = QPushButton("X")
        close_button.clicked.connect(self.close_overlay)
        close_button.setStyleSheet("background: none; border: none; color: black;")

        # Adicionando elementos ao layout
        layout.addWidget(icon_label)
        layout.addWidget(message_label)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        self.setLayout(layout)

        # Adiciona este alerta à lista de ativos e atualiza posições
        AlertOverlay.active_alerts.append(self)
        self.update_overlay_positions(parent)

        # Timer para fechar automaticamente após 5 segundos
        QTimer.singleShot(5000, self.close_overlay)

    def update_overlay_positions(self, parent):
        # Posição base do canto superior direito
        if parent:
            base_x = parent.geometry().right() - 310  # Ajuste de 10 px da borda direita
            base_y = parent.geometry().top() + 10    # Ajuste de 10 px da borda superior

            for idx, overlay in enumerate(AlertOverlay.active_alerts):
                overlay.move(base_x, base_y + idx * 80)  # Espaçamento entre os alertas
                overlay.show()

    def close_overlay(self):
        if self in AlertOverlay.active_alerts:
            AlertOverlay.active_alerts.remove(self)
            self.update_overlay_positions(self.parent())
        self.close()


# Testando o sistema de overlays
# def main():
#     app = QApplication(sys.argv)
#     main_window = QWidget()
#     main_window.resize(800, 600)
#     main_window.show()

#     # Exemplos de alertas
#     AlertOverlay("Este é um alerta de sucesso!", alert_type="success", parent=main_window)
#     AlertOverlay("Este é um alerta de erro!", alert_type="error", parent=main_window)
#     AlertOverlay("Este é um alerta de aviso!", alert_type="warning", parent=main_window)

#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

from PyQt5.QtCore import QMetaObject, Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QWidget, QPushButton, QSizePolicy

class Ui_ResetPassword(QDialog):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        # Configuração básica do diálogo
        Dialog.setObjectName("ResetPasswordDialog")
        Dialog.setMaximumSize(QSize(500, 500))
        Dialog.setMinimumSize(QSize(500, 500))
        Dialog.setAttribute(Qt.WA_TranslucentBackground)
        Dialog.setWindowFlags(Qt.FramelessWindowHint)
        Dialog.setStyleSheet("QDialog {background: transparent; }\n"
                             "QToolTip {\n"
                             "	color: #ffffff;\n"
                             "	background-color: rgba(27, 29, 35, 160);\n"
                             "	border: 1px solid rgb(40, 40, 40);\n"
                             "	border-radius: 2px;\n"
                             "}")

        # Widget central do layout
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background: transparent;\n"
                                         "color: #dbd7d7;")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)

        # Frame principal
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Adicionar layout de frame_main ao layout horizontal do centralwidget
        self.horizontalLayout.addWidget(self.frame_main)
        Dialog.setLayout(self.horizontalLayout)  # Configura o layout para o QDialog

        # Frame superior
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName("frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(16777215, 65))
        self.frame_top.setStyleSheet("background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMaximumSize(QSize(16777215, 16777215))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy1)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-image: url(icons/MedStock/favicon.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_bar_top.setFont(font)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;\n""")
        self.horizontalLayout_10.addWidget(self.label_title_bar_top)
        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy1.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy1)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy2.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy2)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #81C784;\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #4CAF50;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/20x20/icons/20x20/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)
        self.horizontalLayout_5.addWidget(self.btn_close)
        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top_btns)
        self.horizontalLayout_3.addWidget(self.frame_top_right)
        self.verticalLayout.addWidget(self.frame_top)

        # Frame central
        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName("frame_center")
        self.frame_center.setStyleSheet("background-color: #b5c6bf;")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        
        # Frame de conteúdo completo
        self.frame_content_full = QFrame(self.frame_center)
        self.frame_content_full.setObjectName("frame_content_full")
        self.frame_content_full.setStyleSheet("background-color: #F9F9F9;")
        self.frame_content_full.setFrameShape(QFrame.NoFrame)
        self.frame_content_full.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_full)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        # Frame de conteúdo central
        self.frame_content = QFrame(self.frame_content_full)
        self.frame_content.setObjectName("frame_content")
        self.frame_content.setStyleSheet("background-color: transparent;")
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)
        self.content_layout = QVBoxLayout(self.frame_content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Adicionar conteúdo ao frame_content
        self.verticalLayout_4.addWidget(self.frame_content)

        # Frame da barra inferior
        self.frame_grip = QFrame(self.frame_content_full)
        self.frame_grip.setObjectName("frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)

        # Adiciona o frame_grip à barra de conteúdo completa
        self.verticalLayout_4.addWidget(self.frame_grip)

        # Adicionar o frame_content_full ao layout horizontal_2
        self.horizontalLayout_2.addWidget(self.frame_content_full)

        # Adicionar o frame_center ao layout vertical de frame_main
        self.verticalLayout.addWidget(self.frame_center)

        # Conectar todos os slots
        QMetaObject.connectSlotsByName(Dialog)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,QFileDialog, QScrollArea, QSizePolicy, QDialog
from PyQt5.QtGui import QFont, QIcon, QCursor,QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer
from datetime import datetime
from Class.Requerimento import Requerimento
from Class.Utilizador import Utilizador
from Pages.Requerimento.ValidationDialog import ValidationDialog
from APP.UI.ui_functions import UIFunctions
import os
from APP.Label.Label import add_status_lable
from APP.Overlays.Overlay import Overlay
from APP.PDF.Generate_PDF import GeneratePdfRequerimento
from API.API_PUT_Request import (API_CancelRequerimento, API_AcceptRequerimento, API_RejectRequerimento, 
                                API_StandByRequerimento, API_ResumeRequerimento, API_PrepareRequerimento,
                                API_SendRequerimento, API_FinishRequerimento, API_ReavaliationRequerimento,
                                API_UpdateRequerimentoExterno)
from API.API_POST_Request import API_SendEmailRequerimentoStatus


class RequerimentoCard(QWidget):
    def __init__(self, user:Utilizador, requerimento: Requerimento, update_callback=None,parent_page=None):
        super().__init__()
        self.user = user
        self.requerimento = requerimento
        self.parent_page = parent_page
        self.expanded = False
        self.callbackUpdate = update_callback
        self.minimumHeight_Card = 180

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.layout().setSpacing(5)

        # Container principal
        self.container = QFrame()
        self.container.setFrameShape(QFrame.StyledPanel)
        self.container.setStyleSheet("background-color: #F3F3F3; border: 1px solid #ddd; border-radius: 8px;")
        self.container.setMaximumHeight(self.minimumHeight_Card)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 15, 15, 15)
        self.container_layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        # Esquerda: ID e Data
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        id_label = QLabel(f"REQ-{self.requerimento.requerimento_id} - {self.requerimento.tipo_requerimento}")
        id_label.setFont(QFont("Arial", 16, QFont.Bold))
        id_label.setStyleSheet("color: #333;border:none;")
        left_layout.addWidget(id_label)

        data_pedido = (
            datetime.strptime(self.requerimento.data_pedido, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y %H:%M")
            if self.requerimento.data_pedido else "------------"
        )
        data_label = QLabel(data_pedido)
        data_label.setFont(QFont("Arial", 12))
        data_label.setStyleSheet("color: #555;border:none;")
        left_layout.addWidget(data_label)
        header_layout.addLayout(left_layout)

        # Centro: Status
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        status_label = add_status_lable(self.requerimento.status_atual)
        status_layout.addWidget(status_label, alignment=Qt.AlignCenter)
        header_layout.addLayout(status_layout)

        # Direita: Botões de ação
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.setAlignment(Qt.AlignRight)
        

        if self.requerimento.status_atual == 0 and (user.role_nome=="Gestor Responsável" or user.role_nome!="Farmacêutico") and self.requerimento.tipo_requerimento=="Interno":
            delete_button = QPushButton()
            recolored_icon_delete = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/close.png"), "#f54251"))
            delete_button.setIcon(recolored_icon_delete)
            delete_button.setIconSize(QSize(24, 24))
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setStyleSheet(self.button_style("#f54251"))
            actions_layout.addWidget(delete_button, alignment=Qt.AlignRight)
            if(user.role_nome=="Gestor Responsável"):
                delete_button.clicked.connect(lambda: self.reject_requerimento())
            elif user.role_nome!="Farmacêutico":
                delete_button.clicked.connect(lambda: self.cancel_requerimento())

        if self.requerimento.status_atual == 0 and user.role_nome=="Gestor Responsável" and self.requerimento.tipo_requerimento=="Interno":
            accept_button = QPushButton()
            recolored_accept_button = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/check.png"), "#b5c6bf"))
            accept_button.setIcon(recolored_accept_button)
            accept_button.setIconSize(QSize(24, 24))
            accept_button.setCursor(QCursor(Qt.PointingHandCursor))
            accept_button.setStyleSheet(self.button_style("#b5c6bf"))
            accept_button.clicked.connect(lambda: self.accept_requerimento())
            actions_layout.addWidget(accept_button, alignment=Qt.AlignRight)

        if (self.requerimento.status_atual == 1 or self.requerimento.status_atual == 10) and user.role_nome=="Farmacêutico" and self.requerimento.tipo_requerimento=="Interno":
            stand_by_button = QPushButton()
            recolored_icon_stand_by = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/pause_circle.png"), "#eb8c34"))
            stand_by_button.setIcon(recolored_icon_stand_by)
            stand_by_button.setIconSize(QSize(24, 24))
            stand_by_button.setCursor(QCursor(Qt.PointingHandCursor))
            stand_by_button.setStyleSheet(self.button_style("#eb8c34"))
            actions_layout.addWidget(stand_by_button, alignment=Qt.AlignRight)
            stand_by_button.clicked.connect(lambda: self.stand_by_requerimento())

        if (self.requerimento.status_atual == 1 or self.requerimento.status_atual == 10) and user.role_nome=="Farmacêutico":
            pistola_button = QPushButton()
            recolored_icon_pistola_button = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/barcode_reader.png"), "#4287f5"))
            pistola_button.setIcon(recolored_icon_pistola_button)
            pistola_button.setIconSize(QSize(24, 24))
            pistola_button.setCursor(QCursor(Qt.PointingHandCursor))
            pistola_button.setStyleSheet(self.button_style("#4287f5"))
            actions_layout.addWidget(pistola_button, alignment=Qt.AlignRight)
            pistola_button.clicked.connect(lambda: self.prepare_requerimento())

        if self.requerimento.status_atual == 6 and user.role_nome=="Farmacêutico" and self.requerimento.tipo_requerimento=="Interno":
            resume_button = QPushButton()
            recolored_icon_resume_button = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/play.png"), "#b5c6bf"))
            resume_button.setIcon(recolored_icon_resume_button)
            resume_button.setIconSize(QSize(24, 24))
            resume_button.setCursor(QCursor(Qt.PointingHandCursor))
            resume_button.setStyleSheet(self.button_style("#b5c6bf"))
            actions_layout.addWidget(resume_button, alignment=Qt.AlignRight)
            resume_button.clicked.connect(lambda: self.resume_requerimento())
            
        
        if self.requerimento.status_atual == 3 and user.role_nome=="Farmacêutico":
            send_button = QPushButton()
            recolored_icon_send_button = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/package.png"), "#4287f5"))
            send_button.setIcon(recolored_icon_send_button)
            send_button.setIconSize(QSize(24, 24))
            send_button.setCursor(QCursor(Qt.PointingHandCursor))
            send_button.setStyleSheet(self.button_style("#4287f5"))
            actions_layout.addWidget(send_button, alignment=Qt.AlignRight)
            if self.requerimento.tipo_requerimento=="Interno":
                send_button.clicked.connect(lambda: self.send_requerimento())
            else:
                send_button.clicked.connect(lambda: self.send_requerimento_externo())
        
        if self.requerimento.status_atual == 8 and (user.role_nome != "Farmacêutico" and user.role_nome != "Gestor Responsável") and self.requerimento.tipo_requerimento=="Interno":
            validate_button = QPushButton()
            recolored_icon_validate = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/play.png"), "#b5c6bf"))
            validate_button.setIcon(recolored_icon_validate)
            validate_button.setIconSize(QSize(24, 24))
            validate_button.setCursor(QCursor(Qt.PointingHandCursor))
            validate_button.setStyleSheet(self.button_style("#b5c6bf"))
            actions_layout.addWidget(validate_button, alignment=Qt.AlignRight)
            validate_button.clicked.connect(lambda: self.open_validation_window())
        
        if self.requerimento.status_atual == 11 and user.role_nome == "Farmacêutico" and self.requerimento.tipo_requerimento=="Externo":
                add_consumivel_button = QPushButton()
                recolored_icon_add_consumivel_button = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/prescriptions.png"), "#b5c6bf"))
                add_consumivel_button.setIcon(recolored_icon_add_consumivel_button)
                add_consumivel_button.setIconSize(QSize(24, 24))
                add_consumivel_button.setCursor(QCursor(Qt.PointingHandCursor))
                add_consumivel_button.setStyleSheet(self.button_style("#b5c6bf"))
                actions_layout.addWidget(add_consumivel_button, alignment=Qt.AlignRight)
                add_consumivel_button.clicked.connect(lambda: self.open_create_requerimento_page())

        download_button = QPushButton()
        download_button.setIcon(QIcon("./icons/MaterialIcons/picture_as_pdf.png"))
        download_button.setIconSize(QSize(24, 24))
        download_button.setCursor(QCursor(Qt.PointingHandCursor))
        download_button.setStyleSheet(self.button_style("#f54251"))
        download_button.clicked.connect(lambda: self.choose_file_location_GeneratePdfRequerimento())
        actions_layout.addWidget(download_button, alignment=Qt.AlignRight)

        
        self.details_button = QPushButton()
        recolored_icon_details = QIcon(UIFunctions.recolor_icon(os.path.abspath("./icons/MaterialIcons/visibility.png"), "#4287f5"))
        self.details_button.setIcon(recolored_icon_details)
        self.details_button.setIconSize(QSize(24, 24))
        self.details_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.details_button.setStyleSheet(self.button_style("#4287f5"))
        self.details_button.clicked.connect(self.toggle_details)
        actions_layout.addWidget(self.details_button, alignment=Qt.AlignRight)

        header_layout.addLayout(actions_layout)
        self.container_layout.addLayout(header_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVisible(False)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.details_frame = QFrame()
        self.details_frame.setStyleSheet("border: none;")
        self.details_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.details_layout = QVBoxLayout(self.details_frame)
        self.details_layout.setContentsMargins(10, 10, 10, 10)
        self.details_layout.setSpacing(5)

        if(self.requerimento.tipo_requerimento=="Interno"):
            setor_label = QLabel()
            setor_label.setText(f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Setor:</span> <span style='font-size:14px; color:#000000;'>{self.requerimento.setor_nome_localizacao or 'Não atribuído'}</span>")
            setor_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(setor_label)

            utilizador_pedido_label = QLabel()
            utilizador_pedido_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Solicitado por:</span> "
                f"<span style='font-size:14px; color:#555555;'>{self.requerimento.nome_utilizador_pedido or 'Desconhecido'}</span>"
            )
            utilizador_pedido_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(utilizador_pedido_label)

            itens_label = QLabel()
            itens_label.setText(
                "<span style='font-size:16px; font-weight:bold; color:#000000;'>Itens Pedidos:</span>"
            )
            itens_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(itens_label)
        else:
            utilizador_pedido_label = QLabel()
            utilizador_pedido_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Solicitado por:</span> "
                f"<span style='font-size:14px; color:#555555;'>{self.requerimento.nome_utilizador_pedido or 'Desconhecido'}</span>"
            )
            utilizador_pedido_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(utilizador_pedido_label)
            
            paciente_nome_label = QLabel()
            paciente_nome_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Nome do Doente:</span> "
                f"<span style='font-size:14px; color:#555555;'>{self.requerimento.paciente_nome or 'Desconhecido'}</span>"
            )
            paciente_nome_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(paciente_nome_label)

            paciente_estado_label = QLabel()
            paciente_estado_label.setText(
                f"<span style='font-size:16px; font-weight:bold; color:#000000;'>Estado do Doente:</span> "
                f"<span style='font-size:14px; color:#555555;'>{self.requerimento.paciente_estado or 'Desconhecido'}</span>"
            )
            paciente_estado_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(paciente_estado_label)
            
            
        if(self.requerimento.tipo_requerimento=="Interno"):
            if self.requerimento.itens_pedidos:
                for item in self.requerimento.itens_pedidos:
                    nome_consumivel = item.nome_item or "Item desconhecido"
                    quantidade = item.quantidade or "Quantidade não especificada"
                    tipo_item = item.tipo_item or "Tipo não especificado"

                    if tipo_item == "Medicamento":
                        icon_path = "./icons/MaterialIcons/medicamento.png"
                    elif tipo_item == "Vacinas":
                        icon_path = "./icons/MaterialIcons/vacina.png"
                    elif tipo_item == "Material Hospitalar":
                        icon_path = "./icons/MaterialIcons/material_hospitalar.png"
                    elif tipo_item == "Outros":
                        icon_path = "./icons/MaterialIcons/outro.png"
                    else:
                        icon_path = None

                    item_layout = QHBoxLayout()

                    if icon_path:
                        icon_label = QLabel()
                        icon_label.setPixmap(QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        icon_label.setFixedSize(20, 20)
                        item_layout.addWidget(icon_label)

                    item_text_label = QLabel()
                    item_text_label.setText(
                        f"<span style='font-size:14px; color:#000000;'>"
                        f"{nome_consumivel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>(Quantidade: {quantidade})</span>"
                    )
                    item_text_label.setFont(QFont("Arial"))
                    item_layout.addWidget(item_text_label)

                    self.details_layout.addLayout(item_layout)
            else:                
                    no_items_label = QLabel("<span style='font-size:14px; color:#555555;'>Nenhum item pedido.</span>")
                    no_items_label.setFont(QFont("Arial"))
                    no_items_label.setTextFormat(Qt.RichText)
                    self.details_layout.addWidget(no_items_label)


        historico_label = QLabel()
        historico_label.setText(
            "<span style='font-size:16px; font-weight:bold; color:#000000;'>Histórico:</span>"
        )
        historico_label.setFont(QFont("Arial"))
        self.details_layout.addWidget(historico_label)
        
        if self.requerimento.tipo_requerimento == "Interno":
            self.historicoInternos()
        else:
            self.historicoExternos()
            

        self.details_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.details_frame.setLayout(self.details_layout)
        self.scroll_area.setWidget(self.details_frame)
        self.container_layout.addWidget(self.scroll_area)
        self.layout().addWidget(self.container)
        
        if self.requerimento.urgente:
            self.container.setStyleSheet("background-color: #f8d7da; border: 1px solid #f5c2c7; border-radius: 8px;")

    def open_create_requerimento_page(self):
        if self.parent_page:
            self.parent_page.show_create_requerimento_externo_page_wrapper(self.requerimento)
        else:
            Overlay.show_error(self, "Não foi possível abrir a página de escolher consumiveis e o setor para o requerimento.")
            
    def send_requerimento_externo(self):
        self.send_requerimento()
        self.finishRequerimento()
        

    def cancel_requerimento(self):
        response = API_CancelRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            Overlay.show_information(self, f'Requerimento {self.requerimento.requerimento_id} foi cancelado')
            self.callbackUpdate()
        else:
            Overlay.show_error(self, response.error_message)
            
    def stand_by_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_StandByRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            if self.requerimento.tipo_requerimento == "Interno":
                stringAlerts=f'Requerimento {self.requerimento.requerimento_id} foi colocado em stand by e email enviado ao requerente'
                QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
            else:
                Overlay.show_information(top_parent, f'Requerimento {self.requerimento.requerimento_id} foi colocado em stand by')
        else:
            Overlay.show_error(top_parent, response.error_message)
    
    def resume_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_ResumeRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            if self.requerimento.tipo_requerimento == "Interno":
                stringAlerts=f'Requerimento {self.requerimento.requerimento_id} voltou para a lista de espera e email enviado ao requerente'
                QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
            else:
                self.callbackUpdate()
                Overlay.show_information(top_parent, f'Requerimento {self.requerimento.requerimento_id} voltou para a lista de espera')
        else:
            Overlay.show_error(top_parent, response.error_message)
            
    def prepare_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_PrepareRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            stringAlerts=f'Requerimento {self.requerimento.requerimento_id} esta em preparação e email enviado ao requerente'
            QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
        else:
            self.callbackUpdate()
            Overlay.show_error(top_parent, response.error_message)
            
    def send_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_SendRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            if self.requerimento.tipo_requerimento == "Interno":
                stringAlerts=f'Requerimento {self.requerimento.requerimento_id} foi entregue e email enviado ao requerente'
                QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
            else:
                self.callbackUpdate()
                Overlay.show_information(top_parent, f'Requerimento {self.requerimento.requerimento_id} foi entregue')
        else:
            Overlay.show_error(top_parent, response.error_message)
    
    def accept_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_AcceptRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            stringAlerts=f'Requerimento {self.requerimento.requerimento_id} foi aceite e email enviado ao requerente'
            QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
        else:
            Overlay.show_error(top_parent, response.error_message)

    def reject_requerimento(self):
        top_parent = self.get_top_parent()
        response = API_RejectRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id)
        if response.success:
            stringAlerts=f'Requerimento {self.requerimento.requerimento_id} foi recusado e email enviado ao requerente'
            QTimer.singleShot(0, lambda: self.send_email_update(self.requerimento.requerimento_id, top_parent, stringAlerts))
        else:
            Overlay.show_error(top_parent, response.error_message)
    
    
    def historicoInternos(self):
        for hist in self.requerimento.historico:
            historico_text_label = QLabel()
            match hist.requerimento_status:
                case 0:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Pedido criado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                    )
                case 1:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Avaliado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 2:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Pedido enviado para preparar por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 3:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Preparado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 4:
                    descricao_texto = ""
                    if hist.descricao:
                        descricao_limpa = hist.descricao.replace("Requerimento finalizado.", "").strip()
                        if descricao_limpa:
                            descricao_texto = (
                                f"<br><span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                f"Comentário:</span> "
                                f"<span style='font-size:14px; color:#555555;'>{descricao_limpa}</span>"
                            )
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Finalizado e Validado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        f"{descricao_texto}"
                    )
                case 5:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Recusado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        #f"<br><span style='font-size:14px; color:#555555;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Motivo: {hist.descricao}</span>"
                        )
                case 6:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Colocado em Stand By por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 7:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Cancelado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 8:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Enviado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 9:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Colocado em Re-Validação por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                case 10:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Requerimento enviado novamente para a lista de espera por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                    
            historico_text_label.setFont(QFont("Arial"))
            self.details_layout.addWidget(historico_text_label)


    def historicoExternos(self):
        for hist in self.requerimento.historico:
            historico_text_label = QLabel()

            match hist.requerimento_status:
                case 11:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Pedido Externo criado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>")
                    historico_text_label.setFont(QFont("Arial"))
                    self.details_layout.addWidget(historico_text_label)
                case 2:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Consumiveis e Setor Selecionado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                    )
                    historico_text_label.setFont(QFont("Arial"))
                    self.details_layout.addWidget(historico_text_label)

                    setor_label = QLabel()
                    setor_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Setor:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{self.requerimento.setor_nome_localizacao or 'Setor não especificado'}</span>"
                    )
                    setor_label.setFont(QFont("Arial"))
                    self.details_layout.addWidget(setor_label)

                    for item in self.requerimento.itens_pedidos:
                        nome_consumivel = item.nome_item or "Item desconhecido"
                        quantidade = item.quantidade or "Quantidade não especificada"
                        tipo_item = item.tipo_item or "Tipo não especificado"

                        if tipo_item == "Medicamento":
                            icon_path = "./icons/MaterialIcons/medicamento.png"
                        elif tipo_item == "Vacinas":
                            icon_path = "./icons/MaterialIcons/vacina.png"
                        elif tipo_item == "Material Hospitalar":
                            icon_path = "./icons/MaterialIcons/material_hospitalar.png"
                        elif tipo_item == "Outros":
                            icon_path = "./icons/MaterialIcons/outro.png"
                        else:
                            icon_path = None

                        item_layout = QHBoxLayout()

                        spacer_label = QLabel()
                        spacer_label.setFixedSize(90, 20)
                        item_layout.addWidget(spacer_label)

                        if icon_path:
                            icon_label = QLabel()
                            icon_label.setPixmap(QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                            icon_label.setFixedSize(20, 20)
                            item_layout.addWidget(icon_label)

                        item_text_label = QLabel()
                        item_text_label.setText(
                            f"<span style='font-size:14px; color:#000000;'>"
                            f"{nome_consumivel}</span> "
                            f"<span style='font-size:14px; color:#555555;'>(Quantidade: {quantidade})</span>"
                        )
                        item_text_label.setFont(QFont("Arial"))
                        item_layout.addWidget(item_text_label)

                        self.details_layout.addLayout(item_layout)
                        
                    historico_text_label_2 = QLabel()    
                    historico_text_label_2.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Pedido enviado para preparar por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                    )
                    historico_text_label_2.setFont(QFont("Arial"))
                    self.details_layout.addWidget(historico_text_label_2)
                case 3:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Preparado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                        )
                    historico_text_label.setFont(QFont("Arial"))
                    self.details_layout.addWidget(historico_text_label)
                case 4:
                    historico_text_label.setText(
                        f"<span style='font-size:16px; font-weight:bold; color:#000000;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Finalizado por:</span> "
                        f"<span style='font-size:14px; color:#555555;'>{hist.user_responsavel}</span> "
                        f"<span style='font-size:14px; color:#555555;'>em {datetime.strptime(hist.data, '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y %H:%M')}</span>"
                    )
                    historico_text_label.setFont(QFont("Arial"))
                    self.details_layout.addWidget(historico_text_label)

    def send_email_update(self, requerimento_id, top_parent, stringAlerts):
        response=API_SendEmailRequerimentoStatus(requerimento_id)
        if response.success:
            self.callbackUpdate()
            Overlay.show_information(top_parent, stringAlerts)
        else:
            Overlay.show_error(top_parent, response.error_message)

    def toggle_details(self):
        self.expanded = not self.expanded

        if self.expanded:
            self.scroll_area.setVisible(True)
            self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.container.setMaximumHeight(500)
            self.scroll_area.setMaximumHeight(500)
        else:
            self.scroll_area.setVisible(False)
            self.container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.container.setMaximumHeight(self.minimumHeight_Card)
        
        self.container.updateGeometry()
        self.updateGeometry()


    def open_requerimento_page(self):
        self.parent.show_requerimentoExterno_wrapper(self.requerimento)
        
    def open_validation_window(self, ):
        top_parent = self.get_top_parent()
        validation_dialog = ValidationDialog(self.requerimento, self)
        result = validation_dialog.exec_()

        if result == QDialog.Accepted:
            observations = validation_dialog.get_observations()
            self.finishRequerimento(observations)
        elif validation_dialog.was_cancelled:
            Overlay.show_information(top_parent, "Validação Cancelada!")
        elif result == QDialog.Rejected:
            rejected_items = validation_dialog.get_rejected_items()
            observations = validation_dialog.get_observations()
            self.reavaliationRequerimento(rejected_items, observations)

    def finishRequerimento(self, observations: str = ""):
        top_parent = self.get_top_parent()
        response = API_FinishRequerimento(self.user.utilizador_id, self.requerimento.requerimento_id, observations)
        if response.success:
            Overlay.show_information(top_parent, f"Requerimento {self.requerimento.requerimento_id} finalizado com sucesso!")
            self.callbackUpdate()
        else:
            Overlay.show_error(top_parent, response.error_message)
            
    def reavaliationRequerimento(self, rejected_items, observations):
        top_parent = self.get_top_parent()
        response = API_ReavaliationRequerimento(self.user.utilizador_id,self.requerimento.requerimento_id, rejected_items, observations)
        if response.success:
            Overlay.show_information(top_parent, f"Requerimento {self.requerimento.requerimento_id} rejeitado com sucesso!")
            self.callbackUpdate()
        else:
            Overlay.show_error(top_parent, response.error_message)


    def choose_file_location_GeneratePdfRequerimento(self):
        top_parent = self.get_top_parent()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar PDF", 
            "", 
            "PDF Files (*.pdf);;All Files (*)", 
            options=options
        )
        if file_path:
            GeneratePdfRequerimento(file_path, self.requerimento)
            Overlay.show_information(top_parent, "PDF guardado na localização "+file_path)
            
            
    def choose_file_location_GeneratePdfRequerimentoExterno(self):
        top_parent = self.get_top_parent()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar PDF", 
            "", 
            "PDF Files (*.pdf);;All Files (*)", 
            options=options
        )
        if file_path:
            GeneratePdfRequerimento(file_path, self.requerimento)
            Overlay.show_information(top_parent, "PDF guardado na localização "+file_path)

    def get_top_parent(widget):
        parent = widget
        while parent.parentWidget() is not None:
            parent = parent.parentWidget()
        return parent

    @staticmethod
    def button_style(color):
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:], 16)}, 51);
            }}
            QPushButton:pressed {{
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:], 16)}, 127);
            }}
        """
        

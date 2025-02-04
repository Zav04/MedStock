from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QComboBox, QCheckBox,QSizePolicy,QLineEdit
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.Utilizador import Utilizador
from Class.Requerimento import Requerimento
from API.API_GET_Request import (API_GetRequerimentosByUser, API_GetRequerimentosByResponsavel,
                                API_GetSectors, API_GetConsumiveis, API_GetRequerimentosByFarmaceutico)
from API.API_POST_Request import API_CreateRequerimento
from API.API_PUT_Request import API_UpdateRequerimentoExterno
from APP.Card.Card import RequerimentoCard
from Class.ConsumivelManager import ConsumivelManager
from APP.UI.ui_functions import UIFunctions
from Pages.Requerimento.ui_DragAndDrop_Itens import DraggableLabel, DropZone, DropLabel
from Pages.p_Consumiveis import ConsumiveisTablePage
import asyncio


class RequerimentoPage(QWidget):
    def __init__(self, user: Utilizador, consumivel_manager: ConsumivelManager , page_stock: ConsumiveisTablePage):
        super().__init__()
        self.user = user
        self.page_stock = page_stock
        self.consumivel_manager = consumivel_manager
        self.main_layout = QVBoxLayout(self)
        self.current_requerimentos = []
        self.ui_updated = False
        self.current_filter = None
        self.current_requerimentos_dict = {}
        self.setup_RequerimentoPage()
        asyncio.create_task(self.load_requerimentos(self.user))
        
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.load_requerimentos_wrapper)
        self.update_timer.start(60000)

    def setup_RequerimentoPage(self):
        self.setup_page=True
        title_layout = QHBoxLayout()
        self.title = QLabel("REQUERIMENTOS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        if self.user.role_nome != "Gestor Responsável" and self.user.role_nome != "Farmacêutico" and self.user.role_nome != "Administrador":
            self.create_button = QPushButton("CRIAR NOVO REQUERIMENTO")
            self.create_button.setFixedSize(400, 40)
            self.create_button.setStyleSheet(Style.style_bt_QPushButton)
            self.create_button.clicked.connect(self.show_create_requerimento_interno_page_wrapper)
            title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)


        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(50)
        
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)


        self.filter_buttons = {}
        if self.user.role_nome == "Farmacêutico":
            filter_buttons = [
                ("Pendentes de Resposta", "Pendentes de Resposta"),
                ("Todos", "Todos"),
                ("Urgente", "Urgente"),
                ("Na Lista de Espera", "Status_1"),
                ("Em Preparação", "Status_2"),
                ("Pronto para Entrega", "Status_3"),
                ("Finalizado", "Status_4"),
                ("Stand-By", "Status_6"),
                ("Em Validação", "Status_8"),
                ("Externo", "Externo")
            ]
        else:
            filter_buttons = [
                ("Pendentes de Resposta", "Pendentes de Resposta"),
                ("Todos", "Todos"),
                ("Urgente", "Urgente"),
                ("Espera de Aprovação", "Status_0"),
                ("Na Lista de Espera", "Status_1"),
                ("Em Preparação", "Status_2"),
                ("Pronto para Entrega", "Status_3"),
                ("Finalizado", "Status_4"),
                ("Recusado", "Status_5"),
                ("Stand-By", "Status_6"),
                ("Cancelado", "Status_7"),
            ]
            
        self.current_filter = "Pendentes de Resposta"

        for label, key in filter_buttons:
            button = QPushButton(label)
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            button.setStyleSheet(Style.style_bt_QPushButton_Filter)
            button.clicked.connect(lambda checked, k=key: self.apply_filter(k))
            self.filter_buttons[key] = button
            filter_layout.addWidget(button)
        

        self.main_layout.addLayout(filter_layout)
        self.main_layout.addSpacing(15)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)
        

        self.setLayout(self.main_layout)


    async def show_create_requerimento_page(self):
        self.clear_layout(self.main_layout)
        self.all_consumivel = []
        self.create_page_layout = QVBoxLayout()

        back_button = QPushButton()
        back_button.setFixedSize(100, 40)
        back_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/arrow_back.png", "#b5c6bf")))
        back_button.setStyleSheet(Style.style_bt_QPushButton)
        back_button.clicked.connect(self.reload_page_requerimentos)
        back_button.setText("Voltar")
        back_button.setIconSize(QSize(20, 20))
        self.create_page_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        self.content_layout = QVBoxLayout()
        
        self.create_page_layout.setSpacing(20)
        self.filter_line_edit = QLineEdit()
        self.filter_line_edit.setPlaceholderText("Digite para filtrar os itens...")
        self.filter_line_edit.setFixedHeight(30)
        self.filter_line_edit.setFixedWidth(650)
        self.filter_line_edit.setStyleSheet(Style.style_QlineEdit)
        self.filter_line_edit.textChanged.connect(self.apply_item_filter)
        self.filter_line_edit.setAlignment(Qt.AlignLeft)
        self.content_layout.addWidget(self.filter_line_edit)

        left_frame = QFrame()
        self.left_layout = QGridLayout()
        left_frame.setLayout(self.left_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(left_frame)
        
        asyncio.create_task(self.fetch_consumivel())

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        self.drop_zone = DropZone(self)
        shopping_cart_label = DropLabel(self.drop_zone)

        right_layout.addWidget(shopping_cart_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.drop_zone)
        right_layout.addWidget(self.drop_zone.delete_button, alignment=Qt.AlignCenter)

        horizontal_content_layout = QHBoxLayout()
        horizontal_content_layout.addWidget(left_scroll_area)
        horizontal_content_layout.addWidget(right_frame)

        self.content_layout.addLayout(horizontal_content_layout)

        self.sector_input = QComboBox()
        self.sector_input.setFixedSize(400, 40)
        self.sector_input.setStyleSheet(Style.style_QComboBox)
        self.sector_urgent_layout = QHBoxLayout()
        self.sector_urgent_layout.setAlignment(Qt.AlignCenter)
        self.sector_urgent_layout.addWidget(self.sector_input)
        self.sector_urgent_layout.addSpacing(20)
        asyncio.create_task(self.update_sectors())
        
        
    async def requerimentoInterno_page(self):
        if self.user.role_nome == "Enfermeiro" or self.user.role_nome == "Médico":
            self.urgent_input = QCheckBox("Urgente")
            self.urgent_input.setChecked(False)
            self.urgent_input.setStyleSheet(Style.style_checkbox)
            self.sector_urgent_layout.addWidget(self.urgent_input)
            
        self.content_layout.addLayout(self.sector_urgent_layout)
        create_button = QPushButton("Criar Requerimento")
        create_button.setFixedSize(500, 40)
        create_button.setStyleSheet(Style.style_bt_QPushButton)
        if self.user.role_nome == "Enfermeiro" or self.user.role_nome == "Médico":
            create_button.clicked.connect(lambda: self.create_requerimento(user_id_pedido=self.user.utilizador_id, urgent=self.urgent_input.isChecked(), drop_zone=self.drop_zone))
        else:
            create_button.clicked.connect(lambda: self.create_requerimento(user_id_pedido=self.user.utilizador_id, urgent=False, drop_zone=self.drop_zone))
        self.content_layout.addWidget(create_button, alignment=Qt.AlignCenter)
        self.create_page_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.create_page_layout)
        
    async def requerimentoExterno_page(self, requerimento: Requerimento):
        self.content_layout.addLayout(self.sector_urgent_layout)
        create_button = QPushButton("Associar Consumiveis")
        create_button.setFixedSize(500, 40)
        create_button.setStyleSheet(Style.style_bt_QPushButton)
        create_button.clicked.connect(lambda: self.update_requerimento_externo(requerimento_id=requerimento.requerimento_id, setor_id=self.sector_input.currentData(), drop_zone=self.drop_zone))
        self.content_layout.addWidget(create_button, alignment=Qt.AlignCenter)
        self.create_page_layout.addLayout(self.content_layout)
        self.main_layout.addLayout(self.create_page_layout)

    async def fetch_consumivel(self):
        response = await API_GetConsumiveis()
        if response.success:
            self.all_consumivel = response.data 
            self.update_item_display(self.all_consumivel)
        else:
            Overlay.show_error(self, response.error_message)

    def apply_item_filter(self):
        filter_text = self.filter_line_edit.text().lower()
        filtered_consumivel = [
            item for item in self.all_consumivel if filter_text in item.nome_consumivel.lower()
        ]
        self.update_item_display(filtered_consumivel)
        
    def update_item_display(self, consumivel):
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        row, col = 0, 0
        for item in consumivel:
            
            item_label = DraggableLabel(
                consumivel_id=item.consumivel_id,
                nome_consumivel=item.nome_consumivel,
                tipo_consumivel=item.nome_tipo,
            )
            self.left_layout.addWidget(item_label, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def create_requerimento(self, user_id_pedido,urgent, drop_zone):
        requerimento_consumivel = []
        for row in range(drop_zone.rowCount()):
            item_widget = drop_zone.item(row, 0)
            consumivel_data = item_widget.data(Qt.UserRole)
            data_parts = consumivel_data.split("|")
            id ,nome_consumivel = data_parts
            item_id= int(id) if id.isdigit() else None
            quantidade = drop_zone.cellWidget(row, 1).value()
            requerimento_consumivel.append({"consumivel_id": item_id, "quantidade": quantidade})

        setor_id = self.sector_input.currentData()
        
        if urgent:
            urgent = True
        else:
            urgent = False
            
        response = API_CreateRequerimento(user_id_pedido, setor_id,urgent, requerimento_consumivel)
        
        if response.success:
            self.reload_page_requerimentos()
            Overlay.show_success(self, "Requerimento criado com sucesso!")
        else:
            Overlay.show_error(self, response.error_message)

    def update_requerimento_externo(self, requerimento_id, setor_id, drop_zone):
        requerimento_consumivel = []
        for row in range(drop_zone.rowCount()):
            item_widget = drop_zone.item(row, 0)
            item_data = item_widget.data(Qt.UserRole)
            item_parts = item_data.split("|")
            item_id = int(item_parts[0])
            quantidade = drop_zone.cellWidget(row, 1).value()
            requerimento_consumivel.append({
                "consumivel_id": item_id,
                "quantidade": quantidade
            })

        setor_id = self.sector_input.currentData()
        
        response = API_UpdateRequerimentoExterno(requerimento_id, setor_id, requerimento_consumivel, self.user.utilizador_id)
        if response.success:
            self.reload_page_requerimentos()
            Overlay.show_success(self, "Requerimento Externo Atualizado com sucesso!")
        else:
            Overlay.show_error(self, response.error_message)

    async def load_requerimentos(self, user: Utilizador):
        if user.role_nome == "Gestor Responsável":
            response = await API_GetRequerimentosByResponsavel(user.utilizador_id)
        elif user.role_nome == "Farmacêutico":
            response = await API_GetRequerimentosByFarmaceutico()
        else:
            response = await API_GetRequerimentosByUser(user.utilizador_id)
            
        if not response.success:
            Overlay.show_error(self, response.error_message)
            return

        if(user.role_nome == "Farmacêutico"):
            new_requerimentos = sorted(
                response.data,
                key=lambda x: (not x.urgente, x.requerimento_id),
                reverse=False)
        else:
            new_requerimentos = sorted(response.data, key=lambda x: x.requerimento_id, reverse=True)
        
        new_requerimentos_dict = {req.requerimento_id: req for req in new_requerimentos}
        
        self.ui_updated = False
        updated_ids = set()
        for requerimento_id, requerimento in new_requerimentos_dict.items():
            if requerimento_id not in self.current_requerimentos_dict:
                self.add_requerimento_card(requerimento)
                self.ui_updated = True
            elif requerimento != self.current_requerimentos_dict[requerimento_id]:
                self.remove_requerimento_card(requerimento_id)
                self.add_requerimento_card(requerimento)
                self.ui_updated = True
            updated_ids.add(requerimento_id)

        for requerimento_id in list(self.current_requerimentos_dict.keys()):
            if requerimento_id not in updated_ids:
                self.remove_requerimento_card(requerimento_id)
                ui_updated = True

        self.current_requerimentos_dict = new_requerimentos_dict.copy()

        self.current_requerimentos = new_requerimentos

        self.apply_filter(self.current_filter)
        
        if self.setup_page:
            self.setup_page=False
            self.ui_updated = False
        else:
            if ui_updated:
                Overlay.show_information(self, "Requerimentos atualizados!")

    def add_requerimento_card(self, requerimento):
        card = RequerimentoCard(user=self.user, requerimento=requerimento, consumivel_manager=self.consumivel_manager, 
                                update_callback=self.reload_requerimentos,page_stock=self.page_stock, parent_page=self)
        self.scroll_layout.addWidget(card)
        self.current_requerimentos_dict[requerimento.requerimento_id] = requerimento

    def remove_requerimento_card(self, requerimento_id):
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, RequerimentoCard) and widget.requerimento.requerimento_id == requerimento_id:
                widget.deleteLater()
                break
        self.current_requerimentos_dict.pop(requerimento_id, None)

    def reload_page_requerimentos(self):
        self.clear_layout(self.main_layout)
        self.setup_RequerimentoPage()
        self.load_requerimentos_wrapper()
        
    def reload_requerimentos(self):
        self.load_requerimentos_wrapper()

    async def update_sectors(self):
        response = await API_GetSectors()
        if response.success:
            asyncio.create_task(self.create_sectors(response.data))
        else:
            Overlay.show_error(self, response.error_message)

    def create_sectors(self, sectors):
        self.sector_input.clear()
        self.sector_input.addItem("Selecionar Setor", None)
        for sector in sectors:
            self.sector_input.addItem(f"{sector.nome_setor} - {sector.localizacao}", sector.setor_id)

    def load_requerimentos_wrapper(self):
        asyncio.create_task(self.load_requerimentos(self.user))
    
    def update_sectors_wrapper(self):
        asyncio.create_task(self.update_sectors())
    
    def show_create_requerimento_interno_page_wrapper(self):
        asyncio.create_task(self.show_create_requerimento_page())
        asyncio.create_task(self.requerimentoInterno_page())
    
    def show_create_requerimento_externo_page_wrapper(self, requerimento: Requerimento):
        asyncio.create_task(self.show_create_requerimento_page())
        asyncio.create_task(self.requerimentoExterno_page(requerimento=requerimento))
        
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

                
    def apply_filter(self, filter_key):
        
        if self.current_filter != filter_key or self.setup_page or  self.ui_updated:
            selected_button = self.filter_buttons.get(filter_key)
            if selected_button:
                self.set_filter_selected(selected_button)

            self.current_filter = filter_key

            #TODO COLOCAR ISTO OK PARA SO VER OS REQUERIMENTOS URGENTES
            # if self.user.role_nome == "Farmacêutico":
            #     requerimentos_urgentes = [
            #         req for req in self.current_requerimentos if req.urgente and req.status_atual in (1, 3,11)
            #     ]
            #     if requerimentos_urgentes:
            #         Overlay.show_warning(
            #             self, 
            #             "Há requerimentos urgentes pendentes. Responda-os antes de continuar com outros requerimentos."
            #         )
            #         filtered_requerimentos = requerimentos_urgentes
            #     else:
            #         filtered_requerimentos = self.get_filtered_requerimentos(filter_key)
            # else:
            filtered_requerimentos = self.get_filtered_requerimentos(filter_key)
            
            self.clear_layout(self.scroll_layout)
            for requerimento in filtered_requerimentos:
                self.add_requerimento_card(requerimento)
        else:
            return

    def get_filtered_requerimentos(self, filter_key):
        if filter_key == "Todos":
            return self.current_requerimentos
        elif filter_key == "Pendentes de Resposta":
            if self.user.role_nome == "Gestor Responsável":
                return [req for req in self.current_requerimentos if req.status_atual == 0]
            elif self.user.role_nome == "Farmacêutico":
                return [
                    req for req in self.current_requerimentos 
                    if req.status_atual in (1, 6, 3, 10, 11)
                ]
            else:
                return [
                    req for req in self.current_requerimentos if req.status_atual == 8
                ]
        elif filter_key == "Urgente":
            return [req for req in self.current_requerimentos if req.urgente]
        elif filter_key.startswith("Status_"):
            status = int(filter_key.split("_")[1])
            if status == 1:
                requerimentos_filtrados = [req for req in self.current_requerimentos if req.status_atual == 1 or req.status_atual == 10]
                return requerimentos_filtrados
            else:
                return [req for req in self.current_requerimentos if req.status_atual == status]
        elif filter_key == "Externo":
            return [req for req in self.current_requerimentos if req.tipo_requerimento == "Externo"]
        else:
            return self.current_requerimentos

    def set_filter_selected(self, selected_button):
        for button in self.filter_buttons.values():
            button.setStyleSheet(Style.style_bt_QPushButton_Filter)
        selected_button.setStyleSheet(Style.style_bt_QPushButton_Filter_Selected)



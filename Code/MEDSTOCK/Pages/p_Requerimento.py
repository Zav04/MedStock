from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QComboBox, QCheckBox,QSizePolicy,QLineEdit
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from APP.UI.ui_styles import Style
from APP.Overlays.Overlay import Overlay
from Class.Utilizador import Utilizador
from API.API_GET_Request import (API_GetRequerimentosByUser, API_GetRequerimentosByResponsavel,
                                API_GetSectors, API_GetConsumiveis, API_GetRequerimentosByFarmaceutico)
from API.API_POST_Request import API_CreateRequerimento
from APP.Card.Card import RequerimentoCard
from APP.UI.ui_functions import UIFunctions
from Pages.Requerimento.ui_DragAndDrop_Itens import DraggableLabel, DropZone, DropLabel
import asyncio


class RequerimentoPage(QWidget):
    def __init__(self, user: Utilizador):
        super().__init__()
        self.user = user
        self.main_layout = QVBoxLayout(self)
        self.current_requerimentos = []
        self.ui_updated = False
        self.current_filter = None
        self.current_requerimentos_dict = {}
        self.setup_RequerimentoPage()
        QTimer.singleShot(0, self.load_requerimentos_wrapper)
        
        
        # self.update_timer = QTimer(self)
        # self.update_timer.timeout.connect(self.load_requerimentos_wrapper)
        # self.update_timer.start(60000)

    def setup_RequerimentoPage(self):
        self.setup_page=True
        title_layout = QHBoxLayout()
        self.title = QLabel("REQUERIMENTOS")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setStyleSheet("color: #C0C0C0; font-weight: bold;")
        title_layout.addWidget(self.title, alignment=Qt.AlignLeft)

        self.create_button = QPushButton("CRIAR NOVO REQUERIMENTO")
        self.create_button.setFixedSize(400, 40)
        self.create_button.setStyleSheet(Style.style_bt_QPushButton)
        self.create_button.clicked.connect(self.show_create_requerimento_page_wrapper)
        title_layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        #TODO ADMIN NOT SEE THIS BUTTON
        if self.user.role_nome == "Gestor Responsável" or self.user.role_nome == "Farmacêutico":
            self.create_button.hide()

        self.main_layout.addLayout(title_layout)
        self.main_layout.addSpacing(50)
        
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)


        self.filter_buttons = {}
        if self.user.role_nome == "Gestor Responsável":
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
        elif self.user.role_nome == "Farmacêutico":
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
            ]
        else:
            filter_buttons = [
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
            
        if self.user.role_nome == "Gestor Responsável" or self.user.role_nome == "Farmacêutico":
            self.current_filter = "Pendentes de Resposta"
        else:
            self.current_filter= "Todos"

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
        create_page_layout = QVBoxLayout()

        back_button = QPushButton()
        back_button.setFixedSize(100, 40)
        back_button.setIcon(QIcon(UIFunctions.recolor_icon("./icons/MaterialIcons/arrow_back.png", "#b5c6bf")))
        back_button.setStyleSheet(Style.style_bt_QPushButton)
        back_button.clicked.connect(self.reload_page_requerimentos)
        back_button.setText("Voltar")
        back_button.setIconSize(QSize(20, 20))
        create_page_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        content_layout = QVBoxLayout()
        
        create_page_layout.setSpacing(20)
        self.filter_line_edit = QLineEdit()
        self.filter_line_edit.setPlaceholderText("Digite para filtrar os itens...")
        self.filter_line_edit.setFixedHeight(30)
        self.filter_line_edit.setFixedWidth(650)
        self.filter_line_edit.setStyleSheet(Style.style_QlineEdit)
        self.filter_line_edit.textChanged.connect(self.apply_item_filter)
        self.filter_line_edit.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(self.filter_line_edit)

        left_frame = QFrame()
        self.left_layout = QGridLayout()
        left_frame.setLayout(self.left_layout)

        left_scroll_area = QScrollArea()
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(left_frame)

        try:
            asyncio.create_task(self.fetch_consumivel())
        except Exception as e:
            print(e)
        ##asyncio.create_task(self.fetch_consumivel(self.left_layout))

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        drop_zone = DropZone(self)
        shopping_cart_label = DropLabel(drop_zone)

        right_layout.addWidget(shopping_cart_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(drop_zone)
        right_layout.addWidget(drop_zone.delete_button, alignment=Qt.AlignCenter)

        horizontal_content_layout = QHBoxLayout()
        horizontal_content_layout.addWidget(left_scroll_area)
        horizontal_content_layout.addWidget(right_frame)

        content_layout.addLayout(horizontal_content_layout)

        self.sector_input = QComboBox()
        self.sector_input.setFixedSize(400, 40)
        self.sector_input.setStyleSheet(Style.style_QComboBox)
        
        if self.user.role_nome == "Enfermeiro" or self.user.role_nome == "Médico":
            sector_urgent_layout = QHBoxLayout()
            sector_urgent_layout.setAlignment(Qt.AlignCenter)
            self.urgent_input = QCheckBox("Urgente")
            self.urgent_input.setChecked(False)
            self.urgent_input.setStyleSheet(Style.style_checkbox)
            sector_urgent_layout.addWidget(self.sector_input)
            sector_urgent_layout.addSpacing(20)
            sector_urgent_layout.addWidget(self.urgent_input)
            content_layout.addLayout(sector_urgent_layout)

        asyncio.create_task(self.update_sectors())

        create_button = QPushButton("Criar Requerimento")
        create_button.setFixedSize(500, 40)
        create_button.setStyleSheet(Style.style_bt_QPushButton)
        create_button.clicked.connect(lambda: self.create_requerimento(user_id_pedido=self.user.utilizador_id, urgent=self.urgent_input.isChecked(), drop_zone=drop_zone))

        content_layout.addWidget(create_button, alignment=Qt.AlignCenter)

        create_page_layout.addLayout(content_layout)

        self.main_layout.addLayout(create_page_layout)

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
                #TODO VERIFICAR COMO VAI FICAR COM TIVER ALGORITMO DE ALOCAÇÃO E GESTÃO DE STOCK
                quantidade_disponivel=item.quantidade_total
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
            item_id = int(item_widget.data(Qt.UserRole))
            quantidade = drop_zone.cellWidget(row, 1).value()
            requerimento_consumivel.append({"consumivel_id": item_id, "quantidade": quantidade})

        setor_id = self.sector_input.currentData()
        
        if urgent:
            urgent = True
        else:
            urgent = False

        response = API_CreateRequerimento(user_id_pedido, setor_id,urgent, requerimento_consumivel)
        if response.success:
            
            #TODO ANTES DE CRIAR TENHO FAZER A GESTÃO PARA VER O QUE SE PODE ALOCAR OS CONSUMIVEIS
            self.reload_page_requerimentos()
            Overlay.show_success(self, "Requerimento criado com sucesso!")
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
        card = RequerimentoCard(user=self.user, requerimento=requerimento, update_callback=self.reload_requerimentos)
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
            QTimer.singleShot(0, lambda: self.create_sectors(response.data))
        else:
            Overlay.show_error(self, response.error_message)

    def create_sectors(self, sectors):
        self.sector_input.clear()
        self.sector_input.addItem("Selecionar Setor", None)
        for sector in sectors:
            self.sector_input.addItem(f"{sector.nome_setor} - {sector.localizacao}", sector.setor_id)

    def load_requerimentos_wrapper(self):
        asyncio.ensure_future(self.load_requerimentos(self.user))
    
    def update_sectors_wrapper(self):
        asyncio.ensure_future(self.update_sectors())
    
    def show_create_requerimento_page_wrapper(self):
        asyncio.ensure_future(self.show_create_requerimento_page())
        
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

            if self.user.role_nome == "Farmacêutico":
                requerimentos_urgentes = [
                    req for req in self.current_requerimentos if req.urgente and req.status in (1, 3)
                ]
                if requerimentos_urgentes:
                    Overlay.show_warning(
                        self, 
                        "Há requerimentos urgentes pendentes. Responda-os antes de continuar com outros requerimentos."
                    )
                    filtered_requerimentos = requerimentos_urgentes
                else:
                    filtered_requerimentos = self.get_filtered_requerimentos(filter_key)
            else:
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
                return [req for req in self.current_requerimentos if req.status == 0]
            else:
                return [
                    req for req in self.current_requerimentos 
                    if req.status in (1, 6, 3)
                ]
        elif filter_key == "Urgente":
            return [req for req in self.current_requerimentos if req.urgente]
        elif filter_key.startswith("Status_"):
            status = int(filter_key.split("_")[1])
            return [req for req in self.current_requerimentos if req.status == status]
        else:
            return self.current_requerimentos

    def set_filter_selected(self, selected_button):
        for button in self.filter_buttons.values():
            button.setStyleSheet(Style.style_bt_QPushButton_Filter)
        selected_button.setStyleSheet(Style.style_bt_QPushButton_Filter_Selected)



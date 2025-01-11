from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QTimer
from APP.UI.ui_styles import Style
from API.API_GET_Request import API_GetSectors, API_GetAllUsers, API_GetUtilizadoresComSetores
from API.API_PUT_Request import API_AssociateUserToSector
from APP.Overlays.Overlay import Overlay
import asyncio


class AssociateUserToSectorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.sectors = []
        self.users = []
        self.allocations = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 30, 20, 30)

        self.title = QLabel("ASSOCIAR UTILIZADOR A SETOR")
        self.title_font = QFont("Arial", 24, QFont.Bold)
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(15)

        self.font_Label = QFont("Arial", 12)

        self.sector_label = QLabel("Setor")
        self.sector_label.setFont(self.font_Label)
        self.sector_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.sector_input = QComboBox()
        self.sector_input.setFixedSize(500, 40)
        self.sector_input.setStyleSheet(Style.style_QComboBox)

        self.user_label = QLabel("Utilizador")
        self.user_label.setFont(self.font_Label)
        self.user_label.setStyleSheet("color: #C0C0C0;font-weight: bold;")
        self.user_input = QComboBox()
        self.user_input.setFixedSize(500, 40)
        self.user_input.setStyleSheet(Style.style_QComboBox)

        self.associate_button = QPushButton("Associar")
        self.associate_button.setFixedSize(150, 40)
        self.associate_button.setStyleSheet(Style.style_bt_QPushButton)
        self.associate_button.clicked.connect(self.associate_user_to_sector)

        self.main_layout.addWidget(self.sector_label,alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.sector_input,alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.user_label,alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.user_input,alignment=Qt.AlignCenter)
        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.associate_button, alignment=Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Utilizador", "Setor"])
        self.table.setFont(QFont("Arial", 11))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(Style.style_Table)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection) 
        self.main_layout.addWidget(self.table)

        self.update_data_thread = QTimer(self)
        self.update_data_thread.timeout.connect(self.update_data)
        self.update_data_thread.start(60000)
        
        self.update_data()
        self.setLayout(self.main_layout)

    async def fetch_data(self):
        users_response = await API_GetAllUsers()
        sectors_response = await API_GetSectors()
        allocations_response = await API_GetUtilizadoresComSetores()

        return users_response, sectors_response, allocations_response

    def update_data(self):
        asyncio.create_task(self.refresh_data())

    async def refresh_data(self):
        users_response, sectors_response, allocations_response = await self.fetch_data()


        if allocations_response.success:
            self.update_allocations(allocations_response.data)
        else:
            Overlay.show_error(self, allocations_response.error_message)
        if users_response.success:
            self.update_users(users_response.data)
        else:
            Overlay.show_error(self, users_response.error_message)
        if sectors_response.success:
            self.update_sectors(sectors_response.data)
        else:
            Overlay.show_error(self, sectors_response.error_message)

    def update_users(self, users):
        allocated_user_ids = {allocation.utilizador_id for allocation in self.allocations}
        unallocated_users = [user for user in users if user.utilizador_id not in allocated_user_ids]

        if unallocated_users != self.users:
            self.users = unallocated_users
            self.user_input.clear()
            self.user_input.addItem("Selecione o Utilizador", None)
            for user in unallocated_users:
                self.user_input.addItem(user.nome, user.utilizador_id)

    def update_sectors(self, sectors):
        allocated_sectors = {(allocation.nome_setor, allocation.localizacao) for allocation in self.allocations}
        
        unallocated_sectors = [
            sector for sector in sectors 
            if (sector.nome_setor, sector.localizacao) not in allocated_sectors
        ]

        if unallocated_sectors != self.sectors:
            self.sectors = unallocated_sectors
            self.sector_input.clear()
            self.sector_input.addItem("Selecione o Setor", None)
            for sector in unallocated_sectors:
                self.sector_input.addItem(f"{sector.nome_setor} - {sector.localizacao}", sector.setor_id)

    def update_allocations(self, allocations):
        if allocations != self.allocations:
            self.allocations = allocations
            self.table.setRowCount(len(allocations))
            for row, allocation in enumerate(allocations):
                self.table.setItem(row, 0, QTableWidgetItem(allocation.nome))
                self.table.setItem(row, 1, QTableWidgetItem(f"{allocation.nome_setor} - {allocation.localizacao}"))


    def associate_user_to_sector(self):
        user_id = self.user_input.currentData()
        sector_id = self.sector_input.currentData()
        asyncio.create_task(self.perform_association(user_id, sector_id))

    async def perform_association(self, user_id, sector_id):
        response = await API_AssociateUserToSector(user_id, sector_id)
        if response.success:
            self.sector_input.setCurrentIndex(0)
            self.user_input.setCurrentIndex(0)
            Overlay.show_success(self, response.data)
            self.update_data()
        else:
            Overlay.show_error(self, response.error_message)

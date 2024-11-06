
from Custom_Widgets.QCustomModals import QCustomModals
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor,QIcon,QPixmap
from APP.ui_styles import Style

class Overlay:
    @staticmethod
    def show_success(parent, message):
        Overlay._show_modal("Successo", parent, message)

    @staticmethod
    def show_information(parent, message):
        Overlay._show_modal("Informação", parent, message)

    @staticmethod
    def show_warning(parent, message):
        Overlay._show_modal("Aviso", parent, message)

    @staticmethod
    def show_error(parent, message):
        Overlay._show_modal("Erro", parent, message)

    @staticmethod
    def _show_modal(modal_type, parent, message):

        kwargs = {
            "title": f"{modal_type}",
            "description": message,
            "position": "top-right",
            "parent": parent,
            "animationDuration": 5000
        }
        

        if modal_type == "Informação":
            modal = QCustomModals.InformationModal(**kwargs)
            modal.setStyleSheet(Style.style_InformationModal)
        elif modal_type == "Successo":
            modal = QCustomModals.SuccessModal(**kwargs)
            modal.setStyleSheet(Style.style_SuccessModal)
        elif modal_type == "Aviso":
            modal = QCustomModals.WarningModal(**kwargs)
            modal.setStyleSheet(Style.style_WarningModal)
        elif modal_type == "Erro":
            modal = QCustomModals.ErrorModal(**kwargs)
            modal.setStyleSheet(Style.style_ErrorModal)
        else:
            return
        
        

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(0, 0, 0, 150)) 
        shadow_effect.setOffset(0, 0)
        modal.setGraphicsEffect(shadow_effect)
        modal.show()
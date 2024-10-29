
from PySide2.QtWidgets import QGraphicsDropShadowEffect
from Custom_Widgets.QCustomModals import QCustomModals
from PySide2.QtGui import QColor

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
            "animationDuration": 3000
        }

        if modal_type == "Informação":
            modal = QCustomModals.InformationModal(**kwargs)
        elif modal_type == "Successo":
            modal = QCustomModals.SuccessModal(**kwargs)
        elif modal_type == "Aviso":
            modal = QCustomModals.WarningModal(**kwargs)
        elif modal_type == "Erro":
            modal = QCustomModals.ErrorModal(**kwargs)
        else:
            return


        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(0, 0, 0, 150)) 
        shadow_effect.setOffset(0, 0)
        modal.setGraphicsEffect(shadow_effect)

        modal.show()
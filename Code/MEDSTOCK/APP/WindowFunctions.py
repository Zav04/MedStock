# WindowFunctions.py
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from APP.ui_functions import UIFunctions

class WindowFunctions:
    @staticmethod
    def setupWindow(self,title, icon_path):
        """Set window title and icon."""
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_path))
        UIFunctions.labelTitle(self, 'MedStock')
        UIFunctions.uiDefinitions(self)

    @staticmethod
    def removeTitleBar(window, status=True):
        """Remove the standard title bar."""
        window.setWindowFlag(Qt.FramelessWindowHint, status)
        window.setAttribute(Qt.WA_TranslucentBackground, status)

    @staticmethod
    def enableWindowDragging(window):
        """Enable window dragging by attaching mouse events."""
        window.dragPos = None

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                window.move(window.pos() + event.globalPos() - window.dragPos)
                window.dragPos = event.globalPos()
                event.accept()

        def handleMousePress(event):
            window.dragPos = event.globalPos()

        # Assign the event functions directly
        window.mouseMoveEvent = moveWindow
        window.mousePressEvent = handleMousePress

    @staticmethod
    def maximizeRestoreWindow(window, maximized):
        """Maximize or restore the window."""
        if maximized:
            window.showMaximized()
        else:
            window.showNormal()

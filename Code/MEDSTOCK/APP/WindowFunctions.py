# WindowFunctions.py
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from APP.Ui_Functions import UIFunctions

class WindowFunctions:
    @staticmethod
    def setupWindow(self, title, icon_path):
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
    def enableWindowDragging(window, title_bar_frame=None):
        """Enable window dragging by attaching mouse events to a specific frame."""
        window.dragPos = None

        # Define the mouse event functions for moving the window
        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                window.move(window.pos() + event.globalPos() - window.dragPos)
                window.dragPos = event.globalPos()
                event.accept()

        def handleMousePress(event):
            window.dragPos = event.globalPos()

        # Assign the event functions only to the specified title bar frame
        if title_bar_frame:
            title_bar_frame.mouseMoveEvent = moveWindow
            title_bar_frame.mousePressEvent = handleMousePress
        else:
            # Fall back to attaching the events directly to the window if no frame is specified
            window.mouseMoveEvent = moveWindow
            window.mousePressEvent = handleMousePress

    @staticmethod
    def maximizeRestoreWindow(window, maximized):
        """Maximize or restore the window."""
        if maximized:
            window.showMaximized()
        else:
            window.showNormal()

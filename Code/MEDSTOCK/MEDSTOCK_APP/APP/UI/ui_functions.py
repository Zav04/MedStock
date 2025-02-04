from APP.UI.ui_styles import Style
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import (QPropertyAnimation,QSize,Qt)
from PyQt5.QtGui import (QColor,QFont,QPixmap,QIcon)
from PyQt5.QtWidgets import *
import tempfile
import os


GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

count = 1

class UIFunctions(QMainWindow):

    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/20x20/icons/20x20/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/20x20/icons/20x20/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    def returStatus():
        return GLOBAL_STATE


    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status


    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()


    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)


    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_menu.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect
    
    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_right.setText(newText)

    @staticmethod
    def selectStandardMenu(main_window, widget, label_function):
        for w in main_window.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))
                label_function(main_window,w.text())
                

    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    def userIcon(self, initialsTooltip):
        self.ui.label_user_icon.setText(initialsTooltip)
        style = self.ui.label_user_icon.styleSheet()
        style += "QLabel { font-size: 20px; font-weight: bold; }\n"
        self.ui.label_user_icon.setStyleSheet(style)


    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        self.ui.btn_close.clicked.connect(lambda: self.close())

    def recolor_icon(path, color):
        pixmap = QPixmap(path)
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(QColor(color))
        colored_pixmap.setMask(pixmap.mask())
        
        temp_dir = tempfile.gettempdir()
        temp_icon_path = os.path.join(temp_dir, f"recolor_{os.path.basename(path)}")
        colored_pixmap.save(temp_icon_path, "PNG")
        
        return temp_icon_path
    
    
    @staticmethod
    def center_column_content(column, table_widget):
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, column)
            if item:
                item.setTextAlignment(Qt.AlignCenter)

    @staticmethod
    def adjust_column_sizes(table_widget: QTableWidget):
        table_widget.resizeColumnsToContents()
        header = table_widget.horizontalHeader()

        for column in range(table_widget.columnCount()):
            header_text = table_widget.horizontalHeaderItem(column).text()
            content_width = header.sectionSize(column)
            header_width = table_widget.fontMetrics().boundingRect(header_text).width() + 20
            optimal_width = max(content_width, header_width)
            
            if column >= table_widget.columnCount() - 5:
                header.setSectionResizeMode(column, QHeaderView.Stretch)
                UIFunctions.center_column_content(column, table_widget)
            else:
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                header.resizeSection(column, optimal_width)

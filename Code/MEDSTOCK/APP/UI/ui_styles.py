

class Style():
    

    style_bt_menu = (
    """
    QPushButton {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid #b5c6bf;
        background-color: #b5c6bf;
        text-align: left;
        padding-left: 45px;
        font-size: 16px;
        font-weight: bold;
        color: #dbd7d7;
    }
    QPushButton:hover {
        background-color: #81C784;
        border-left: 28px solid #81C784;
        border-right: none;
        color: #dbd7d7;
    }
    QPushButton:pressed {
        background-color: #4CAF50;
        border-left: 28px solid #4CAF50;
        border-right: none;
        color: #dbd7d7;
    }
    """
    )
    
    style_QlineEdit = ("""
            QLineEdit {
                background-color: rgb(255, 255, 255);
                border-radius: 5px;
                border: 2px solid #b5c6bf;
                padding-left: 10px;
                color: rgb(0, 0, 0);
                font: 16pt "Arial";
                padding-right: 30px;
            }
            QLineEdit:hover {
                border: 2px solid #81C784;
            }
            QLineEdit:focus {
                border: 4px solid #4CAF50;
            }
        """)
    
    style_bt_QPushButton = (
    """
    QPushButton {
        background-position: left center;
        background-repeat: no-repeat;
        border: 2px solid #b5c6bf;
        border-left: none;
        border-right: none;
        background-color: #b5c6bf;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: rgb(255,255,255);
    }
    QPushButton:hover {
        background-color: #81C784;
        border-left: none;
        border-right: none;
        color: rgb(255,255,255);
    }
    QPushButton:pressed {
        background-color: #4CAF50;
        border-left: none;
        border-right: none;
        color: rgb(255,255,255);
    }
    """
    )
    
    style_QComboBox = (
        """
        QComboBox {
            background-color: rgb(255, 255, 255);
            border-radius: 5px;
            border: 2px solid #b5c6bf;
            padding-left: 10px;
            color: rgb(0, 0, 0);
            font: 16pt "Arial";
        }
        QComboBox:hover {
            border: 2px solid #81C784;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 3px;
            border-left-color: rgb(255, 255, 255);
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background-image: url(:/20x20/icons/20x20/cil-arrow-bottom.png);
            background-position: center;
            background-repeat: no-repeat;
        }
        QComboBox QAbstractItemView {
            border: 2px solid #81C784;
            background-color: rgb(255, 255, 255);
            selection-background-color: #81C784;
            selection-color: rgb(255, 255, 255);
            padding: 5px;
            font: 14pt "Arial";
            outline: 0;
        }
        QComboBox QAbstractItemView:hover {
            border: 2px solid #81C784;
        }
        """
    )
    
    style_QDateEdit = (
    """
    QDateEdit {
        background-color: rgb(255, 255, 255);
        border-radius: 5px;
        border: 2px solid #b5c6bf;
        padding-left: 10px;
        color: rgb(0, 0, 0);
        font: 16pt "Arial";
    }
    QDateEdit:hover {
        border: 2px solid #81C784;
    }
    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left-width: 3px;
        border-left-color: rgb(255, 255, 255);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QDateEdit::down-arrow {
        image: url(:/icons/MaterialIcons/calendar_month.png);
        width: 16px;
        height: 16px;
    }
    QCalendarWidget QWidget {
        alternate-background-color: #f4f4f4;
        font-size: 10pt;
    }
    QCalendarWidget QAbstractItemView:enabled {
        font-size: 10pt;
        color: rgb(0, 0, 0);
        background-color: rgb(255, 255, 255);
        selection-background-color: #81C784;
        selection-color: rgb(255, 255, 255);
    }
    QCalendarWidget QToolButton {
        height: 40px;
        width: 80px;
        font-size: 10pt;
        color: rgb(0, 0, 0);
        background-color: #e6e6e6;
        border: none;
        margin: 5px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: #81C784;
        color: rgb(255, 255, 255);
    }
    """
    )


    style_bt_TextEdit = ("""
    QPushButton {
        background: none;
        border: none;
        color: #b5c6bf;
        font-size: 14px;
        text-decoration: underline;
    }
    QPushButton:hover {
        color: #81C784;
    }
    QPushButton:pressed {
        color: #4CAF50;
    }
""")
    
    style_Table = ("""
            QTableWidget {
                gridline-color: #dddddd;
                background-color: transparent;
                border: none;
                text-align: center;
            }
            
            QTableWidget::item {
                padding-left: 5px;
                padding-right: 5px;
                border-bottom: 3px solid #b5c6bf;
                color: rgb(0, 0, 0);
                text-align: center;
            }
            
            QTableWidget::item:selected {
                background-color: #b5c6bf;
                color: #333;
            }
            
            QHeaderView::section {
                background-color: #b5c6bf;
                color: #333;
                padding: 4px;
                font-weight: bold;
                font-size: 20px;
                border: 1px solid #d0d0d0;
            }
        QScrollBar:vertical, QScrollBar:horizontal {
            border: none;
            background: #757575;
            width: 14px;
            margin: 21px 0 21px 0;
            border-radius: 0px;
        }
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #b5c6bf;
            min-height: 25px;
            border-radius: 7px;
        }
        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-top-left-radius: 7px;
            border-top-right-radius: 7px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """)
    
    style_Table_Requerimento = ("""
        QTableWidget {
            gridline-color: #dddddd;
            background-color: transparent;
            border: none;
            text-align: center;
        }

        QTableWidget::item {
            padding-left: 5px;
            padding-right: 5px;
            color: rgb(0, 0, 0);
            text-align: center;
        }
        QTableWidget::item:selected {
            background-color: #b5c6bf;
            color: #333;
        }
        QHeaderView::section {
            background-color: #b5c6bf;
            color: #333;
            padding: 4px;
            font-weight: bold;
            font-size: 20px;
            border: 1px solid #d0d0d0;
        }
        
        QScrollBar:vertical, QScrollBar:horizontal {
            border: none;
            background: #757575;
            width: 14px;
            margin: 21px 0 21px 0;
            border-radius: 0px;
        }
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #b5c6bf;
            min-height: 25px;
            border-radius: 7px;
        }
        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-top-left-radius: 7px;
            border-top-right-radius: 7px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
    """)
    
    style_ScrollBar = ("""
            QScrollArea {
                border: none;
                background: transparent;
            }        
        QScrollBar:vertical, QScrollBar:horizontal {
            border: none;
            background: #757575;
            width: 14px;
            margin: 21px 0 21px 0;
            border-radius: 0px;
        }
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #b5c6bf;
            min-height: 25px;
            border-radius: 7px;
        }
        QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {
            border: none;
            background: #757575;
            height: 20px;
            border-top-left-radius: 7px;
            border-top-right-radius: 7px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """)


    style_InformationModal = ("""
    InformationModal {
        border-radius: 10px;
        border: 2px solid ;
        border-color: #2799be;
        background-color: #2799be;
        }
        QPushButton#closeButton {
            border: none;
            outline: none;
            text-decoration: none;
            background-color: transparent;
        }
        QLabel#titlelabel{
            font-size: 12px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#bodyLabel{
            font-size: 11px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#iconlabel {
            min-width: 20px;
            min-height: 20px;
            max-width: 20px;
            max-height: 20px;
            margin-right: 12px;
        }""")


    style_SuccessModal = ("""
    SuccessModal {
        border-radius: 5px;
        border: 2px solid ;
        border-color: #29b328;
        background-color: #29b328;
        }
        QPushButton#closeButton {
            border: none;
            outline: none;
            text-decoration: none;
            background-color: transparent;
        }
        QLabel#titlelabel{
            font-size: 12px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#bodyLabel{
            font-size: 11px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#iconlabel {
            min-width: 20px;
            min-height: 20px;
            max-width: 20px;
            max-height: 20px;
            margin-right: 12px;
        }""")
    
    style_WarningModal = ("""
    WarningModal {
        border-radius: 5px;
        border: 2px solid ;
        border-color: #bb8128;
        background-color: #bb8128;
        }
        QPushButton#closeButton {
            border: none;
            outline: none;
            text-decoration: none;
            background-color: transparent;
        }
        QLabel#titlelabel{
            font-size: 12px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#bodyLabel{
            font-size: 11px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#iconlabel {
            min-width: 20px;
            min-height: 20px;
            max-width: 20px;
            max-height: 20px;
            margin-right: 12px;
        }""")

    style_ErrorModal = ("""
    ErrorModal {
        border-radius: 5px;
        border: 2px solid ;
        border-color: #bb221d;
        background-color: #bb221d;
        }
        QPushButton#closeButton {
            border: none;
            outline: none;
            text-decoration: none;
            background-color: transparent;
        }
        QLabel#titlelabel{
            font-size: 12px;
            font-weight: bold;
            color: rgb(255, 255, 255);
            
        }
        QLabel#bodyLabel{
            font-size: 11px;
            font-weight: bold;
            color: rgb(255, 255, 255);
        }
        QLabel#iconlabel {
            min-width: 20px;
            min-height: 20px;
            max-width: 20px;
            max-height: 20px;
            margin-right: 12px;
        }""")
    
    
    
    


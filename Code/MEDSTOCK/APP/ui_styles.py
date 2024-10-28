

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
    
    
    


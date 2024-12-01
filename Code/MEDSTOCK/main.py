import sys
from Pages.Dashboard.Layout_Dashboard import Dashboard
from Pages.Login.Layout_Login import Login
from dotenv import load_dotenv
from qasync import QEventLoop
from APP.UI.ui_styles import Style
from PyQt5.QtWidgets import QApplication
import logging
import asyncio

# TODO JUST FOR TESTING
from Class.utilizador import Utilizador
# TODO JUST FOR TESTING

if __name__ == "__main__":
    load_dotenv()

    logging.getLogger("requests").disabled = True
    logging.getLogger("matplotlib").disabled = True 
    logging.getLogger("urllib3").disabled = True

    app = QApplication(sys.argv)
    app.setStyleSheet(Style.style_ScrollBar)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # TODO JUST FOR TESTING
    user = Utilizador(
        nome="Bruno Oliveira Rafael", 
        email="bruno.bx04@hotmail.com", 
        sexo="M", 
        data_nascimento="1999-06-06", 
        utilizador_id=12, 
        role_id=1, 
        role_nome="Gestor Responsável"
        #role_nome="Administrador"
    )
    # TODO JUST FOR TESTING

    try:
        window = Dashboard(user=user)
        window.show()

        with loop:
            sys.exit(loop.run_forever())
    except Exception as e:
        logging.error(f"Erro na execução do MedStock: {e}")
        sys.exit(1)

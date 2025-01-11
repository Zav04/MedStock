import sys
from Pages.Login.Layout_Login import Login
from dotenv import load_dotenv
from qasync import QEventLoop
from APP.UI.ui_styles import Style
from PyQt5.QtWidgets import QApplication
import logging
import asyncio
if __name__ == "__main__":
    load_dotenv()

    logging.getLogger("requests").disabled = True
    logging.getLogger("matplotlib").disabled = True 
    logging.getLogger("urllib3").disabled = True

    app = QApplication(sys.argv)
    app.setStyleSheet(Style.style_ScrollBar)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        window=Login()
        window.show()

        with loop:
            sys.exit(loop.run_forever())
    except Exception as e:
        logging.error(f"Erro na execução do MedStock: {e}")
        sys.exit(1)

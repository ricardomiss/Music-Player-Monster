import sys
import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qasync
from modules.playerqt5 import *

async def main():
    app = QApplication(sys.argv)
    main_window = Player()
    main_window.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
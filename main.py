import sys
import asyncio
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qasync
from modules.player import *
from modules.media_control import *

def run_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(callback())

async def main():
    app = QApplication(sys.argv)
    main_window = Player()
    main_window.show()

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    callback_thread = threading.Thread(target=run_callback)
    callback_thread.start()
    try:
        asyncio.run(main())
    finally:
        callback_thread.join()
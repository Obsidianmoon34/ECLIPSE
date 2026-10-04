import threading

import uvicorn

from communication.server import app


class CommunicationServerRunner:
    def __init__(self):
        self.server = uvicorn.Server(
            uvicorn.Config(
                app,
                host="0.0.0.0",
                port=8765,
                log_level="warning",
            )
        )

        self.thread = threading.Thread(
            target=self.server.run,
            name="ECLIPSECommunicationServer",
            daemon=False,
        )

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.should_exit = True

        if self.thread.is_alive():
            self.thread.join(timeout=5)
import eventlet
import socketio
import pandas as pd
from typing import Any
from Logger import Logger
from utils.helper_functions import get_device_id
from tabulate import tabulate


class CloudServer:
    """
    Cloud server class to receive processed data from edge nodes.
    """

    def __init__(self, port: int = 20000):
        """
        Initialize the CloudServer instance.

        Args:
            port (int, optional): The port on which the cloud server will run. Defaults to 20000.
        """
        self.port = port
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)
        self.logger = Logger(name="CloudServer").get_logger()
        self.data = {}
        self.transtimes = {}
        self.proctimes = {}

    def process_edge_data(self, device_id: str, data: Any):
        """
        Receive data from an edge node.

        Args:
            device_id (str): The identifier of the edge node.
            data (Any): The processed data received from the edge node.
        """
        self.logger.info(f"Received data from edge node {device_id}: {data}")
        self.data.setdefault(device_id, [])
        self.data[device_id].append(data)

    def _print_stats(self, device_id: str):
        """
        Print the statistics for each edge node upon disconnection.
        """
        df = pd.DataFrame(
            {
                "Device ID": [device_id],
                "Amount Data Received": [len(self.data.get(device_id, []))],
                "Total Transmission Time": [self.transtimes.get(device_id, 0)],
                "Total Processing Time": [self.proctimes.get(device_id, 0)],
            }
        )
        print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))
        self.logger.info(f"Edge node {device_id} disconnected")

    def print_stats(self):
        """
        Print the statistics for all edge nodes.
        """
        df = pd.DataFrame(
            {
                "Device ID": list(self.transtimes.keys()),
                "Amount Data Received": [
                    len(self.data.get(device_id, [])) for device_id in self.data.keys()
                ],
                "Total Transmission Time": list(self.transtimes.values()),
                "Total Processing Time": list(self.proctimes.values()),
            }
        )
        print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))

    def run_server(self):
        """
        Run the cloud server.
        """
        try:
            eventlet.wsgi.server(
                eventlet.listen(("", self.port)),
                self.app,
            )
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def run(self):
        """
        Start the cloud server and set up event handlers.
        """
        server_thread = eventlet.spawn(self.run_server)

        @self.sio.event
        def connect(sid, environ):
            device_id = get_device_id(environ) or sid
            self.sio.save_session(sid, {"device_id": device_id})
            self.logger.info(f"Edge node {device_id} connected, session ID: {sid}")

        @self.sio.event
        def disconnect(sid):
            session = self.sio.get_session(sid)
            device_id = session["device_id"]
            self._print_stats(device_id)

        @self.sio.event
        def recv(sid, data):
            session = self.sio.get_session(sid)
            device_id = session["device_id"]
            if "transtime" in data and "proctime" in data:
                self.transtimes[device_id] = data["transtime"]
                self.proctimes[device_id] = data["proctime"]
            elif "data" in data:
                self.process_edge_data(device_id, data["data"])

        server_thread.wait()


if __name__ == "__main__":
    try:
        cloud = CloudServer()
        cloud.run()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        if isinstance(e, Exception):
            cloud.logger.error(f"An error occurred: {e}")
        cloud.print_stats()
        cloud.logger.info("Cloud server stopped.")
        cloud.sio.shutdown()

from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from os import path
from pathlib import Path
from threading import Thread

from urllib.parse import parse_qs, urlparse

from platform_overrides import Platform
from util.dialog import file_explorer

# P -> 16, S -> 19
SERVER_PORT = 1619
FRONTEND_DIRECTORY = Path(__file__).parent.parent / "setup-website/build"


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        super().__init__(
            request, client_address, server, directory=str(FRONTEND_DIRECTORY.resolve())
        )

    # Overridden to bypass slow FQDN lookup.
    # Copied from https://stackoverflow.com/a/5273870
    def address_string(self):
        host, port = self.client_address[:2]
        return host

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.handle_file_explorer_api(self.path[5:])

        return super().do_GET()

    def handle_file_explorer_api(self, path: str):
        parsed_url = urlparse(path)
        command = parsed_url.path
        # query_parameters = parse_qs(parsed_url.query)

        try:
            if command == "locate-rpcs3":
                return self.handle_api_locate_rpcs3()
            else:
                return self.send_error(400, "Invalid API command")
        except Exception as e:
            return self.send_error(500, str(e))

    def handle_api_locate_rpcs3(self):
        configuration_directory = self._locate_rpcs3_directory()
        rpcs3_exe = self._locate_rpcs3_exe()

        return self._send_response_json(
            {
                "executable": rpcs3_exe,
                "configurationDirectory": configuration_directory,
            }
        )

    def _locate_rpcs3_directory(self):
        default_directory = Platform.current.default_rpcs_directory

        if default_directory is not None:
            if path.exists(default_directory):
                return default_directory

        with file_explorer() as f:
            return f.dialog_open_directory(
                title="Select your RPCS3 root directory",
            )

    def _locate_rpcs3_exe(self):
        with file_explorer() as f:
            return f.dialog_open_file(
                title="Select your RPCS3 executable",
                filetypes=[
                    ("Application", Platform.current.file_extension_rpcs3),
                    ("All Files", "*.*"),
                ],
            )

    def _send_response_json(self, object):
        self.send_response(HTTPStatus.OK)

        json_string = json.dumps(object)
        json_bytes = bytes(json_string, "utf-8")

        # Development
        self.send_header("Access-Control-Allow-Origin", "http://localhost:5173")

        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(json_bytes)))
        self.end_headers()

        self.wfile.write(json_bytes)


def serve_file_explorer():
    server = ThreadingHTTPServer(("localhost", SERVER_PORT), CustomHandler)

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return server


if __name__ == "__main__":
    serve_file_explorer()

    while True:
        pass

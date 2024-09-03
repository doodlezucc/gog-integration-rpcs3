from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from os import path
import os
import string
from threading import Thread
from urllib.parse import parse_qs, urlparse

# from ..platform_overrides import Platform

# P -> 16, S -> 19
SERVER_PORT = 1619
FRONTEND_DIRECTORY = "setup-website/build"


def list_file_system_roots():
    # One liner from https://stackoverflow.com/a/34187346
    return ["%s:" % d for d in string.ascii_uppercase if path.exists("%s:" % d)]


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server, directory=FRONTEND_DIRECTORY)

    # Overridden to bypass slow FQDN lookup.
    # Copied from https://stackoverflow.com/a/5273870
    def address_string(self):
        host, port = self.client_address[:2]
        return host

    def do_GET(self):
        if self.path.startswith("/api"):
            return self.handle_file_explorer_api(self.path[5:])

        super().do_GET()

    def handle_file_explorer_api(self, path: str):
        parsed_url = urlparse(path)
        command = parsed_url.path
        query_parameters = parse_qs(parsed_url.query)

        try:
            if command == "roots":
                return self.handle_api_roots()
            elif command == "list":
                return self.handle_api_list(query_parameters)
            else:
                return self.send_error(400, "Invalid API command")
        except Exception as e:
            return self.send_error(500, str(e))

    def handle_api_roots(self):
        return self._send_response_json(
            [
                {"identifier": root_dir}
                # for root_dir in Platform.current.list_file_system_roots()
                for root_dir in list_file_system_roots()
            ]
        )

    def handle_api_list(self, params: dict):
        directory = str(params["directory"][0])

        dir_entries = os.scandir(directory)

        def file_type(is_directory: bool):
            if is_directory:
                return "directory"
            else:
                return "file"

        return self._send_response_json(
            [
                {"basename": dir_entry.name, "type": file_type(dir_entry.is_dir())}
                for dir_entry in dir_entries
            ]
        )

    def _send_response_json(self, object):
        json_string = json.dumps(object)
        json_bytes = bytes(json_string, "utf-8")

        self.send_response(HTTPStatus.OK)
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

    while True:
        pass


serve_file_explorer()

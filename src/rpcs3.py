import io
import subprocess
from os import path

from typing import List

from .platform_overrides import Platform
from .sfo import decode_sfo_file


class RPCS3:
    FILENAME_GAMES_YAML = "games.yml"

    def __init__(self, root: str):
        self.executable = path.join(root, Platform.current.filename_rpcs_executable)
        self.games_file = path.join(root, RPCS3.FILENAME_GAMES_YAML)

    def _run_with_arguments(self, args: List[str]):
        return subprocess.run([self.executable] + args)

    def read_games(self):
        with io.open(self.games_file) as file:
            file_content = file.read()
            valid_yaml_lines = [
                line for line in file_content.splitlines() if ": " in line
            ]

            return [RPCS3Game.from_yaml_line(line) for line in valid_yaml_lines]


class RPCS3Game:
    def __init__(self, id: str, directory: str):
        self.id = id
        self.directory = directory

        self._cached_sfo = None

    @staticmethod
    def from_yaml_line(line: str):
        line_parts = [part.strip() for part in line.split(": ")]

        return RPCS3Game(line_parts[0], line_parts[1])

    @property
    def _sfo(self):
        if self._cached_sfo is None:
            sfo_file = path.join(self.directory, "PS3_GAME", "PARAM.SFO")
            self._cached_sfo = decode_sfo_file(sfo_file)

        return self._cached_sfo

    @property
    def title(self) -> str:
        return self._sfo.title

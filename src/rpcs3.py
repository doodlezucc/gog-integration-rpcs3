import io
import subprocess
from os import path

from typing import List

from .sfo import decode_sfo_file


class RPCS3:
    FILENAME_GAMES_YAML = "games.yml"

    def __init__(self, executable: str, config_directory: str):
        self.executable = executable
        self.config_directory = config_directory

    @property
    def games_file(self) -> str:
        return path.join(self.config_directory, RPCS3.FILENAME_GAMES_YAML)

    def _run_with_arguments(self, args: List[str]):
        return subprocess.run([self.executable] + args)

    def read_games(self):
        with io.open(self.games_file) as file:
            file_content = file.read()
            valid_yaml_lines = [
                line for line in file_content.splitlines() if ": " in line
            ]

            return [RPCS3Game.from_yaml_line(line) for line in valid_yaml_lines]

    def _get_game_by_id(self, game_id: str):
        for game in self.read_games():
            if game.id == game_id:
                return game

        raise GameNotFoundError()

    def launch_game_by_id(self, game_id: str):
        game = self._get_game_by_id(game_id)

        game_eboot_bin = game.find_eboot_file()
        self._run_with_arguments([game_eboot_bin])


class GameNotFoundError(Exception):
    pass


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

    @property
    def _default_eboot_bin_path(self) -> str:
        return path.join(self.directory, "PS3_GAME", "USRDIR", "EBOOT.BIN")

    def find_eboot_file(self) -> str:
        # There might be alternative paths?
        return self._default_eboot_bin_path

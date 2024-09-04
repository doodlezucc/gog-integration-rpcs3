import sys
from typing import List

from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import LocalGameState, Platform
from galaxy.api.types import (
    Authentication,
    Game,
    LicenseInfo,
    LicenseType,
    LocalGame,
    NextStep,
)

from src.rpcs3 import RPCS3, RPCS3Game
from src.setup_server import serve_file_explorer


class RPCS3IntegrationPlugin(Plugin):
    VERSION = "0.1"

    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.PlayStation,
            RPCS3IntegrationPlugin.VERSION,
            reader,
            writer,
            token,
        )

    # required
    async def authenticate(self, stored_credentials=None):
        server = serve_file_explorer()

        host, port = server.server_address

        PARAMS = {
            "window_title": f"Configure, {__file__}",
            "window_width": 800,
            "window_height": 600,
            "start_uri": f"http://localhost:{port}",
            "end_uri_regex": r"^http://localhost:.*/callback.html.*",
        }

        return NextStep("rpcs3_user", PARAMS)

    async def pass_login_credentials(self, step, credentials, cookies):
        self.rpcs3 = RPCS3(
            credentials["executable"], credentials["configurationDirectory"]
        )

    # required
    async def get_owned_games(self):
        # Converts from RPCS3Game to Game instance
        def to_gog_game(game: RPCS3Game):
            gog_game = Game(
                game.id, game.title, None, LicenseInfo(LicenseType.SinglePurchase)
            )

            self.add_game(gog_game)
            return gog_game

        rpcs3_games = self.rpcs3.read_games()

        return [to_gog_game(game) for game in rpcs3_games]

    async def get_local_games(self) -> List[LocalGame]:
        # Converts from RPCS3Game to Game instance
        def to_local_game(game: RPCS3Game):
            return LocalGame(game.id, LocalGameState.Installed)

        rpcs3_games = self.rpcs3.read_games()

        return [to_local_game(game) for game in rpcs3_games]


def main():
    create_and_run_plugin(RPCS3IntegrationPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()

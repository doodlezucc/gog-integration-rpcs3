import sys
from typing import List

from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import LocalGameState, Platform
from galaxy.api.types import Authentication, Game, LicenseInfo, LicenseType, LocalGame

from src.rpcs3 import RPCS3, RPCS3Game

RPCS3_ROOT = "<redacted>"


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

        self.rpcs3 = RPCS3(RPCS3_ROOT)

    # required
    async def authenticate(self, stored_credentials=None):
        return Authentication("rpcs3_user", "RPCS3")

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

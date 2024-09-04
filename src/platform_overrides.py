import platform
from typing import Union


class Platform:
    current: "Platform"

    @property
    def file_extension_rpcs3(self) -> str:
        raise NotImplementedError()

    @property
    def default_rpcs_directory(self) -> Union[str, None]:
        return None

    @staticmethod
    def identify() -> "Platform":
        system = platform.system()

        if system == "Windows":
            return WindowsPlatform()
        elif system == "Darwin":
            return DarwinPlatform()
        elif system == "Linux":
            return LinuxPlatform()

        raise NotImplementedError("Platform not recognized")


# Windows specifics
class WindowsPlatform(Platform):
    @property
    def file_extension_rpcs3(self) -> str:
        return ".exe"


# Common MacOS/Linux specifics
class _NixPlatform(Platform):
    pass


# MacOS specifics
class DarwinPlatform(_NixPlatform):
    @property
    def file_extension_rpcs3(self) -> str:
        return ".app"

    @property
    def default_rpcs_directory(self) -> Union[str, None]:
        return "~/Library/Application Support/rpcs3"


# Linux specifics
class LinuxPlatform(_NixPlatform):
    @property
    def file_extension_rpcs3(self) -> str:
        return ".AppImage"

    @property
    def default_rpcs_directory(self) -> Union[str, None]:
        return "~/.config/rpcs3"


Platform.current = Platform.identify()

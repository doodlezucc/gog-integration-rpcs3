from os import path
import platform
import string
from typing import List


class Platform:
    current: "Platform"

    @property
    def filename_rpcs_executable(self) -> str:
        raise NotImplementedError()

    def list_file_system_roots(self) -> List[str]:
        raise NotImplementedError()

    @staticmethod
    def identify() -> "Platform":
        system = platform.system()

        if system == "Windows":
            return WindowsPlatform()

        raise NotImplementedError("Platform")


# Windows specifics
class WindowsPlatform(Platform):
    @property
    def filename_rpcs_executable(self) -> str:
        return "rpcs3.exe"

    def list_file_system_roots(self) -> List[str]:
        # One liner from https://stackoverflow.com/a/34187346
        return ["%s:" % d for d in string.ascii_uppercase if path.exists("%s:" % d)]


# Common MacOS/Linux specifics
class _NixPlatform(Platform):
    @property
    def filename_rpcs_executable(self) -> str:
        return "rpcs3"

    def list_file_system_roots(self) -> List[str]:
        return ["/"]


# MacOS specifics
class DarwinPlatform(_NixPlatform):
    pass


# Linux specifics
class LinuxPlatform(_NixPlatform):
    pass


Platform.current = Platform.identify()

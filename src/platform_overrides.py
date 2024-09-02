import platform


class Platform:
    current: "Platform"

    @property
    def filename_rpcs_executable(self) -> str:
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


# Common MacOS/Linux specifics
class _NixPlatform(Platform):
    @property
    def filename_rpcs_executable(self) -> str:
        return "rpcs3"


# MacOS specifics
class DarwinPlatform(_NixPlatform):
    pass


# Linux specifics
class LinuxPlatform(_NixPlatform):
    pass


Platform.current = Platform.identify()

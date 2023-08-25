from pathlib import Path


class FileError(Exception):
    pass


class MissingFileError(FileError):
    pass


class SystemFileReader:
    def open_file(self, path: Path) -> bytes:
        raise FileError()


class WindowsFileReader(SystemFileReader):
    def open_file(self, path: Path) -> bytes:
        raise MissingFileError()


class MacOSFileReader(SystemFileReader):
    def open_file(self, path: Path) -> bytes:
        raise ValueError()

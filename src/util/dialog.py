import tkinter as tk
from tkinter import filedialog
from typing import List, Tuple


class FileExplorer:
    def __enter__(self):
        self._tk_root = tk.Tk()
        self._tk_root.withdraw()

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self._tk_root.destroy()

    def dialog_open_file(self, title: str, filetypes: List[Tuple[str, str]]):
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
        )

    def dialog_open_directory(self, title: str, must_exist=True):
        return filedialog.askdirectory(
            title=title,
            mustexist=must_exist,
        )


def file_explorer():
    return FileExplorer()

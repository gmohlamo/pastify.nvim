from .type import Config
from .validate import validate_config
from PIL import ImageGrab
from asyncio import create_task, create_subprocess_shell, subprocess
from codecs import encode, decode
from io import BytesIO
from json import loads
from os import makedirs, path
import time
from secrets import token_urlsafe
from typing import Literal
import vim  # type: ignore


class Pastify(object):
    def __init__(self) -> None:
        self.nonce: str = token_urlsafe()
        self.config: Config = vim.exec_lua('return require("pastify").getConfig()')

    def logger(self, msg: str, level: Literal["WARN", "INFO", "ERROR"]) -> None:
        vim.command(f'lua vim.notify("{msg}", vim.log.levels.{level or "INFO"})')

    def get_path(self):
        file_path = path.normpath(vim.exec_lua('return require("pastify").getFilePath()'))
        return path.abspath(file_path)

    def get_image_path_name(self, relative: bool = False):
        image_path_name: str = vim.exec_lua(
            'return require("pastify").createImagePathName()'
        )
        return path.normpath("./" + image_path_name)

    def paste_text(self, after) -> None:
        img = ImageGrab.grabclipboard()
        # ImageGrab.grabclipboard returns either a: Image, List of file names or None (text)
        if img is None:
            # Get text from clipboard instead
            if after:
                vim.command('normal! "+p')
            else:
                vim.command('normal! "+P')
            return

        options = self.config["opts"]

        # Filetype should be run each time for each new buffer
        filetype: str = vim.exec_lua("return vim.bo.filetype")

        # The path should be re-run for each paste in case the buffer path changed
        local_path: str = self.get_path()

        if not validate_config(
            self.config,
            self.logger,
            filetype,
        ):
            return

        file_name = "" # just setting this as an empty string instead

        timestamp = int(time.time())
        file_name = f"image_{timestamp}"

        if path.exists(
            path.join(local_path, self.get_image_path_name(), f"{file_name}.png")
        ):
            self.logger("File already exists.", "WARN")
            return

        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        placeholder_text = ""
        assets_path = path.abspath(
            path.join(local_path, self.get_image_path_name())
        )

        abs_img_path = path.join(assets_path, f"{file_name}.png")

        if not path.exists(assets_path):
            makedirs(assets_path)

        placeholder_text = path.join(assets_path, f"{file_name}.png")
        self.logger("Full path {}".format(placeholder_text), "INFO")
        img.save(abs_img_path, "PNG")

        if filetype not in self.config["ft"]:
            filetype = self.config["opts"]["default_ft"]
        pattern = self.config["ft"][filetype].replace("$IMG$", placeholder_text)
        # check if we're in visual mode to run a different command
        if vim.eval("mode()") in ["v", "V", ""]:
            vim.command(f"normal! c{pattern}")
        else:
            if after:
                vim.command(f"normal! a{pattern}")
            else:
                vim.command(f"normal! i{pattern}")

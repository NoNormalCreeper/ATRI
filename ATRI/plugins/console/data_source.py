import json
import socket
import string
from random import sample
from pathlib import Path

from nonebot.permission import SUPERUSER

from ATRI.service import Service
from ATRI.utils import request
from ATRI.exceptions import WriteFileError


CONSOLE_DIR = Path(".") / "data" / "plugins" / "console"
CONSOLE_DIR.mkdir(parents=True, exist_ok=True)


class Console(Service):
    def __init__(self):
        Service.__init__(
            self, "控制台", "前端管理页面", True, main_cmd="/con", permission=SUPERUSER
        )

    @staticmethod
    async def get_host_ip(is_pub: bool):
        if is_pub:
            data = await request.get("https://ifconfig.me/ip")
            return data.text

        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            if s:
                s.close()

    @staticmethod
    def get_random_str(k: int) -> str:
        return "".join(sample(string.ascii_letters + string.digits, k))

    @staticmethod
    def get_auth_info() -> dict:
        df = CONSOLE_DIR / "data.json"
        if not df.is_file():
            try:
                with open(df, "w", encoding="utf-8") as w:
                    w.write(json.dumps({}))
            except Exception:
                raise WriteFileError(f"Writing file: {str(df)} failed!")

        base_data: dict = json.loads(df.read_bytes())
        data = base_data.get("data")
        return data or {"data": None}

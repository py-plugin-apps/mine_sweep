import re
from .data_source import MineSweeper, GameState, OpenResult, MarkResult
from .utils import skin_list
from core import Handler, Request, Response, RequestIterator, ResponseIterator

package = "mine_sweep"


class CellException(Exception):
    def __init__(self, cell):
        self.cell = cell


def calc_xy(cell):
    x = ord(cell[:1].lower()) - ord("a")
    y = int(cell[1:]) - 1
    return x, y


@Handler.StreamToStream
async def sweep(request_iterator: RequestIterator) -> ResponseIterator:
    request = await request_iterator.__anext__()

    if request.message == "中级":
        game = MineSweeper(16, 16, 40)
    elif request.message == "高级":
        game = MineSweeper(16, 30, 99)
    else:
        game = MineSweeper(9, 9, 10)

    yield Response(
        message="扫雷已开始，发送 挖开+区域号 挖开区域，发送 标记+区域号 标记区域（可以连续写多个区域号）\n发送 邀请+@群成员 或 邀请所有人 邀请其他人一起扫雷",
        image=game.draw(),
        messageDict={"at": request.event.sender.qq}
    )

    while True:
        request = await request_iterator.__anext__()
        msg = request.message
        if msg.startswith("挖开"):
            try:
                for i in re.findall(r"[a-z]\d+", msg.lower()):

                    x, y = calc_xy(i)
                    if x >= game.row or y >= game.column:
                        raise CellException(i)

                    game.open(x, y)
            except CellException as e:
                yield Response(f"无效的坐标:{e.cell}")
                continue
            if game.state == GameState.FAIL or game.state == GameState.WIN:
                break
            yield Response(image=game.draw())

        elif msg.startswith("标记"):
            try:
                for i in re.findall(r"[a-z]\d+", msg.lower()):
                    x, y = calc_xy(i)
                    if x >= game.row or y >= game.column:
                        raise CellException(i)

                    game.mark(x, y)
            except CellException as e:
                yield Response(f"无效的坐标:{e.cell}")
                continue
            yield Response(image=game.draw())
        else:
            yield Response("发送 挖开+区域号 挖开区域，发送 标记+区域号 标记区域")
    if game.state == GameState.WIN:
        msg = "游戏结束,恭喜通关"
    else:
        msg = "游戏结束"

    yield Response(msg, image=game.draw())

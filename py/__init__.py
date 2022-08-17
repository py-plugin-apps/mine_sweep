from .data_source import MineSweeper, GameState, OpenResult, MarkResult
from .utils import skin_list
from core import Handler, Request, Response, RequestIterator, ResponseIterator

package = "mine_sweep"


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
        message="扫雷已开始，发送 挖开+区域号 挖开区域，发送 标记+区域号 标记区域,发送 邀请+@群成员 邀请其他人一起扫雷",
        image=game.draw(),
        messageDict={"at": request.event.sender.qq}
    )

    while True:
        request = await request_iterator.__anext__()
        msg = request.message
        if msg.startswith("挖开"):
            try:
                x, y = calc_xy(msg[2:])
                if x >= game.row or y >= game.column:
                    raise Exception()
            except Exception:
                yield Response("无效的坐标!")
                continue

            game.open(x, y)
            if game.state == GameState.FAIL or game.state == GameState.WIN:
                break
            yield Response(image=game.draw())

        elif msg.startswith("标记"):
            try:
                x, y = calc_xy(msg[2:])
                if x >= game.row or y >= game.column:
                    raise Exception()
            except Exception:
                yield Response("无效的坐标!")
                continue

            game.mark(x, y)
            yield Response(image=game.draw())
        else:
            yield Response("发送 挖开+区域号 挖开区域，发送 标记+区域号 标记区域")

    yield Response("游戏结束", image=game.draw())

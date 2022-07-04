"""VI-Ri
ASCIIフォーマットの`.par`ファイルからVIデータを抽出, 抵抗値を算出してExcelへ出力する。
Excelには Current[A], Voltage[V], Time[s], Current[μA], Ri[Ω], VIグラフが含まれる。
"""

from src.views.view import UserInterFace
from src.controllers.controller import Controller
from src.controllers.handler import Handler


interface = UserInterFace()
controller = Controller(interface)
handler = Handler(controller)

while True:
    event, __ = controller.interface.window.read()
    handler.handle(event)

    if event is None:
        break

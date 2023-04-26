from ppt.accessor import PresentationAccessor
from ppt import types

from pprint import pprint

PPT_PATH = "./_sample_data/sample.pptx"
IMG_PATH = "./_sample_data/Python.png"

def main() -> None:
    presentation = PresentationAccessor(PPT_PATH)

    # スライドレイアウト情報を取得して使いたいレイアウトを選択する
    # NOTE: ユーザに指定させる場合は .name 情報を使うと良い
    pprint(presentation.slide_layouts)
    presentation.change_slide_layout(6) # 白紙をアクティブに

    # スライドの追加・複製・削除
    print(presentation.number_of_slide) # 1
    presentation.add_slide(change_active_slide=False)
    presentation.add_slide(change_active_slide=False)
    presentation.duplicate_slide(src_slide_index=0, change_active_slide=False)
    print(presentation.number_of_slide) # 4
    presentation.remove_slide(1)
    print(presentation.number_of_slide) # 3
    # 残っているのは複製元、空、複製先

    # アクティブなスライドの変更に失敗してみる
    try:
        presentation.change_active_slide(3)
    except IndexError as e:
        print(e)
        print("存在しないスライドを指定するとエラーになる.\n適切なエラーハンドリングが必要.")
    # 変更する
    presentation.change_active_slide(2) # 複製先をアクティブに

    # アクティブなスライドの情報を読み取る
    rectangles = presentation.get_contents(types.SHAPE_TYPES.rectangle)
    pprint(rectangles)

    # ↑の情報を元にスライドに図形を追加する
    presentation.change_active_slide(1) # 空のスライドをアクティブに
    for rectangle in rectangles:
        presentation.add_picture(types.Picture(rectangle.coordinates, rectangle.size, IMG_PATH))

    # 保存
    # 返り値として保存の成功/失敗が返ってくる
    is_saved = presentation.save_as("./_sample_data/output.pptx")
    # presentation.overwrite() # 上書き保存


if __name__ == "__main__":
    main()

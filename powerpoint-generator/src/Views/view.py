import PySimpleGUI as sg

import src.config as config


"""
GUI Styles

enabled_events
    通常イベントが発火しない要素に対してTrueを指定するとイベントが発火するようになる。
    例) FolderBrowse → InputTextへの入力時のイベントをキャッチして何かする
disabled
    使用不可にする。
    イベントの発火をキャッチしてこの要素を切り替えることで使用可/不可のコントロールが可能。
"""
TITLE = "PowerPointFormatter"
FONT = "MeiryoUI"
WINDOW_SIZE = (1000, 600)
THEME_COLOR = "BlueMono"

sg.theme(THEME_COLOR)

# Window
WINDOW_STYLES = {
    "title": TITLE,
    "size": WINDOW_SIZE,
    "font": FONT,
    "resizable": True,
}

# レイアウトパターンの選択
SELECT_LAYOUT_PATTERN_STYLES = {
    "FRAME": {
        "title": "レイアウトパターンの選択",
        "title_color": "green",  # TODO いい感じの色を選ぶ
        "relief": sg.RELIEF_SOLID,
    },
    # 特定フォーマットデータ
    "PATTERN1_RADIO": {
        "key": "-SELECT_PATTERN1-",
        "group_id": "SELECT_OUTPUT_PATTERN",
        "size": (40, 1),
        "enable_events": True,
        "default": True,  # デフォルト選択
    },
    # 順序データ
    "PATTERN2_RADIO": {
        "key": "-SELECT_PATTERN2-",
        "group_id": "SELECT_OUTPUT_PATTERN",
        "enable_events": True,
        "size": (40, 1),
    },
}

# PowerPointの入力
PWT_BROWSE_STYLES = {
    "FRAME": {
        "title": "設定用PowerPointの選択",
        # "title_color": 'red',  # TODO いい感じの色を選ぶ
        "relief": sg.RELIEF_SOLID,
    },
    "INPUT_TEXT": {
        "key": "-USER_UTIL_PWT-",
        "enable_events": True,
        "disabled": True,
        "size": (30, 1),
    },
    "FILE_BROWSE": {
        "size": (15, 1),
        "font": (FONT, 10),
        "file_types": (("pptxファイル", "*.pptx"), ("pptmファイル", "*.pptm"))
    },
    "SLIDE_DESC_TEXT": {
        "size": (20, 1),
        "font": (FONT, 15),
        "justification": "right"
    },
    "COMBO_TEMPLATE_INDEX": {
        "key": "-TEMPLATE_INDEX-",
        "enable_events": True,
        "values": [""],
        "default_value": "",
        "size": (5, 1),
    },
}

# 画像の入力
IMAGE_BROWSE_STYLES = {
    "FRAME": {
        "title": "画像の入力方法 / 使用する画像の選択",
        "title_color": 'red',  # TODO いい感じの色を選ぶ
        "relief": sg.RELIEF_SOLID,
    },
    # ラジオボタン
    "FOLDER_RADIO": {
        "key": "-SELECT_FOLDER-",
        "group_id": "IMAGE_INPUT_METHOOD",
        "tooltip": "フォルダを1つ指定する(フォルダ内の画像を対象に処理を行う)",
        "size": (20, 1),
        "enable_events": True,
        "default": True,
    },
    "FILES_RADIO": {
        "key": "-SELECT_FILES-",
        "group_id": "IMAGE_INPUT_METHOOD",
        "tooltip": "ファイルを複数選択する(選択したファイルを対象に処理を行う)",
        "size": (20, 1),
        "enable_events": True,
    },
    # フォルダ入力
    "FOLDER_INPUT_TEXT": {
        "key": "-SRC_FOLDER-",
        "size": (30, 1),
        "enable_events": True,
        "disabled": True,
    },
    "FOLDER_BROWSE": {
        "key": "-BROWSE_FOLDER-",
        "size": (15, 1),
        "font": (FONT, 10),
    },
    # ファイル入力
    "FILES_INPUT_TEXT": {
        "key": "-SRC_FILES-",
        "text_color": "gray",
        "size": (30, 1),
        "enable_events": True,
        "disabled": True,
    },
    "FILES_BROWSE": {
        "key": "-BROWSE_FILES-",
        "tooltip": "画像ファイルを複数選択(jpg, png, bmpに対応)",
        "size": (15, 1),
        "font": (FONT, 10),
        "file_types": (("pngファイル", "*.png"), ("jpgファイル", "*.jpg"), ("jpegファイル", "*.jpeg"), ("bmpファイル", "*.bmp")),
        "files_delimiter": config.FILES_BROWSE_DELIMITER,
        "disabled": True,
    },
}

# ラベル部分の選択
SELECT_LABEL_PART_STYLES = {
    "DESC_TEXT": {
        "text": "連番 or レイアウト に当たる箇所を選択してください",
        "size": (40, 1),
        "font": (FONT, 15),
    },
    "TEXT": {
        "text": "元画像名: ",
        "size": (10, 1),
        "font": (FONT, 12),
    },
    "PLACEHOLDER": {
        "key": "-LABEL_PART_PLACEFOLDER-",
        "text": "未入力",
        "size": (30, 1),
        "font": (FONT, 12),
    },
    "COMBO": {
        "key": "-LABEL_PART-",
        "tooltip": "レイアウトに相当する箇所を選択する",
        "values": ["", ""],
        "default_value": "",
        "size": (20, 1),
    }
}

# 実行
SUBMIT_STYLES = {
    "FRAME": {
        "title": "処理の実行",
        "title_color": "black",
        "relief": sg.RELIEF_SOLID,
    },
    "BUTTON": {
        "key": "-SUBMIT-"
    },
    "CHECK_OPEN_FILE": {
        "key": "-CHECK_OPEN_FILE-",
        "tooltip": "チェックを入れた場合、出力ファイルを自動的に開く",
        "size": (20, 1),
        "default": True,
    },
    "DESC_TEXT": {
        "text": "出力ファイル名を入力 (入力しなかった場合自動的に現在時刻が割り当てられる)",
        "size": (70, 1),
        "font": (FONT, 15),
    },
    "INPUT_TEXT": {
        "key": "-OUTPUT_NAME-",
        "size": (40, 1),
    },
}


class InterFace:
    """UI"""

    def __init__(self):
        select_layout_pattern_frame = sg.Frame(
            layout=[
                [sg.Radio("ラベル位置に配置(1画像:複数データ)", **SELECT_LAYOUT_PATTERN_STYLES["PATTERN1_RADIO"])],
                [sg.Radio("順に並べる(1画像:1データ)", **SELECT_LAYOUT_PATTERN_STYLES["PATTERN2_RADIO"])],
            ], **SELECT_LAYOUT_PATTERN_STYLES["FRAME"]
        )

        powerpoint_browse_frame = sg.Frame(
            layout=[
                [
                    sg.InputText(**PWT_BROWSE_STYLES["INPUT_TEXT"]),
                    sg.FileBrowse("ファイル選択", **PWT_BROWSE_STYLES["FILE_BROWSE"]),
                ],
                [
                    sg.T("使用するスライドを選択: ", **PWT_BROWSE_STYLES["SLIDE_DESC_TEXT"]),
                    sg.Combo(**PWT_BROWSE_STYLES["COMBO_TEMPLATE_INDEX"]),
                ],
            ], **PWT_BROWSE_STYLES["FRAME"]
        )

        image_browse_frame = sg.Frame(
            layout=[
                [
                    sg.Radio("フォルダ指定", **IMAGE_BROWSE_STYLES["FOLDER_RADIO"]),
                    sg.InputText(**IMAGE_BROWSE_STYLES["FOLDER_INPUT_TEXT"]),
                    sg.FolderBrowse("フォルダ選択", **IMAGE_BROWSE_STYLES["FOLDER_BROWSE"]),
                ],
                [
                    sg.Radio("複数ファイル選択", **IMAGE_BROWSE_STYLES["FILES_RADIO"]),
                    sg.InputText(**IMAGE_BROWSE_STYLES["FILES_INPUT_TEXT"]),
                    sg.FilesBrowse("ファイル選択", **IMAGE_BROWSE_STYLES["FILES_BROWSE"]),
                ],
                [sg.T(**SELECT_LABEL_PART_STYLES["DESC_TEXT"])],
                [
                    sg.T(**SELECT_LABEL_PART_STYLES["TEXT"]),
                    sg.T(**SELECT_LABEL_PART_STYLES["PLACEHOLDER"]),
                    sg.Combo(**SELECT_LABEL_PART_STYLES["COMBO"])
                ],
            ],
            **IMAGE_BROWSE_STYLES["FRAME"]
        )

        submit_frame = sg.Frame(
            layout=[
                [sg.T(**SUBMIT_STYLES["DESC_TEXT"])],
                [sg.Input(**SUBMIT_STYLES["INPUT_TEXT"])],
                [
                    sg.Submit("実行", **SUBMIT_STYLES["BUTTON"]),
                    sg.Checkbox("出力ファイルを開く", **SUBMIT_STYLES["CHECK_OPEN_FILE"])
                ],
            ], **SUBMIT_STYLES["FRAME"]
        )

        self.window = sg.Window(
            layout=[
                [select_layout_pattern_frame],
                [powerpoint_browse_frame],
                [image_browse_frame],
                [submit_frame],
            ],
            **WINDOW_STYLES,
        )

    def close_window(self):
        """windowを閉じる"""
        self.window.close()
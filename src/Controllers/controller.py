import os
import re
import glob
import shutil
import pathlib
import subprocess
import PySimpleGUI as sg
from datetime import datetime

import src.config as config
from src.Models.slide import SlideGenerator
from src.Models.sorter import ImageSorter, LabeledImage, TextBoxSorter
from src.Models.presentation import PresentationReader, PresentationWriter
from src.Views.popup import Popup


class Controller():
    def __init__(self, window) -> None:
        self.window = window
        self.reader: PresentationReader
        self.image_templates: list
        self.textbox_templates: list
        self.input_images: list[pathlib.Path]

    # Events
    def input_user_util_pwt(self, values):
        """ユーザー設定PowerPoint入力"""
        self.reader = PresentationReader(values["-USER_UTIL_PWT-"])
        # スライドの枚数を取得 ユーザに表示を合わせるため1からスタートする
        new_values = [i for i in range(1, self.reader.get_number_of_slide() + 1)]
        self._update_combo("-TEMPLATE_INDEX-", new_values)
        self._receive_templates(values)

    def select_folder(self, __):
        """フォルダ入力 選択"""
        self._enable("-BROWSE_FOLDER-")
        self._disable("-BROWSE_FILES-")
        self._change_text_color("-SRC_FOLDER-", sg.theme_element_text_color())
        self._change_text_color("-SRC_FILES-", "gray")

    def select_files(self, __):
        """複数ファイル入力 選択"""
        self._disable("-BROWSE_FOLDER-")
        self._enable("-BROWSE_FILES-")
        self._change_text_color("-SRC_FOLDER-", "gray")
        self._change_text_color("-SRC_FILES-", sg.theme_element_text_color())

    def input_img_folder(self, values):
        """画像ファイル 入力(フォルダ指定)"""
        self._receive_images_from_folder(values)
        # 画像が存在しないフォルダが選択された場合
        if not self.input_images:
            self._update("-SRC_FOLDER-", "")
            Popup.call_error_popup("選択されたフォルダは画像が存在しません。")
            return
        self._update_select_label_part()

    def input_img_files(self, values):
        """画像ファイル 入力(複数ファイル)"""
        self._receive_images_from_files(values)
        self._update_select_label_part()

    def select_template_index(self, values):
        """ベーススライドのインデックス 選択"""
        self._receive_templates(values)

    def click_submit(self, values):
        """処理の実行"""
        # 入力のバリデーション(失敗した場合中断)
        if not self.validate_input(values):
            return
        # srcファイルのコピー(失敗した場合中断)
        if not (dst_path := self._copy_src_file(values)):
            return

        label_part_index = self._receive_label_part_index(values)
        # 選択されたパターンに応じて分岐する
        if values["-SELECT_PATTERN1-"]:
            slide_generator = self._set_laidout_images(label_part_index)
        elif values["-SELECT_PATTERN2-"]:
            slide_generator = self._set_sequence_images(label_part_index)

        if self.textbox_templates:
            slide_generator = self._set_textboxes(slide_generator)

        # TODO 失敗した場合生成したファイルは削除する
        # Helper.delete_file(dst_path)

        writer = PresentationWriter(dst_path, slide_generator.slides)
        writer.set_empty_slides(self._receive_template_slide_index(values))
        writer.add_images()
        writer.add_textboxes()
        writer.save(dst_path)

        if values["-CHECK_OPEN_FILE-"]:
            Helper.open_result(dst_path)

        Helper.finish_process()

    def _copy_src_file(self, values) -> str | None:
        if values["-OUTPUT_NAME-"]:
            dst_path = Helper.copy_file(values["-USER_UTIL_PWT-"], values["-OUTPUT_NAME-"])
        else:
            dst_path = Helper.copy_file_and_append_timestamp(values["-USER_UTIL_PWT-"])
        return dst_path

    def _set_laidout_images(self, label_part_index: int) -> SlideGenerator:
        # TODO 適切な大きさに切り分ける & エラーキャッチしてGUIに通知
        image_sorter = ImageSorter(self.input_images)
        grouped_images = image_sorter.labeling_images(label_part_index)
        total_number_of_contents = Helper.get_total_number_of_contents(grouped_images)
        slide_generator = SlideGenerator(self.image_templates, config.IMAGE_KEY, total_number_of_contents)
        slide_generator.set_laidout_images_to_slides(grouped_images)
        return slide_generator

    def _set_sequence_images(self, label_part_index: int) -> SlideGenerator:
        # TODO 適切な大きさに切り分ける & エラーキャッチしてGUIに通知
        image_sorter = ImageSorter(self.input_images)
        image_sorter.sort_based_on_numeric_part(label_part_index)
        grouped_images = image_sorter.labeling_images(label_part_index)
        total_number_of_contents = Helper.get_total_number_of_contents(grouped_images)
        slide_generator = SlideGenerator(self.image_templates, config.IMAGE_KEY, total_number_of_contents)
        slide_generator.sort_template_images_by_numeric_label()
        slide_generator.set_sequence_images_to_slides(grouped_images)
        return slide_generator

    def _set_textboxes(self, slide_generator: SlideGenerator):
        # TODO 適切な大きさに切り分ける & エラーキャッチしてGUIに通知
        tb_sorter = TextBoxSorter(self.textbox_templates)
        tb_sorter.sort_based_on_label(config.REGEX_POINTING_GROUP, config.REGEX_POINTING_LABEL)
        sorted_textboxes = tb_sorter.sorted_textboxes
        [slide_generator.set_textboxes_to_template(i) for i in sorted_textboxes]
        slide_generator.set_textboxes_to_slides()
        return slide_generator

    # From View
    def _receive_images_from_folder(self, values: dict, regex=config.REGEX_IMAGE):
        """入力されたフォルダから画像を受け取る。

        Parameters
        ----------
        values : dict
            GUIの持つ値。
        regex : str
            画像ファイルにマッチするパターン, by default config.REGEX_IMAGE
        """
        p = pathlib.Path(values["-SRC_FOLDER-"])
        self.input_images = sorted([i for i in p.glob('**/*') if re.search(regex, str(i))])

    def _receive_images_from_files(self, values: dict, delimiter=config.FILES_BROWSE_DELIMITER):
        """入力されたfilesから画像を受け取る。

        Parameters
        ----------
        values : dict
            GUIの持つ値。
        delimiter : str
            filesの区切り文字, by default config.FILES_BROWSE_DELIMITER
        """
        files = values["-SRC_FILES-"].split(delimiter)
        self.input_images = sorted([pathlib.Path(f) for f in files])

    def _receive_templates(self, values):
        """テンプレートの情報を受け取る。"""
        # 最初の呼び出し時は-TEMPLATE_INDEX-が空なので0をセットする
        slide_index = int(values["-TEMPLATE_INDEX-"] - 1) if values["-TEMPLATE_INDEX-"] else 0
        try:
            self.image_templates = self.reader.get_image_templates(slide_index)
            self.textbox_templates = self.reader.get_textbox_templates(slide_index, config.REGEX_POINTING_GROUP, config.REGEX_POINTING_LABEL)
        except IndexError:
            Popup.call_error_popup("存在しないスライドが選択されました。設定を確認してください。")

    def _receive_label_part_index(self, values) -> int:
        """ラベル部分のインデックスを受け取る。"""
        # Comboの持つvaluesには .Values でアクセスできる
        label = self.window["-LABEL_PART-"].Values
        selected_layout_part = values["-LABEL_PART-"]
        return label.index(selected_layout_part)

    def _receive_template_slide_index(self, values) -> int:
        """テンプレートとして使うスライドのインデックス(何枚目か)を受け取る。"""
        # 表示をユーザーに合わせてあるため -1 する。
        return int(values["-TEMPLATE_INDEX-"]) - 1

    # To View
    def _disable(self, key):
        """要素を無効にする"""
        self.window[key].update(disabled=True)

    def _enable(self, key):
        """要素を有効にする"""
        self.window[key].update(disabled=False)

    def _change_text_color(self, key: str, color: str):
        """要素のtext_colorを変更する"""
        self.window[key].update(text_color=color)

    def _to_visible(self, key):
        """要素を可視化する"""
        self.window[key].update(visible=True)

    def _to_hidden(self, key):
        """要素を隠す"""
        self.window[key].update(visible=False)

    def _update(self, key, new_value):
        """要素のvalue更新"""
        self.window[key].update(new_value)

    def _update_combo(self, key, new_values, default_index=0):
        """Comboの更新"""
        self.window[key].update(values=new_values)
        self.window[key].update(value=new_values[default_index])

    def _update_select_label_part(self):
        """ラベル部分選択用のCombo, Text更新"""
        representative = self.input_images[0]
        # delimiterで区切った結果をプレビューとして表示
        image_stem_previews = representative.stem.split(config.DELIMITER)
        self._update_combo("-LABEL_PART-", image_stem_previews, -1)
        image_preview = representative.name
        self._update("-LABEL_PART_PLACEFOLDER-", image_preview)

    # validation
    def validate_input(self, values) -> bool:
        """入力のバリデーション"""
        # PowerPointが入力されていない場合
        if not values["-USER_UTIL_PWT-"]:
            Popup.call_error_popup("設定用PowerPointが入力されていません")
            return False
        # 画像が入力されていない場合
        if not values["-SRC_FOLDER-"] and not values["-SRC_FILES-"]:
            Popup.call_error_popup("画像ファイルが入力されていません")
            return False
        # PowerPointは入力されているがフォーマットが存在しない場合(PowerPoint入力確認後)
        if not self.image_templates:
            Popup.call_error_popup("選択されたPowerPointのスライドには四角形が存在しないため画像を出力できません。\n設定を確認してください。")
            return False
        return True
class Helper():
    def __init__(self) -> None:
        pass

    @staticmethod
    def open_result(output_path):
        """ファイルを開く"""
        subprocess.Popen(['start', output_path], shell=True)

    @staticmethod
    def finish_process():
        """終了処理"""
        Popup.call_success_popup("処理が成功しました!")

    @staticmethod
    def copy_file_and_append_timestamp(src: str, dt_format='%y%m%d_%H%M') -> str | None:
        """[現在時刻.拡張子]形式のコピーを作成"""
        dt_now = datetime.now()
        dt_now = dt_now.strftime(dt_format)
        p = pathlib.Path(src)

        dst = f"{dt_now}{p.suffix}"

        # すでに同じタイムスタンプのファイルが存在する場合
        if glob.glob(dst):
            Popup.call_error_popup("タイムスタンプが重複しています。\n1分以上経ってから再度実行するか、名前を指定してください。")
            return
        shutil.copy(src, dst)
        return dst

    @staticmethod
    def copy_file(src: str, dst: str) -> str | None:
        """コピーを作成"""
        p = pathlib.Path(src)
        dst = f"{dst}{p.suffix}"
        try:
            shutil.copy(src, dst)
        except Exception:
            Popup.call_error_popup('出力ファイル名が無効です。\n・重複した名前を指定している可能性があります。\n・次の文字は使用できません。\n  ¥ : / * ? " < > | ')
            return
        return dst

    @staticmethod
    def delete_file(path: str):
        """ファイルを削除
        """
        try:
            os.remove(path)
        except FileNotFoundError:
            print("指定されたファイルは存在しません")

    @staticmethod
    def get_total_number_of_contents(grouped_images: dict[str, list[LabeledImage]]):
        total_number_of_contents = 0
        [total_number_of_contents := total_number_of_contents + len(group) for group in grouped_images.values()]
        return total_number_of_contents

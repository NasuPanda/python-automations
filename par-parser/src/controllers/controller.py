import math
import pathlib
import numpy as np

import config
from src.views.view import UserInterFace
from src.services.engine import ExtractVIDataFromParEngine, WriteVIDataToExcelEngine, VIData
from src.services.validate import Validator
from src.utils.exceptions import ValidationError


class Controller():
    """コントローラ。Model⇔Viewのつなぎ込みを行う。

    Class variables
    ----------
    config.DELIMITER: "_"
        ファイル名の区切り文字。
    config.VOLTAGE_RANGE (0.1, 2.0)
        入力電圧の許容幅。

    Instance variables
    ----------
    interface: UserInterface
        UserInterfaceクラスのインスタンス。
        GUIの更新, 値の取得に使用。
    par_paths: list[pathlib.Path]
        Pathオブジェクト(拡張子.par)の配列。
    data_name_part_indexes: list[int]
        データ名を指す箇所(config.DELIMITER区切り)のインデックスの配列。
        パスのソートに使用。
    data_names: list[str]
        データ名の配列。
    vi_data_array: list[VIData]
        VIデータの配列。
        アプリケーションの核となるデータを格納する。
    is_display_vi_data_already_added: bool
        VIデータのGUIが既に更新されているかどうか判定するためのフラグ。
    experiment_mode: str
        試験のモード。この値により電圧が変動する。
    sheets_per_file: int
        1ファイル(Excel)に何シート含まれるか。
        データ数が指定シートより少ない場合はデータ数=シート数になる。
    """

    def __init__(self, interface: UserInterFace) -> None:
        """インスタンスの初期化。

        Parameters
        ----------
        interface : UserInterFace
            UserInterfaceクラスのインスタンス。
        """
        self.interface: UserInterFace = interface
        # NOTE: 判定に使うので明示的に空として初期化する
        self.par_paths: list[pathlib.Path] = []
        self.data_name_part_indexes: list[int] = []
        self.data_names: list[str] = []
        self.vi_data_array: list[VIData] = []
        self.is_display_vi_data_already_added = False

        self.experiment_mode: str = config.DEFAULT_SELECT_EXPERIMENT_MODE_COMBO_VALUE
        self.sheets_per_file: int = config.DEFAULT_SHEET_PER_FILE_VALUE

    def parse_par_to_vi_data(self):
        """.par => .csv => VIデータの取り出しを実行
        """
        self.interface.print_notice(".par => .csv => slope算出 処理中...")

        # 入力のバリデーション
        try:
            Validator.validate_presence(self.par_paths, "parファイル")
            Validator.validate_presence(self.data_names, "サンプル名(選択する)")
            Validator.validate_array_length_equality(self.par_paths, self.data_names)
        except ValidationError as e:
            self.interface.print_alert(str(e))
            return

        # サービス層の処理を実行
        engine = ExtractVIDataFromParEngine(self.experiment_mode)
        for par_path, data_name in zip(self.par_paths, self.data_names):
            vi_data = engine.perform(par_path, data_name)
            self.vi_data_array.append(vi_data)

        self.interface.print_notice(".par => .csv => slope算出 処理完了.")

        # データをGUIへ反映
        self.__add_vi_data_components_to_interface()
        self.update_display_vi_data()

    def __add_vi_data_components_to_interface(self):
        """VIデータのコンポーネントをGUIに追加, 表示する
        """
        # 既に追加されていれば実行しない
        if self.is_display_vi_data_already_added:
            return

        [
            self.interface.add_component_to_container(*self.interface.EXTENDABLE_COMPONENT_KEYS)
            for _ in range(len(self.vi_data_array))
        ]
        self.is_display_vi_data_already_added = True

    def update_display_vi_data(self):
        """GUIに表示されているVIデータをインスタンス変数を元に更新する
        """
        # 見栄えのためにround()で丸めている
        self.interface.update_all_resistances([round(vi.resistance, 2) for vi in self.vi_data_array])
        self.interface.update_all_judge([vi.is_resistance_valid for vi in self.vi_data_array])
        self.interface.update_all_min_voltage([vi.min_voltage for vi in self.vi_data_array])
        self.interface.update_all_max_voltage([vi.max_voltage for vi in self.vi_data_array])

    def update_vi_data(self):
        """VIデータを更新する(インスタンス変数, GUIともに)
        """
        # NOTE: 無効になっていない値は電圧を変更しても更新されない
        # index: invalid_components / vi_data_array 共通のindex
        # keys: min_voltage, max_voltageをキーとして持つcomponent_keyの辞書
        for index, component_keys in self.interface.invalid_component_keys.items():
            vi_data = self.vi_data_array[index]
            min_voltage = self.interface.component_value(
                component_keys[config.EXTENDABLE_MIN_VOLTAGE_KEY]
            )
            max_voltage = self.interface.component_value(
                component_keys[config.EXTENDABLE_MAX_VOLTAGE_KEY]
            )

            # バリデーション
            try:
                Validator.validate_numericality_and_within_range(min_voltage, *config.VOLTAGE_RANGE)
                Validator.validate_numericality_and_within_range(max_voltage, *config.VOLTAGE_RANGE)
                Validator.validate_less_than(float(min_voltage), float(max_voltage))
            except ValidationError as e:
                self.interface.print_alert(str(e))
                return

            # VIデータの更新
            # min_voltage, max_voltageは受け取った段階では str なので変換しておく
            vi_data.min_voltage = float(min_voltage)
            vi_data.max_voltage = float(max_voltage)
            vi_data.update_resistance()

            self.vi_data_array[index] = vi_data

        self.update_display_vi_data()

    def write_vi_data_to_excel(self):
        """VIデータをExcelに書き込む
        """
        self.interface.print_notice("Excel書き込み 処理中...")

        # バリデーション
        try:
            judges = self.interface.all_judges
            Validator.validate_exclusion(False, "判定がOKになっていない値", *judges)
        except ValidationError as e:
            self.interface.print_alert(str(e))
            self.interface.print_alert("Riの値を確認, 電圧を調整して「Ri更新」ボタンを押して下さい")
            return

        # sheets_per_sizeに応じてvi_data_arrayを分割
        # 例
        # len(vi_data_array): 10 / sheets_per_file: 5 => 2
        # len(vi_data_array): 12 / sheets_per_file: 5 => 3
        split_size = math.ceil(len(self.vi_data_array) / self.sheets_per_file)
        splitted_vi_data_array = self.__split_array(self.vi_data_array, split_size)

        for vi_data_array in splitted_vi_data_array:
            # 出力ファイル名の形式は データ1_データ5.xlsxとする
            # 例
            # [data1, data2, data3, data4, data5]
            # => to_excel_name: data1_data5.xlsx
            # => sheets: data1, data2, ...
            first, last = self.__get_data_name_of_first_and_last_element(vi_data_array)
            to_excel_name = f"{first}_{last}.xlsx"
            engine = WriteVIDataToExcelEngine(to_excel_name)
            engine.perform(vi_data_array)

        self.interface.print_notice("Excel書き込み 処理完了.")

    def receive_par_folder(self):
        """.parファイルが格納されたフォルダを受け取り, インスタンス変数に登録
        """
        # 既にVIデータが入力されている場合は弾く
        if self.is_display_vi_data_already_added:
            self.interface.print_alert("既にVIデータが入力されています !", "再入力することは出来ません.")
            return

        self.interface.print_notice("parファイル読み込み中...")

        # 入力の受け取り, バリデーション
        src_folder = self.interface.component_value(config.SRC_FOLDER_INPUT_KEY)
        paths = self.__get_par_paths_from_folder(src_folder)
        try:
            Validator.validate_presence(paths, "parファイル")
        except ValidationError as e:
            self.interface.print_alert(str(e))
            self.interface.clear_value(config.SRC_FOLDER_INPUT_KEY)
            return

        # データ名選択用のText, Listboxを更新
        example_path = paths[0]
        path_stem_parts = self.__split_path_stem(example_path)
        self.interface.update_component(config.SELECT_DATA_NAME_ORIGIN_FILENAME_TEXT_KEY, {"value": example_path.stem})
        self.interface.update_component(config.SELECT_DATA_NAME_PART_LISTBOX_KEY, {"values": path_stem_parts})

        # インスタンス変数の更新
        self.par_paths = paths

        self.interface.print_notice("parファイルの読み込みに成功しました。")

    def receive_sheets_per_file(self):
        """1ファイル辺りのシート数を受け取り, インスタンス変数に登録
        """
        # 入力の受け取り, バリデーション
        sheets_per_file = self.interface.component_value(config.SHEET_PER_FILE_INPUT_KEY)
        try:
            Validator.validate_numericality_and_within_range(sheets_per_file, 2, 10)
        except ValidationError as e:
            self.interface.print_alert(str(e))
            self.interface.clear_value(config.SHEET_PER_FILE_INPUT_KEY)
            return

        # インスタンス変数の更新
        self.sheets_per_file = int(sheets_per_file)

    def receive_experiment_mode(self):
        """試験モードを受け取り, インスタンス変数に登録
        """
        # 既にVIデータが入力されている場合は弾く
        if self.is_display_vi_data_already_added:
            self.interface.print_alert("既にVIデータが登録されています !", "モードを上書きすることはできません.")
            return

        self.experiment_mode = self.interface.component_value(config.SELECT_MODE_COMBO_KEY)

    def sort_par_paths(self):
        """self.par_pathsをソートする
        """
        # ListBoxから選択されたインデックスを受け取る
        data_name_part_indexes = self.interface.get_indexes(config.SELECT_DATA_NAME_PART_LISTBOX_KEY)
        if not data_name_part_indexes or not self.par_paths:
            return

        def join_parts(path: pathlib.Path):
            """path.stemをdelimiterでsplitしたpartsを指定インデックスでjoinする

            data_name_part_indexesはソートの完了が確定するまでインスタンス変数に登録したくないので関数スコープの変数を利用する
            sortのkeyとして使用するコールバック関数に引数を渡すのは面倒なため
            """
            splits = self.__split_path_stem(path)
            data_name_parts = [splits[i] for i in data_name_part_indexes]
            return config.DELIMITER.join(data_name_parts)

        try:
            self.par_paths.sort(key=join_parts)
        except Exception as e:
            self.interface.print_alert(str(e), "サンプル名の指定で問題が発生しました !")

        # インスタンス変数に登録
        self.data_name_part_indexes = data_name_part_indexes
        self.data_names = [join_parts(path) for path in self.par_paths]

    @classmethod
    def __split_path_stem(cls, path: pathlib.Path):
        """Path.stemをdelimiterで分割する
        """
        return path.stem.split(config.DELIMITER)

    @staticmethod
    def __get_par_paths_from_folder(folder_path):
        """フォルダからparファイルのpathを取得
        """
        temp_p = pathlib.Path(folder_path)
        return list(temp_p.glob('**/*.par'))

    @staticmethod
    def __split_array(array: list, section_size: int) -> list[list]:
        """配列をN分割する。

        Parameters
        ----------
        array : list
            分割したい配列。
        section_size : int
            分割後の要素数。

        Returns
        -------
        list[list]
            分割後の配列。(2次元)
        """
        return np.array_split(array, section_size)

    @staticmethod
    def __get_data_name_of_first_and_last_element(vi_data_array: list[VIData]) -> tuple[str, str]:
        """配列の最初と最後の要素のVIData.data_nameを返す

        Parameters
        ----------
        vi_data_array : list[VIData]
            VIDataインスタンスの配列。

        Returns
        -------
        tuple[str, str]
            最初と最後の要素のVIData.data_name
        """
        return vi_data_array[0].data_name, vi_data_array[-1].data_name

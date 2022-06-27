from dataclasses import dataclass

import config
import src.models.excel.calculator as excel_calculator


@dataclass
class VIData:
    """VIのデータ
    """
    MIN_RESISTANCE = config.MIN_RESISTANCE
    MAX_RESISTANCE = config.MAX_RESISTANCE

    data_name: str
    times: list[int | float]
    currents: list[int | float]
    voltages: list[int | float]
    min_voltage: int | float
    max_voltage: int | float
    resistance: int | float
    is_resistance_valid = True

    @property
    def closest_range_to_min_and_max_voltage(self) -> tuple[int, int]:
        """最小電圧, 最大電圧それぞれに最も近い値の範囲(インデックス)を返す

        Returns
        -------
        tuple[int, int]
            最小側インデックス, 最大側インデックス
        """
        return (
            excel_calculator.find_closest_value_index(self.voltages, self.min_voltage),
            excel_calculator.find_closest_value_index(self.voltages, self.max_voltage)
        )

    def calculate_resistance(self) -> float:
        """VIから抵抗値を算出する

        Returns
        -------
        float
            抵抗値
        """
        min_index, max_index = self.closest_range_to_min_and_max_voltage
        return excel_calculator.calc_slope(
            self.currents[min_index:max_index + 1],
            self.voltages[min_index:max_index + 1]  # NOTE: スライスの仕様上 +1 する必要がある
        )

    def set_is_resistance_valid(self, min: int | float, max: int | float):
        """抵抗値の有効性を検証, インスタンス変数を更新する

        Parameters
        ----------
        min : int | float
            許容最小値
        max : int | float
            許容最大値
        """
        self.is_resistance_valid = min <= self.resistance <= max

    def update_resistance(self):
        """インスタンス変数を元にインスタンスが持つ抵抗値を更新
        """
        self.resistance = self.calculate_resistance()
        self.set_is_resistance_valid(self.MIN_RESISTANCE, self.MAX_RESISTANCE)

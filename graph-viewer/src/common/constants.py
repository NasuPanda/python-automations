import re
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class ComponentKeys:
    log = "-LOG-"
    folder_input = "-INPUT_FOLDER-"
    csv_headers_listbox = "-SELECT_HEADER-"
    explorer_tree = "-TREE-"
    graph_canvas = "-CANVAS-"
    graph_range = {
        "x": {"min": "-X_AXIS_MIN-", "max": "-X_AXIS_MAX-"},
        "y": {"min": "-Y_AXIS_MIN-", "max": "-Y_AXIS_MAX-"},
    }
    graph_range_update = "-UPDATE_GRAPH_RANGE-"
    graph_range_reset = "-RESET_GRAPH_RANGE-"
    base_hline_input = {"1": "-BASE_HLINE_1-", "2": "-BASE_HLINE_2-"}
    baselines_update = "-UPDATE_BASE_HLINES-"
    time_axis_indicator_text = "-X_AXIS_INDICATOR-"


# 処理
WORD_LENGTH_REMOVE_DUPLICATE: Final = 8
TIME_AXIS_HEADER_REGEX = re.compile("time", flags=re.IGNORECASE)

# GUI
FONT = "Monospace"
FOLDER_ICON: Final = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII="
FILE_ICON: Final = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC"
LOG_TEXT_COLORS = {"notice": "green", "alert": "red"}
BASE_HLINE_NUMBERS = ("1", "2")
BASE_HLINE_COLORS = {
    "1": "red",
    "2": "blue",
}
TIME_AXIS_INDICATOR_TEXTS = {"n": "---", "y": "time[s]"}

# グラフ
PLOT_PARAM_FONT = "MS Gothic"
PLOT_PARAM_X_MARGIN = 0
PLOT_PARAM_Y_MARGIN = 0
PLOT_FIGURE_BG_COLOR = "azure"
PLOT_BASELINE_STYLE = "dashed"
PLOT_SUBPLOT_POSITION = {"left": 0.05, "right": 0.6, "bottom": 0.1, "top": 0.95}

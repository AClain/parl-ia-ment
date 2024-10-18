import pandas as pd
from typing import List
import matplotlib.text as mtext


"""
https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text
"""


def highlight_heatmap_highest_value(
    df: pd.DataFrame,
    texts: List[mtext],
    rounding: int = 2,
):
    max_indices = df.max().to_dict()

    for text in texts:
        _, col = int(text.get_position()[1]), int(text.get_position()[0])
        col_name = df.columns[col]

        if round(max_indices[col_name], rounding) == float(text.get_text()):
            text.set_fontweight("bold")
            text.set_fontsize("medium")

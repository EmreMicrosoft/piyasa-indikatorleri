# UI (Ulcer Index)
# https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

# TODO: Descriptions

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n nokta.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class UlcerIndex(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 14, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        _ui_max = self._close.rolling(self._window, min_periods=1).max()
        _r_i = 100 * (self._close - _ui_max) / _ui_max

        def ui_function():
            def _ui_function(x):
                return np.sqrt((x ** 2 / self._window).sum())

            return _ui_function

        self._ulcer_idx = _r_i.rolling(self._window).apply(ui_function(), raw=True)

    def ulcer_index(self) -> pd.Series:
        ulcer_idx = self._check_fillna(self._ulcer_idx)
        return pd.Series(ulcer_idx, name="ui")
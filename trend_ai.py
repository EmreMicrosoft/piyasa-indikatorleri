# AI (Aroon Indicator)
# https://www.investopedia.com/terms/a/aroon.asp

# Trendlerin ne zaman yön değiştirebileceğini belirlemek için kullanılır.
#     Aroon Up = ((N - Days Since N-day High) / N) x 100
#     Aroon Down = ((N - Days Since N-day Low) / N) x 100
#     Aroon Indicator = Aroon Up - Aroon Down

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class AroonIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 25, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window
        rolling_close = self._close.rolling(self._window, min_periods=min_periods)
        self._aroon_up = rolling_close.apply(
            lambda x: float(np.argmax(x) + 1) / self._window * 100, raw=True)
        self._aroon_down = rolling_close.apply(
            lambda x: float(np.argmin(x) + 1) / self._window * 100, raw=True)

    # Üst Kanal:
    def aroon_up(self) -> pd.Series:
        aroon_up_series = self._check_fillna(self._aroon_up, value=0)
        return pd.Series(aroon_up_series, name=f"aroon_up_{self._window}")

    # Alt Kanal:
    def aroon_down(self) -> pd.Series:
        aroon_down_series = self._check_fillna(self._aroon_down, value=0)
        return pd.Series(aroon_down_series, name=f"aroon_down_{self._window}")

    def aroon_indicator(self) -> pd.Series:
        aroon_diff = self._aroon_up - self._aroon_down
        aroon_diff = self._check_fillna(aroon_diff, value=0)
        return pd.Series(aroon_diff, name=f"aroon_ind_{self._window}")
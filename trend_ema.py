# EMA (Exponential Moving Average)
# TODO : link and description

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class EMAIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 14, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna

    def ema_indicator(self) -> pd.Series:
        ema_ = _ema(self._close, self._window, self._fillna)
        return pd.Series(ema_, name=f"ema_{self._window}")
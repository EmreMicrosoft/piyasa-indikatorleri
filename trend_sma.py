# SMA (Simple Moving Average)
# TODO : link and description

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _sma

class SMAIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna

    def sma_indicator(self) -> pd.Series:
        sma_ = _sma(self._close, self._window, self._fillna)
        return pd.Series(sma_, name=f"sma_{self._window}")
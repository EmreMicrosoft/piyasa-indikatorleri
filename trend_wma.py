# WMA (Weighted Moving Average)
# TODO : link and description here

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class WMAIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 9, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        _weight = pd.Series(
            [
                i * 2 / (self._window * (self._window + 1))
                for i in range(1, self._window + 1)
            ])

        def weighted_average(weight):
            def _weighted_average(x):
                return (weight * x).sum()

            return _weighted_average

        self._wma = self._close.rolling(self._window).apply(
            weighted_average(_weight), raw=True)

    def wma(self) -> pd.Series:
        wma = self._check_fillna(self._wma, value=0)
        return pd.Series(wma, name=f"wma_{self._window}")
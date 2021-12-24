# OBV (On-Balance Volume)
# https://en.wikipedia.org/wiki/On-balance_volume

# Borsada fiyat ve hacim ile ilgilidir. OBV,
#  kümülatif bir toplam hacme dayanmaktadır.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class OnBalanceVolumeIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, volume: pd.Series, fillna: bool = False):
        self._close = close
        self._volume = volume
        self._fillna = fillna
        self._run()

    def _run(self):
        obv = np.where(self._close < self._close.shift(1), -self._volume, self._volume)
        self._obv = pd.Series(obv, index=self._close.index).cumsum()

    def on_balance_volume(self) -> pd.Series:
        obv = self._check_fillna(self._obv, value=0)
        return pd.Series(obv, name="obv")
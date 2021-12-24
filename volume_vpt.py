# VPT (Volume-Price Trend)
# https://en.wikipedia.org/wiki/Volume%E2%80%93price_trend

# Yatırımın yukarı veya aşağı hareketlerine bağlı olarak,
#  hisse fiyatı eğilimindeki ve mevcut hacimdeki yüzde
#  değişikliğinin katlarını ekleyen veya çıkaran,
#  devam eden bir kümülatif hacme dayanır.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class VolumePriceTrendIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, volume: pd.Series, fillna: bool = False):
        self._close = close
        self._volume = volume
        self._fillna = fillna
        self._run()

    def _run(self):
        vpt = self._volume * (
            (self._close - self._close.shift(1, fill_value=self._close.mean()))
            / self._close.shift(1, fill_value=self._close.mean()))
        self._vpt = vpt.shift(1, fill_value=vpt.mean()) + vpt

    def volume_price_trend(self) -> pd.Series:
        vpt = self._check_fillna(self._vpt, value=0)
        return pd.Series(vpt, name="vpt")
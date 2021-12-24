# EoM - EMV (Ease of Movement)
# https://en.wikipedia.org/wiki/Ease_of_movement

# Bir varlığın fiyat değişikliğini hacmiyle ilişkilendirir
#  ve bir eğilimin gücünü değerlendirmek için özellikle yararlıdır.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class EaseOfMovementIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        volume: pd.Series,
        window: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._volume = volume
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        self._emv = (
            (self._high.diff(1) + self._low.diff(1))
            * (self._high - self._low)
            / (2 * self._volume))

        self._emv *= 100000000

    def ease_of_movement(self) -> pd.Series:
        emv = self._check_fillna(self._emv, value=0)
        return pd.Series(emv, name=f"eom_{self._window}")

    # sinyal:
    def sma_ease_of_movement(self) -> pd.Series:
        min_periods = 0 if self._fillna else self._window
        emv = self._emv.rolling(self._window, min_periods=min_periods).mean()
        emv = self._check_fillna(emv, value=0)
        return pd.Series(emv, name=f"sma_eom_{self._window}")
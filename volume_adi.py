# ADI (Accumulation/Distribution Index)
# https://school.stockcharts.com/doku.php?id=technical_indicators:accumulation_distribution_line

# Fiyat hareketlerinin öncü göstergesi olarak hareket eder.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  fillna(bool): True ise, nan değerlerini doldurun.


import pandas as pd
from ta.utils import IndicatorMixin

class AccDistIndexIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume
        self._fillna = fillna
        self._run()

    def _run(self):
        clv = ((self._close - self._low) - (self._high - self._close)) / (self._high - self._low)
        clv = clv.fillna(0.0)  # float division by zero
        adi = clv * self._volume
        self._adi = adi.cumsum()

    def acc_dist_index(self) -> pd.Series:
        adi = self._check_fillna(self._adi, value=0)
        return pd.Series(adi, name="adi")
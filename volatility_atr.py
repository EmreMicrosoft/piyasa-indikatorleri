# ATR (Average True Range)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr

# Bu gösterge, fiyat oynaklığının derecesinin bir göstergesidir.
#  Her iki yöndeki güçlü hareketlere genellikle geniş aralıklar
#  veya geniş Gerçek Aralıklar eşlik eder.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class AverageTrueRange(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        close_shift = self._close.shift(1)
        true_range = self._true_range(self._high, self._low, close_shift)
        atr = np.zeros(len(self._close))
        atr[self._window - 1] = true_range[0: self._window].mean()
        for i in range(self._window, len(atr)):
            atr[i] = (atr[i - 1] * (self._window - 1)
             + true_range.iloc[i]) / float(self._window)
        self._atr = pd.Series(data=atr, index=true_range.index)

    def average_true_range(self) -> pd.Series:
        atr = self._check_fillna(self._atr, value=0)
        return pd.Series(atr, name="atr")
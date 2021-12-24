# VI (Vortex Indicator)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vortex_indicator

# Pozitif ve negatif trend hareketini yakalayan iki osilatörden oluşur.
#  Bir yükseliş sinyali, pozitif trend göstergesi negatif trend göstergesinin
#  veya bir temel seviyenin üzerine çıktığında tetiklenir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class VortexIndicator(IndicatorMixin):
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
        close_shift = self._close.shift(1, fill_value=self._close.mean())
        true_range = self._true_range(self._high, self._low, close_shift)
        min_periods = 0 if self._fillna else self._window
        trn = true_range.rolling(self._window, min_periods=min_periods).sum()
        vmp = np.abs(self._high - self._low.shift(1))
        vmm = np.abs(self._low - self._high.shift(1))
        self._vip = vmp.rolling(self._window, min_periods=min_periods).sum() / trn
        self._vin = vmm.rolling(self._window, min_periods=min_periods).sum() / trn

    # +VI
    def vortex_indicator_pos(self):
        vip = self._check_fillna(self._vip, value=1)
        return pd.Series(vip, name="vip")

    # -VI
    def vortex_indicator_neg(self):
        vin = self._check_fillna(self._vin, value=1)
        return pd.Series(vin, name="vin")

    # Diff VI
    def vortex_indicator_diff(self):
        vid = self._vip - self._vin
        vid = self._check_fillna(vid, value=0)
        return pd.Series(vid, name="vid")
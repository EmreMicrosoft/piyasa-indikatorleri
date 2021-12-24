# DPO (Detrended Price Oscillator)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

# Trendi fiyattan çıkarmak ve döngüleri tanımlamayı
#  kolaylaştırmak için tasarlanmış bir göstergedir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class DPOIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 20, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window
        self._dpo = (
            self._close.shift(
                int((0.5 * self._window) + 1), fill_value=self._close.mean()
            ) - self._close.rolling(self._window, min_periods=min_periods).mean())

    def dpo(self) -> pd.Series:
        dpo_series = self._check_fillna(self._dpo, value=0)
        return pd.Series(dpo_series, name="dpo_" + str(self._window))
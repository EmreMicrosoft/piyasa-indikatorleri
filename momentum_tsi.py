# TSI (True Strength Index)
# https://school.stockcharts.com/doku.php?id=technical_indicators:true_strength_index

# Hem trend yönünü hem de aşırı alım/satım koşullarını gösterir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window_slow(int): yüksek nokta.
#  window_fast(int): düşük nokta.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class TSIIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window_slow: int = 25,
        window_fast: int = 13,
        fillna: bool = False,
    ):
        self._close = close
        self._window_slow = window_slow
        self._window_fast = window_fast
        self._fillna = fillna
        self._run()

    def _run(self):
        diff_close = self._close - self._close.shift(1)
        min_periods_r = 0 if self._fillna else self._window_slow
        min_periods_s = 0 if self._fillna else self._window_fast
        smoothed = (
            diff_close.ewm(
                span=self._window_slow, min_periods=min_periods_r, adjust=False).mean()
            .ewm(span=self._window_fast, min_periods=min_periods_s, adjust=False).mean())
        smoothed_abs = (
            abs(diff_close)
            .ewm(span=self._window_slow, min_periods=min_periods_r, adjust=False).mean()
            .ewm(span=self._window_fast, min_periods=min_periods_s, adjust=False).mean())
        self._tsi = smoothed / smoothed_abs
        self._tsi *= 100

    def tsi(self) -> pd.Series:
        tsi_series = self._check_fillna(self._tsi, value=0)
        return pd.Series(tsi_series, name="tsi")
# FI (Force Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:force_index

# Gerçek alış veya satış baskısının ne kadar güçlü olduğunu gösterir.
#  Yüksek pozitif değerler, güçlü bir yükseliş eğilimi olduğu anlamına gelir
#  ve düşük değerler güçlü bir düşüş eğilimi anlamına gelir.

# Argümanlar:
#  close(pandas.Series):veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class ForceIndexIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        volume: pd.Series,
        window: int = 13,
        fillna: bool = False,
    ):
        self._close = close
        self._volume = volume
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        fi_series = (self._close - self._close.shift(1)) * self._volume
        self._fi = _ema(fi_series, self._window, fillna=self._fillna)

    def force_index(self) -> pd.Series:
        fi_series = self._check_fillna(self._fi, value=0)
        return pd.Series(fi_series, name=f"fi_{self._window}")
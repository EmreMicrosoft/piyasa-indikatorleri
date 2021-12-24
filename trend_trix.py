# TRIX (Trix)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix

# Üçlü üstel olarak düzleştirilmiş hareketli ortalamanın değişim yüzdesini gösterir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class TRIXIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 15, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        ema1 = _ema(self._close, self._window, self._fillna)
        ema2 = _ema(ema1, self._window, self._fillna)
        ema3 = _ema(ema2, self._window, self._fillna)
        self._trix = (ema3 - ema3.shift(1, fill_value=ema3.mean())) / ema3.shift(1, fill_value=ema3.mean())
        self._trix *= 100

    def trix(self) -> pd.Series:
        trix_series = self._check_fillna(self._trix, value=0)
        return pd.Series(trix_series, name=f"trix_{self._window}")
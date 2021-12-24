# MI (Mass Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index

# Aralık genişletmelerine dayalı olarak trend dönüşlerini belirlemek için
#  yüksek-düşük aralığını kullanır. Mevcut trendin tersine çevrilmesini
#  öngörebilecek aralık çıkıntılarını tanımlar.

# high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  window_fast(int): hızlı dönem değeri.
#  window_slow(int): yavaş dönem değeri.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class MassIndex(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        window_fast: int = 9,
        window_slow: int = 25,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._window_fast = window_fast
        self._window_slow = window_slow
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window_slow
        amplitude = self._high - self._low
        ema1 = _ema(amplitude, self._window_fast, self._fillna)
        ema2 = _ema(ema1, self._window_fast, self._fillna)
        mass = ema1 / ema2
        self._mass = mass.rolling(self._window_slow, min_periods=min_periods).sum()

    def mass_index(self) -> pd.Series:
        mass = self._check_fillna(self._mass, value=0)
        return pd.Series(mass, name=f"mass_index_{self._window_fast}_{self._window_slow}")
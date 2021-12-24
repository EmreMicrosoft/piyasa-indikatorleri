# UO (Ultimate Oscillator)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator

# Larry Williams'ın (1976) sinyali, üç farklı zaman diliminde
#  momentumu yakalamak için tasarlanmış bir momentum osilatörüdür.

# BP = Close - Minimum(Low or Prior Close)
# TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)
# Average7 = (7-period BP Sum) / (7-period TR Sum)
# Average14 = (14-period BP Sum) / (14-period TR Sum)
# Average28 = (28-period BP Sum) / (28-period TR Sum)
# UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window1(int): kısa dönem.
#  window2(int): orta nokta.
#  window3(int): uzun dönem.
#  weight1(float): UO için kısa BP ortalamasının ağırlığı.
#  weight2(float): UO için ortalama BP ortalamasının ağırlığı.
#  weight3(float): UO için uzun BP ortalamasının ağırlığı.
#  fillna(bool): True ise, nan değerlerini 50 ile doldur.


import pandas as pd
from _utilities import IndicatorMixin

class UltimateOscillator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window1: int = 7,
        window2: int = 14,
        window3: int = 28,
        weight1: float = 4.0,
        weight2: float = 2.0,
        weight3: float = 1.0,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window1 = window1
        self._window2 = window2
        self._window3 = window3
        self._weight1 = weight1
        self._weight2 = weight2
        self._weight3 = weight3
        self._fillna = fillna
        self._run()

    def _run(self):
        close_shift = self._close.shift(1)
        true_range = self._true_range(self._high, self._low, close_shift)
        buying_pressure = self._close - pd.DataFrame(
            {"low": self._low, "close": close_shift}
        ).min(axis=1, skipna=False)
        min_periods_s = 0 if self._fillna else self._window1
        min_periods_m = 0 if self._fillna else self._window2
        min_periods_len = 0 if self._fillna else self._window3
        avg_s = (
            buying_pressure.rolling(self._window1, min_periods=min_periods_s).sum()
            / true_range.rolling(self._window1, min_periods=min_periods_s).sum())
        avg_m = (
            buying_pressure.rolling(self._window2, min_periods=min_periods_m).sum()
            / true_range.rolling(self._window2, min_periods=min_periods_m).sum())
        avg_l = (
            buying_pressure.rolling(self._window3, min_periods=min_periods_len).sum()
            / true_range.rolling(self._window3, min_periods=min_periods_len).sum())
        self._uo = (
            100.0
            * (
                (self._weight1 * avg_s)
                + (self._weight2 * avg_m)
                + (self._weight3 * avg_l))
            / (self._weight1 + self._weight2 + self._weight3))

    def ultimate_oscillator(self) -> pd.Series:
        ultimate_osc = self._check_fillna(self._uo, value=50)
        return pd.Series(ultimate_osc, name="uo")
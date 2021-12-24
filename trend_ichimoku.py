# ICHIMOKU (Ichimoku Kinkō Hyō)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud

# TODO: description here

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  window1(int): n1 düşük dönem.
#  window2(int): n2 orta dönem.
#  window3(int): n3 yüksek dönem.
#  visual(bool): True ise, n2 değerlerini kaydır.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class IchimokuIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        window1: int = 9,
        window2: int = 26,
        window3: int = 52,
        visual: bool = False,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._window1 = window1
        self._window2 = window2
        self._window3 = window3
        self._visual = visual
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods_n1 = 0 if self._fillna else self._window1
        min_periods_n2 = 0 if self._fillna else self._window2
        self._conv = 0.5 * (
            self._high.rolling(self._window1, min_periods=min_periods_n1).max()
            + self._low.rolling(self._window1, min_periods=min_periods_n1).min())
        self._base = 0.5 * (
            self._high.rolling(self._window2, min_periods=min_periods_n2).max()
            + self._low.rolling(self._window2, min_periods=min_periods_n2).min())

    # Dönüşüm Çizgisi:
    def ichimoku_conversion_line(self) -> pd.Series:
        conversion = self._check_fillna(self._conv, value=-1)
        return pd.Series(conversion, name=f"ichimoku_conv_{self._window1}_{self._window2}")

    # Temel Çizgi:
    def ichimoku_base_line(self) -> pd.Series:
        base = self._check_fillna(self._base, value=-1)
        return pd.Series(base, name=f"ichimoku_base_{self._window1}_{self._window2}")

    # Öncül Açıklık - A:
    def ichimoku_a(self) -> pd.Series:
        spana = 0.5 * (self._conv + self._base)
        spana = (spana.shift(self._window2, fill_value=spana.mean()) if self._visual else spana)
        spana = self._check_fillna(spana, value=-1)
        return pd.Series(spana, name=f"ichimoku_a_{self._window1}_{self._window2}")

    # Öncül Açıklık - B:
    def ichimoku_b(self) -> pd.Series:
        spanb = 0.5 * (
            self._high.rolling(self._window3, min_periods=0).max()
            + self._low.rolling(self._window3, min_periods=0).min())
        spanb = (spanb.shift(self._window2, fill_value=spanb.mean()) if self._visual else spanb)
        spanb = self._check_fillna(spanb, value=-1)
        return pd.Series(spanb, name=f"ichimoku_b_{self._window1}_{self._window2}")
# CCI (Commodity Channel Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci

# Bir menkul kıymetin fiyat değişikliği ile ortalama fiyat değişikliği
#  arasındaki farkı ölçer. Yüksek pozitif okumalar, fiyatların ortalamalarının
#  oldukça üzerinde olduğunu ve bunun da bir güç gösterisi olduğunu gösterir.
#  Düşük negatif okumalar, fiyatların ortalamalarının oldukça altında olduğunu
#  ve bunun da bir zayıflık göstergesi olduğunu gösterir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  constant(int): sabit.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class CCIIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 20,
        constant: float = 0.015,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._constant = constant
        self._fillna = fillna
        self._run()

    def _run(self):
        def _mad(x):
            return np.mean(np.abs(x - np.mean(x)))

        min_periods = 0 if self._fillna else self._window
        typical_price = (self._high + self._low + self._close) / 3.0
        self._cci = (
            typical_price
            - typical_price.rolling(self._window, min_periods=min_periods).mean()
        ) / (
            self._constant
            * typical_price.rolling(self._window, min_periods=min_periods).apply(
                _mad, True
            )
        )

    def cci(self) -> pd.Series:
        cci_series = self._check_fillna(self._cci, value=0)
        return pd.Series(cci_series, name="cci")
# SO (Stochastic Oscillator)
# https://school.stockcharts.com/doku.php?id=technical_indicators:stochastic_oscillator_fast_slow_and_full

# 1950'lerin sonlarında George Lane tarafından geliştirildi.
#  Stokastik osilatör, bir hisse senedinin kapanış fiyatının konumunu,
#  bir hisse senedinin fiyatının yüksek ve düşük aralığına göre belirli
#  bir süre boyunca, tipik olarak 14 günlük bir süre boyunca sunar.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  window(int): n periyodu.
#  smooth_window(int): stoch_k üzerinden sma periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class StochasticOscillator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
        smooth_window: int = 3,
        fillna: bool = False,
    ):
        self._close = close
        self._high = high
        self._low = low
        self._window = window
        self._smooth_window = smooth_window
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window
        smin = self._low.rolling(self._window, min_periods=min_periods).min()
        smax = self._high.rolling(self._window, min_periods=min_periods).max()
        self._stoch_k = 100 * (self._close - smin) / (smax - smin)

    def stoch(self) -> pd.Series:
        stoch_k = self._check_fillna(self._stoch_k, value=50)
        return pd.Series(stoch_k, name="stoch_k")

    def stoch_signal(self) -> pd.Series:
        min_periods = 0 if self._fillna else self._smooth_window
        stoch_d = self._stoch_k.rolling(
            self._smooth_window, min_periods=min_periods).mean()
        stoch_d = self._check_fillna(stoch_d, value=50)
        return pd.Series(stoch_d, name="stoch_k_signal")
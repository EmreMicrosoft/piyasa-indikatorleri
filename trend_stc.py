# STC (Schaff Trend Cycle)
# https://www.investopedia.com/articles/forex/10/schaff-trend-cycle-indicator.asp

# Schaff Trend Döngüsü (STC), piyasa trendlerini belirlemek ve tüccarlara
#  alım ve satım sinyalleri sağlamak için yaygın olarak kullanılan bir
#  grafik göstergesidir. 1999 yılında ünlü döviz tüccarı Doug Schaff tarafından
#  geliştirilen STC, bir tür osilatördür ve zaman çerçevesinden bağımsız olarak
#  döviz trendlerinin döngüsel kalıplarda hızlanıp yavaşladığı varsayımına dayanır.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window_fast(int): n dönem kısa vadeli.
#  window_slow(int): n dönem uzun vadeli.
#  cycle(int): döngü boyutu.
#  smooth1(int): stoch_k üzerinden ema dönemi.
#  smooth2(int): stoch_kd üzerinden ema dönemi.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class STCIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window_slow: int = 50,
        window_fast: int = 23,
        cycle: int = 10,
        smooth1: int = 3,
        smooth2: int = 3,
        fillna: bool = False,
    ):
        self._close = close
        self._window_slow = window_slow
        self._window_fast = window_fast
        self._cycle = cycle
        self._smooth1 = smooth1
        self._smooth2 = smooth2
        self._fillna = fillna
        self._run()

    def _run(self):

        _emafast = _ema(self._close, self._window_fast, self._fillna)
        _emaslow = _ema(self._close, self._window_slow, self._fillna)
        _macd = _emafast - _emaslow

        _macdmin = _macd.rolling(window=self._cycle).min()
        _macdmax = _macd.rolling(window=self._cycle).max()
        _stoch_k = 100 * (_macd - _macdmin) / (_macdmax - _macdmin)
        _stoch_d = _ema(_stoch_k, self._smooth1, self._fillna)

        _stoch_d_min = _stoch_d.rolling(window=self._cycle).min()
        _stoch_d_max = _stoch_d.rolling(window=self._cycle).max()
        _stoch_kd = 100 * (_stoch_d - _stoch_d_min) / (_stoch_d_max - _stoch_d_min)
        self._stc = _ema(_stoch_kd, self._smooth2, self._fillna)

    def stc(self):
        stc_series = self._check_fillna(self._stc)
        return pd.Series(stc_series, name="stc")
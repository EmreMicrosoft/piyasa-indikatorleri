# PPO (Percentage Price Oscillator)
# https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo

# Yüzde Fiyat Osilatörü (PPO), iki hareketli ortalama arasındaki farkı
#  daha büyük hareketli ortalamanın yüzdesi olarak ölçen bir momentum osilatörüdür.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Fiyat' sütunu.
#  window_slow(int): n dönem uzun vadeli.
#  window_fast(int): n dönem kısa vadeli.
#  window_sign(int): sinyal için n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class PercentagePriceOscillator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window_slow: int = 26,
        window_fast: int = 12,
        window_sign: int = 9,
        fillna: bool = False,
    ):
        self._close = close
        self._window_slow = window_slow
        self._window_fast = window_fast
        self._window_sign = window_sign
        self._fillna = fillna
        self._run()

    def _run(self):
        _emafast = _ema(self._close, self._window_fast, self._fillna)
        _emaslow = _ema(self._close, self._window_slow, self._fillna)
        self._ppo = ((_emafast - _emaslow) / _emaslow) * 100
        self._ppo_signal = _ema(self._ppo, self._window_sign, self._fillna)
        self._ppo_hist = self._ppo - self._ppo_signal

    def ppo(self):
        ppo_series = self._check_fillna(self._ppo, value=0)
        return pd.Series(ppo_series, name=f"PPO_{self._window_fast}_{self._window_slow}")

    def ppo_signal(self):
        ppo_signal_series = self._check_fillna(self._ppo_signal, value=0)
        return pd.Series(ppo_signal_series, name=f"PPO_sign_{self._window_fast}_{self._window_slow}")

    def ppo_hist(self):
        ppo_hist_series = self._check_fillna(self._ppo_hist, value=0)
        return pd.Series(ppo_hist_series, name=f"PPO_hist_{self._window_fast}_{self._window_slow}")
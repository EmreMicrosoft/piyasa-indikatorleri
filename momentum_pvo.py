# PVO (Percentage Volume Oscillator)
# https://school.stockcharts.com/doku.php?id=technical_indicators:percentage_volume_oscillator_pvo

# Yüzde Hacim Osilatörü (PVO), hacim için bir momentum osilatörüdür.
#  PVO, daha büyük hareketli ortalamanın yüzdesi olarak hacim tabanlı
#  iki hareketli ortalama arasındaki farkı ölçer.

# Argümanlar:
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window_slow(int): n dönem uzun vadeli.
#  window_fast(int): n dönem kısa vadeli.
#  window_sign(int): sinyal için n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class PercentageVolumeOscillator(IndicatorMixin):
    def __init__(
        self,
        volume: pd.Series,
        window_slow: int = 26,
        window_fast: int = 12,
        window_sign: int = 9,
        fillna: bool = False,
    ):
        self._volume = volume
        self._window_slow = window_slow
        self._window_fast = window_fast
        self._window_sign = window_sign
        self._fillna = fillna
        self._run()

    def _run(self):
        _emafast = _ema(self._volume, self._window_fast, self._fillna)
        _emaslow = _ema(self._volume, self._window_slow, self._fillna)
        self._pvo = ((_emafast - _emaslow) / _emaslow) * 100
        self._pvo_signal = _ema(self._pvo, self._window_sign, self._fillna)
        self._pvo_hist = self._pvo - self._pvo_signal

    # PVO Line
    def pvo(self) -> pd.Series:
        pvo_series = self._check_fillna(self._pvo, value=0)
        return pd.Series(pvo_series, name=f"PVO_{self._window_fast}_{self._window_slow}")

    # Signal Line
    def pvo_signal(self) -> pd.Series:
        pvo_signal_series = self._check_fillna(self._pvo_signal, value=0)
        return pd.Series(pvo_signal_series, name=f"PVO_sign_{self._window_fast}_{self._window_slow}")

    # Histgram
    def pvo_hist(self) -> pd.Series:
        pvo_hist_series = self._check_fillna(self._pvo_hist, value=0)
        return pd.Series(pvo_hist_series, name=f"PVO_hist_{self._window_fast}_{self._window_slow}")
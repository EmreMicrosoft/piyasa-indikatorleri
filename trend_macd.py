# MACD (Moving Average Convergence Divergence)
# https://en.wikipedia.org/wiki/MACD
# https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_convergence_divergence_macd
 
# Hareketli Ortalama Yaklaşma/Uzaklaşma, üstel hareketli ortalamaya (EMA)
#  odaklanır. İki hareketli ortalama fiyat arasındaki ilişkiyi gösteren,
#  trend izleyen bir momentum göstergesidir.

# Hesaplamak için şunları kullanırız:

# MACD = EMA(n1, close) — EMA(n2, close)
# MACD_Signal = EMA(n3, MACD)
# MACD_Difference = MACD — MACD_Signal

# Değişkenler için tipik değerler n1=12, n2=26 ve n3=9'dur, ancak ticaret tarzınıza
#  ve hedeflerinize bağlı olarak kütüphanede başka değerler değiştirilebilir.

# Teori, MACD eğrisi (mavi) MACD_Signal'den (turuncu) küçük olduğunda veya
#  MACD farkı (MACD_Signal ve MACD eğrisi arasındaki farkı temsil eden yeşil eğri)
#  0'dan düşük bir değere sahip olduğunda, fiyat eğiliminin (düşüş) olacağını söyler.
#  Aksi ise fiyat artışını gösterir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window_fast(int): n dönem kısa vadeli.
#  window_slow(int): n dönem uzun vadeli.
#  window_sign(int): sinyal için n nokta.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin, _ema

class MACDIndicator(IndicatorMixin):
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
        self._emafast = _ema(self._close, self._window_fast, self._fillna)
        self._emaslow = _ema(self._close, self._window_slow, self._fillna)
        self._macd = self._emafast - self._emaslow
        self._macd_signal = _ema(self._macd, self._window_sign, self._fillna)
        self._macd_diff = self._macd - self._macd_signal

    # MAXD Hattı:
    def macd(self) -> pd.Series:
        macd_series = self._check_fillna(self._macd, value=0)
        return pd.Series(macd_series, name=f"MACD_{self._window_fast}_{self._window_slow}")

    # Sinyal Hattı:
    def macd_signal(self) -> pd.Series:
        macd_signal_series = self._check_fillna(self._macd_signal, value=0)
        return pd.Series(macd_signal_series, name=f"MACD_sign_{self._window_fast}_{self._window_slow}")

    # MACD Histogramı: MACD ve MACD Sinyali arasındaki ilişkiyi gösterir.
    def macd_diff(self) -> pd.Series:
        macd_diff_series = self._check_fillna(self._macd_diff, value=0)
        return pd.Series(macd_diff_series, name=f"MACD_diff_{self._window_fast}_{self._window_slow}")
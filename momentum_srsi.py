# SRSI (Stochastic Relative Strength Index)
# https://school.stockcharts.com/doku.php?id=technical_indicators:stochrsi
# https://www.investopedia.com/terms/s/stochrsi.asp

# StochRSI osilatörü, genelleştirilmiş bir fiyat değişikliği analizinden ziyade
#  belirli bir menkul kıymetin tarihsel performansına uyumlu daha hassas bir gösterge
#  oluşturmak için her iki momentum göstergesinden de yararlanmak üzere geliştirilmiştir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  smooth1(int): Stokastik RSI'nin hareketli ortalaması.
#  smooth2(int): hareketli ortalama %K
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin
from momentum_rsi import RSIIndicator

class StochRSIIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window: int = 14,
        smooth1: int = 3,
        smooth2: int = 3,
        fillna: bool = False,
    ):
        self._close = close
        self._window = window
        self._smooth1 = smooth1
        self._smooth2 = smooth2
        self._fillna = fillna
        self._run()

    def _run(self):
        self._rsi = RSIIndicator(
            close=self._close, window=self._window, fillna=self._fillna).rsi()
        lowest_low_rsi = self._rsi.rolling(self._window).min()
        self._stochrsi = (self._rsi - lowest_low_rsi) / (
            self._rsi.rolling(self._window).max() - lowest_low_rsi)
        self._stochrsi_k = self._stochrsi.rolling(self._smooth1).mean()

    def stochrsi(self):
        stochrsi_series = self._check_fillna(self._stochrsi)
        return pd.Series(stochrsi_series, name="stochrsi")

    def stochrsi_k(self):
        stochrsi_k_series = self._check_fillna(self._stochrsi_k)
        return pd.Series(stochrsi_k_series, name="stochrsi_k")

    def stochrsi_d(self):
        stochrsi_d_series = self._stochrsi_k.rolling(self._smooth2).mean()
        stochrsi_d_series = self._check_fillna(stochrsi_d_series)
        return pd.Series(stochrsi_d_series, name="stochrsi_d")
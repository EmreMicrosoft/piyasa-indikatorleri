# AO (Awesome Oscillator)
# https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)

# AO, piyasa momentumunu ölçmek için kullanılan bir göstergedir.
#  AO, 34 Periyot ve 5 Periyot Basit Hareketli Ortalama'nın (SMA)
#  farkını hesaplar. Kullanılan Basit Hareketli Ortalamalar, kapanış
#  fiyatı kullanılarak değil, her bir çubuğun orta noktaları
#  kullanılarak hesaplanır. AO genellikle eğilimleri doğrulamak
#  veya olası geri dönüşleri tahmin etmek için kullanılır.

# AO, çubukların (H+L)/2 merkez noktalarından çizilen ve çubukların
#  merkezi noktaları boyunca grafiği çizilen 5 periyotlu Basit Hareketli
#  Ortalama'dan (SMA) çıkarılan 34 periyotlu basit bir hareketli ortalamadır.

# MEDIAN PRICE = (HIGH+LOW)/2
# AO = SMA(MEDIAN PRICE, 5)-SMA(MEDIAN PRICE, 34)
#  where
#  SMA — Simple Moving Average.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  window1(int): kısa dönem.
#  window2(int): uzun dönem.
#  fillna(bool): True ise, nan değerlerini -50 ile doldur.


import pandas as pd
from _utilities import IndicatorMixin

class AwesomeOscillatorIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        window1: int = 5,
        window2: int = 34,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._window1 = window1
        self._window2 = window2
        self._fillna = fillna
        self._run()

    def _run(self):
        median_price = 0.5 * (self._high + self._low)
        min_periods_s = 0 if self._fillna else self._window1
        min_periods_len = 0 if self._fillna else self._window2
        self._ao = (
            median_price.rolling(self._window1, min_periods=min_periods_s).mean()
            - median_price.rolling(self._window2, min_periods=min_periods_len).mean()
        )

    def awesome_oscillator(self) -> pd.Series:
        ao_series = self._check_fillna(self._ao, value=0)
        return pd.Series(ao_series, name="ao")
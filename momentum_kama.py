# KAMA (Kaufman's Adaptive Moving Average)
# https://www.tradingview.com/ideas/kama/

# Kaufman'ın Uyarlanabilir Hareketli Ortalaması (KAMA)
#  Piyasa gürültüsünü veya oynaklığını hesaba katmak için tasarlanmış hareketli ortalama.
#  KAMA, fiyat dalgalanmalarının nispeten küçük olduğu ve gürültünün düşük olduğu durumlarda
#  fiyatları yakından takip edecektir. KAMA, fiyat dalgalanmaları genişlediğinde buna uyum
#  sağlayacak ve fiyatları daha uzak bir mesafeden takip edecektir. Bu trend izleyen gösterge,
#  genel trendi, zaman dönüm noktalarını ve filtre fiyat hareketlerini belirlemek için kullanılabilir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  pow1(int): en hızlı EMA sabiti için dönem sayısı.
#  pow2(int): en yavaş EMA sabiti için dönem sayısı.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class KAMAIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window: int = 10,
        pow1: int = 2,
        pow2: int = 30,
        fillna: bool = False,
    ):
        self._close = close
        self._window = window
        self._pow1 = pow1
        self._pow2 = pow2
        self._fillna = fillna
        self._run()

    def _run(self):
        close_values = self._close.values
        vol = pd.Series(abs(self._close - np.roll(self._close, 1)))

        min_periods = 0 if self._fillna else self._window
        er_num = abs(close_values - np.roll(close_values, self._window))
        er_den = vol.rolling(self._window, min_periods=min_periods).sum()
        efficiency_ratio = er_num / er_den

        smoothing_constant = (
            (
                efficiency_ratio * (2.0 / (self._pow1 + 1) - 2.0 / (self._pow2 + 1.0))
                + 2 / (self._pow2 + 1.0)
            )
            ** 2.0
        ).values

        self._kama = np.zeros(smoothing_constant.size)
        len_kama = len(self._kama)
        first_value = True

        for i in range(len_kama):
            if np.isnan(smoothing_constant[i]):
                self._kama[i] = np.nan
            elif first_value:
                self._kama[i] = close_values[i]
                first_value = False
            else:
                self._kama[i] = self._kama[i - 1] + smoothing_constant[i] * (
                    close_values[i] - self._kama[i - 1])

    def kama(self) -> pd.Series:
        kama_series = pd.Series(self._kama, index=self._close.index)
        kama_series = self._check_fillna(kama_series, value=self._close)
        return pd.Series(kama_series, name="kama")
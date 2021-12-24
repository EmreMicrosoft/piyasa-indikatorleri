# MFI (Money Flow Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi

# Alış ve satış baskısını ölçmek için hem fiyatı hem de hacmi kullanır.
#  Tipik fiyat yükseldiğinde (alış baskısı) pozitif, tipik fiyat
#  düştüğünde (satış baskısı) negatiftir. Daha sonra, sıfır ile yüz
#  arasında hareket eden bir osilatör oluşturmak için bir RSI formülüne
#  pozitif ve negatif para akışı oranı eklenir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class MFIIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series,
        window: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        typical_price = (self._high + self._low + self._close) / 3.0
        up_down = np.where(
            typical_price > typical_price.shift(1), 1,
            np.where(typical_price < typical_price.shift(1), -1, 0))
        mfr = typical_price * self._volume * up_down

        # n periyodundaki artı/eksi para akışı:
        min_periods = 0 if self._fillna else self._window
        n_positive_mf = mfr.rolling(self._window, min_periods=min_periods).apply(
            lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True)
        n_negative_mf = abs(
            mfr.rolling(self._window, min_periods=min_periods).apply(
                lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True))

        # n_positive_mf = np.where(mf.rolling(self._window).sum() >= 0.0, mf, 0.0)
        # n_negative_mf = abs(np.where(mf.rolling(self._window).sum() < 0.0, mf, 0.0))

        # Money Flow Index
        mfi = n_positive_mf / n_negative_mf
        self._mfi = 100 - (100 / (1 + mfi))

    def money_flow_index(self) -> pd.Series:
        mfi = self._check_fillna(self._mfi, value=50)
        return pd.Series(mfi, name=f"mfi_{self._window}")
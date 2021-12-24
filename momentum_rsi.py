# RSI (Relative Strength Index)
# https://www.investopedia.com/terms/r/rsi.asp

# Bir menkul kıymetin fiyat hareketlerinin hızını ve değişimini ölçmek
#  için belirli bir zaman aralığındaki son kazanç ve kayıpların büyüklüğünü
#  karşılaştırır. Öncelikle bir varlığın ticaretinde aşırı alım veya aşırı
#  satım koşullarını belirlemeye çalışmak için kullanılır.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n süreci.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class RSIIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 14, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        diff = self._close.diff(1)
        up_direction = diff.where(diff > 0, 0.0)
        down_direction = -diff.where(diff < 0, 0.0)
        min_periods = 0 if self._fillna else self._window
        emaup = up_direction.ewm(
            alpha=1 / self._window, min_periods=min_periods, adjust=False).mean()
        emadn = down_direction.ewm(
            alpha=1 / self._window, min_periods=min_periods, adjust=False).mean()
        relative_strength = emaup / emadn
        self._rsi = pd.Series(
            np.where(emadn == 0, 100, 100 - (100 / (1 + relative_strength))),
            index=self._close.index)

    def rsi(self) -> pd.Series:
        rsi_series = self._check_fillna(self._rsi, value=50)
        return pd.Series(rsi_series, name="rsi")
# BB (The Bollinger Bands)
# https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands

# Bollinger Bantları, belirli bir zaman diliminde 
#  bir varlığın fiyatının oynaklığını analiz etmek için kullanılır.
#  3 bant vardır: Orta Bant (MB) son n dönemdeki fiyatın ortalamasıdır,
#  Üst (UB) ve Alt Bantlar (LB) orta banta eşittir, ancak standart sapmanın
#  x katı eklenip çıkarılır. 

# Kullanılan normal parametreler n = 20 periyot ve x = 2'dir.

# MB = SUM(n last close values) / n
# UB = MB + (X * StdDev)
# LB = MB — (X * StdDev)

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  window_dev(int): n faktör standart sapma
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class BollingerBands(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        window: int = 20,
        window_dev: int = 2,
        fillna: bool = False,
    ):
        self._close = close
        self._window = window
        self._window_dev = window_dev
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._window
        self._mavg = self._close.rolling(self._window, min_periods=min_periods).mean()
        self._mstd = self._close.rolling(self._window, min_periods=min_periods).std(ddof=0)
        self._hband = self._mavg + self._window_dev * self._mstd
        self._lband = self._mavg - self._window_dev * self._mstd

    # Orta Band:
    def bollinger_mavg(self) -> pd.Series:
        mavg = self._check_fillna(self._mavg, value=-1)
        return pd.Series(mavg, name="mavg")

    # Yüksek Band:
    def bollinger_hband(self) -> pd.Series:
        hband = self._check_fillna(self._hband, value=-1)
        return pd.Series(hband, name="hband")

    # Düşük Band:
    def bollinger_lband(self) -> pd.Series:
        lband = self._check_fillna(self._lband, value=-1)
        return pd.Series(lband, name="lband")

    # Band Genişliği: https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_band_width
    def bollinger_wband(self) -> pd.Series:
        wband = ((self._hband - self._lband) / self._mavg) * 100
        wband = self._check_fillna(wband, value=0)
        return pd.Series(wband, name="bbiwband")

    # Yüzde Bandı: https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_band_perce
    def bollinger_pband(self) -> pd.Series:
        pband = (self._close - self._lband) / (self._hband - self._lband)
        pband = self._check_fillna(pband, value=0)
        return pd.Series(pband, name="bbipband")

    # Bollinger Kanal Göstergesi Geçiş Yüksek Bandı (ikili):
    def bollinger_hband_indicator(self) -> pd.Series:
        hband = pd.Series(np.where(self._close > self._hband, 1.0, 0.0),
         index=self._close.index)
        hband = self._check_fillna(hband, value=0)
        return pd.Series(hband, index=self._close.index, name="bbihband")

    # Bollinger Kanal Göstergesi Geçiş Düşük Bandı (ikili):
    def bollinger_lband_indicator(self) -> pd.Series:
        lband = pd.Series(np.where(self._close < self._lband, 1.0, 0.0),
         index=self._close.index)
        lband = self._check_fillna(lband, value=0)
        return pd.Series(lband, name="bbilband")
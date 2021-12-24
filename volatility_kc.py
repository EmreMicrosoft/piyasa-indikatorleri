# KC (Keltner Channel)
# https://school.stockcharts.com/doku.php?id=technical_indicators:keltner_channels

# Keltner Kanalları, kanal kırılmaları ve kanal yönü ile geri dönüşleri
#  belirlemek için kullanılan bir trend takip göstergesidir.
#  Kanallar aynı zamanda trend düz olduğunda aşırı alım ve aşırı satım
#  seviyelerini belirlemek için de kullanılabilir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  window_atr(int): n atr periyodu. Yalnızca orijinal_sürüm parametresi False ise geçerlidir.
#  fillna(bool): True ise, nan değerlerini doldur.
#  orijinal_versiyon(bool): Doğruysa, merkez çizgisi olarak orijinal sürümü
#                           kullan (tipik fiyatın SMA'sı). False ise, merkez
#                           çizgisi olarak yakının EMA'sını kullan.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin
from volatility_atr import AverageTrueRange

class KeltnerChannel(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 20,
        window_atr: int = 10,
        fillna: bool = False,
        original_version: bool = True,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._window_atr = window_atr
        self._fillna = fillna
        self._original_version = original_version
        self._run()

    def _run(self):
        min_periods = 1 if self._fillna else self._window
        if self._original_version:
            self._tp = (
                ((self._high + self._low + self._close) / 3.0)
                .rolling(self._window, min_periods=min_periods)
                .mean()
            )
            self._tp_high = (
                (((4 * self._high) - (2 * self._low) + self._close) / 3.0)
                .rolling(self._window, min_periods=0)
                .mean()
            )
            self._tp_low = (
                (((-2 * self._high) + (4 * self._low) + self._close) / 3.0)
                .rolling(self._window, min_periods=0)
                .mean()
            )
        else:
            self._tp = self._close.ewm(
                span=self._window, min_periods=min_periods, adjust=False
            ).mean()
            atr = AverageTrueRange(
                close=self._close,
                high=self._high,
                low=self._low,
                window=self._window_atr,
                fillna=self._fillna,
            ).average_true_range()
            self._tp_high = self._tp + (2 * atr)
            self._tp_low = self._tp - (2 * atr)

    # Orta Band:
    def keltner_channel_mband(self) -> pd.Series:
        tp_middle = self._check_fillna(self._tp, value=-1)
        return pd.Series(tp_middle, name="mavg")

    # Yüksek Band:
    def keltner_channel_hband(self) -> pd.Series:
        tp_high = self._check_fillna(self._tp_high, value=-1)
        return pd.Series(tp_high, name="kc_hband")

    # Düşük Band:
    def keltner_channel_lband(self) -> pd.Series:
        tp_low = self._check_fillna(self._tp_low, value=-1)
        return pd.Series(tp_low, name="kc_lband")

    # Band Genişliği:
    def keltner_channel_wband(self) -> pd.Series:
        wband = ((self._tp_high - self._tp_low) / self._tp) * 100
        wband = self._check_fillna(wband, value=0)
        return pd.Series(wband, name="bbiwband")

    # Yüzde Bandı:
    def keltner_channel_pband(self) -> pd.Series:
        pband = (self._close - self._tp_low) / (self._tp_high - self._tp_low)
        pband = self._check_fillna(pband, value=0)
        return pd.Series(pband, name="bbipband")

    # Keltner Kanalı Göstergesi Geçiş Yüksek Bandı:
    def keltner_channel_hband_indicator(self) -> pd.Series:
        hband = pd.Series(np.where(self._close > self._tp_high, 1.0, 0.0), index=self._close.index)
        hband = self._check_fillna(hband, value=0)
        return pd.Series(hband, name="dcihband")

    # Keltner Kanalı Göstergesi Geçiş Düşük Bandı:
    def keltner_channel_lband_indicator(self) -> pd.Series:
        lband = pd.Series(np.where(self._close < self._tp_low, 1.0, 0.0), index=self._close.index)
        lband = self._check_fillna(lband, value=0)
        return pd.Series(lband, name="dcilband")
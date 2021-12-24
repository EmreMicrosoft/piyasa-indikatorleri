# VWAP (Volume Weighted Average Price)
# https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday

# VWAP, geçerli gün için toplam işlem hacmine bölünen tüm işlem
#  dönemlerinin dolar değerine eşittir. Hesaplama, ticaret açıldığında
#  başlar ve kapandığında sona erer. Sadece cari işlem günü için iyi
#  olduğu için hesaplamada gün içi periyotlar ve veriler kullanılır.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class VolumeWeightedAveragePrice(IndicatorMixin):
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
        # 1 - tipik fiyat:
        typical_price = (self._high + self._low + self._close) / 3.0

        # 2 - tipik fiyat * hacim:
        typical_price_volume = typical_price * self._volume

        # 3 - yekün * hacim
        min_periods = 0 if self._fillna else self._window
        total_pv = typical_price_volume.rolling(
            self._window, min_periods=min_periods).sum()

        # 4 - toplam hacim:
        total_volume = self._volume.rolling(self._window, min_periods=min_periods).sum()

        self.vwap = total_pv / total_volume

    def volume_weighted_average_price(self) -> pd.Series:
        vwap = self._check_fillna(self.vwap)
        return pd.Series(vwap, name=f"vwap_{self._window}")
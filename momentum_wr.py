# WR (Williams %R)
# https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r

# Larry Williams tarafından geliştirilen Williams %R, Hızlı Stokastik Osilatör'ün
#  tersi olan bir momentum göstergesidir. %R olarak da anılan Williams %R,
#  geriye bakma dönemi için yakının en yüksek seviyesine göre seviyesini yansıtır.
#  Buna karşılık, Stokastik Osilatör, yakının en düşük seviyeye göre seviyesini
#  yansıtır. %R, ham değeri -100 ile çarparak ters çevirmeyi düzeltir. Sonuç olarak,
#  Hızlı Stokastik Osilatör ve Williams %R tamamen aynı çizgileri üretir, sadece
#  ölçekleme farklıdır.

# Williams %R, 0'dan -100'e salınır. Gösterge 0'dan -20'ye kadar okumalar
#  ürettiğinde, bu aşırı alım piyasa koşullarını gösterir. Okumalar -80 ile -100
#  arasında olduğunda, aşırı satım piyasa koşullarını gösterir.
#  Şaşırtıcı olmayan bir şekilde, Stokastik Osilatörden türetilen sinyaller
#  Williams %R için de geçerlidir.

# %R = (Highest High - Close)/(Highest High - Lowest Low) * -100
#  Lowest Low = geriye dönük inceleme dönemi için en düşük en düşük.
#  Highest High = geriye dönük inceleme dönemi için en yüksek en yüksek.
#  %R, -100 ile çarpılır. (ters çevirmeyi düzelt ve ondalık basamağı hareket ettir)

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  lbp(int): yeniden inceleme süresi.
#  fillna(bool): True ise, nan değerlerini -50 ile doldur.


import pandas as pd
from _utilities import IndicatorMixin

class WilliamsRIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        lbp: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._lbp = lbp
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods = 0 if self._fillna else self._lbp
        highest_high = self._high.rolling(
            self._lbp, min_periods=min_periods
        ).max()  # highest high over lookback period lbp

        lowest_low = self._low.rolling(
            self._lbp, min_periods=min_periods
        ).min()  # lowest low over lookback period lbp

        self._wr = -100 * (highest_high - self._close) / (highest_high - lowest_low)

    def williams_r(self) -> pd.Series:
        wr_series = self._check_fillna(self._wr, value=-50)
        return pd.Series(wr_series, name="wr")
# DC (Donchian Channel)
# https://www.investopedia.com/terms/d/donchianchannels.asp

# Alt bant, n dönemi için en düşük fiyatı belirtir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class DonchianChannel(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 20,
        offset: int = 0,
        fillna: bool = False,
    ):
        self._offset = offset
        self._close = close
        self._high = high
        self._low = low
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        self._min_periods = 1 if self._fillna else self._window
        self._hband = self._high.rolling(
            self._window, min_periods=self._min_periods
        ).max()
        self._lband = self._low.rolling(
            self._window, min_periods=self._min_periods
        ).min()

    # YÜSKSEK BAND:
    def donchian_channel_hband(self) -> pd.Series:
        hband = self._check_fillna(self._hband, value=-1)
        if self._offset != 0:
            hband = hband.shift(self._offset)
        return pd.Series(hband, name="dchband")

    # DÜŞÜK BAND:
    def donchian_channel_lband(self) -> pd.Series:
        lband = self._check_fillna(self._lband, value=-1)
        if self._offset != 0:
            lband = lband.shift(self._offset)
        return pd.Series(lband, name="dclband")

    # ORTA BAND:
    def donchian_channel_mband(self) -> pd.Series:
        mband = ((self._hband - self._lband) / 2.0) + self._lband
        mband = self._check_fillna(mband, value=-1)
        if self._offset != 0:
            mband = mband.shift(self._offset)
        return pd.Series(mband, name="dcmband")

    # BAND GENİŞLİĞİ:
    def donchian_channel_wband(self) -> pd.Series:
        mavg = self._close.rolling(self._window, min_periods=self._min_periods).mean()
        wband = ((self._hband - self._lband) / mavg) * 100
        wband = self._check_fillna(wband, value=0)
        if self._offset != 0:
            wband = wband.shift(self._offset)
        return pd.Series(wband, name="dcwband")

    # YÜZDE BANDI:
    def donchian_channel_pband(self) -> pd.Series:
        pband = (self._close - self._lband) / (self._hband - self._lband)
        pband = self._check_fillna(pband, value=0)
        if self._offset != 0:
            pband = pband.shift(self._offset)
        return pd.Series(pband, name="dcpband")
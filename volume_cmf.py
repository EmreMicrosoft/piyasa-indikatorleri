# CMF (Chaikin Money Flow)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf

# Belirli bir dönemdeki Para Akışı Hacmi miktarını ölçer.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class ChaikinMoneyFlowIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series,
        window: int = 20,
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
        mfv = ((self._close - self._low) - (self._high - self._close)) / (self._high - self._low)
        mfv = mfv.fillna(0.0)  # float division by zero
        mfv *= self._volume
        min_periods = 0 if self._fillna else self._window
        self._cmf = (mfv.rolling(self._window, min_periods=min_periods).sum()
            / self._volume.rolling(self._window, min_periods=min_periods).sum())

    def chaikin_money_flow(self) -> pd.Series:
        cmf = self._check_fillna(self._cmf, value=0)
        return pd.Series(cmf, name="cmf")
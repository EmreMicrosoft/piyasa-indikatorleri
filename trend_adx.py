# ADX (Average Directional Movement Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx

# Artı Yön Göstergesi (+DI) ve Eksi Yön Göstergesi (-DI), bu farklılıkların
#  düzleştirilmiş ortalamalarından türetilir ve zaman içindeki eğilim yönünü ölçer.
#  Bu iki göstergeye genellikle toplu olarak Yönlü Hareket Göstergesi (DMI) denir.

# Ortalama Yön Endeksi (ADX), +DI ve -DI arasındaki farkın düzleştirilmiş
#  ortalamalarından türetilir ve zaman içindeki eğilimin (yönden bağımsız olarak) gücünü ölçer.

# Bu üç göstergeyi birlikte kullanarak, grafik uzmanları trendin hem yönünü hem de gücünü belirleyebilir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin, _get_min_max

class ADXIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        if self._window == 0:
            raise ValueError("window may not be 0")

        close_shift = self._close.shift(1)
        pdm = _get_min_max(self._high, close_shift, "max")
        pdn = _get_min_max(self._low, close_shift, "min")
        diff_directional_movement = pdm - pdn

        self._trs_initial = np.zeros(self._window - 1)
        self._trs = np.zeros(len(self._close) - (self._window - 1))
        self._trs[0] = diff_directional_movement.dropna()[0 : self._window].sum()
        diff_directional_movement = diff_directional_movement.reset_index(drop=True)

        for i in range(1, len(self._trs) - 1):
            self._trs[i] = (
                self._trs[i - 1]
                - (self._trs[i - 1] / float(self._window))
                + diff_directional_movement[self._window + i]
            )

        diff_up = self._high - self._high.shift(1)
        diff_down = self._low.shift(1) - self._low
        pos = abs(((diff_up > diff_down) & (diff_up > 0)) * diff_up)
        neg = abs(((diff_down > diff_up) & (diff_down > 0)) * diff_down)

        self._dip = np.zeros(len(self._close) - (self._window - 1))
        self._dip[0] = pos.dropna()[0 : self._window].sum()

        pos = pos.reset_index(drop=True)

        for i in range(1, len(self._dip) - 1):
            self._dip[i] = (
                self._dip[i - 1]
                - (self._dip[i - 1] / float(self._window))
                + pos[self._window + i])

        self._din = np.zeros(len(self._close) - (self._window - 1))
        self._din[0] = neg.dropna()[0 : self._window].sum()

        neg = neg.reset_index(drop=True)

        for i in range(1, len(self._din) - 1):
            self._din[i] = (
                self._din[i - 1]
                - (self._din[i - 1] / float(self._window))
                + neg[self._window + i])

    # Ortalama Yön İndeksi:
    def adx(self) -> pd.Series:
        dip = np.zeros(len(self._trs))

        for idx, value in enumerate(self._trs):
            dip[idx] = 100 * (self._dip[idx] / value)

        din = np.zeros(len(self._trs))

        for idx, value in enumerate(self._trs):
            din[idx] = 100 * (self._din[idx] / value)

        directional_index = 100 * np.abs((dip - din) / (dip + din))

        adx_series = np.zeros(len(self._trs))
        adx_series[self._window] = directional_index[0 : self._window].mean()

        for i in range(self._window + 1, len(adx_series)):
            adx_series[i] = (
                (adx_series[i - 1] * (self._window - 1)) + directional_index[i - 1]
            ) / float(self._window)

        adx_series = np.concatenate((self._trs_initial, adx_series), axis=0)
        adx_series = pd.Series(data=adx_series, index=self._close.index)

        adx_series = self._check_fillna(adx_series, value=20)
        return pd.Series(adx_series, name="adx")

    # Artı Yön Göstergesi:
    def adx_pos(self) -> pd.Series:
        dip = np.zeros(len(self._close))
        for i in range(1, len(self._trs) - 1):
            dip[i + self._window] = 100 * (self._dip[i] / self._trs[i])

        adx_pos_series = self._check_fillna(
            pd.Series(dip, index=self._close.index), value=20)
        return pd.Series(adx_pos_series, name="adx_pos")

    # Eksi Yön Göstergesi:
    def adx_neg(self) -> pd.Series:
        din = np.zeros(len(self._close))
        for i in range(1, len(self._trs) - 1):
            din[i + self._window] = 100 * (self._din[i] / self._trs[i])

        adx_neg_series = self._check_fillna(
            pd.Series(din, index=self._close.index), value=20)
        return pd.Series(adx_neg_series, name="adx_neg")
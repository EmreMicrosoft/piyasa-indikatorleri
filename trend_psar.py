# Parabolic SAR (Parabolic Stop And Reverse)
# https://school.stockcharts.com/doku.php?id=technical_indicators:parabolic_sar

# Daha yaygın olarak Parabolik SAR olarak bilinen Parabolik Durdurma ve Geri Alma,
#  J. Welles Wilder tarafından geliştirilen trend izleyen bir göstergedir.
#  Parabolik SAR, yükseliş trendinde fiyat çubuklarının altında ve düşüş trendinde
#  fiyat çubuklarının üzerinde tek bir parabolik çizgi (veya noktalar) olarak görüntülenir.

# Argümanlar:
#  high(pandas.Series): veri kümesi 'Yüksek' sütunu.
#  low(pandas.Series): veri kümesi 'Düşük' sütunu.
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  step(float): SAR'ı hesaplamak için kullanılan Hızlanma Faktörü.
#  max_step(float): Hızlanma Faktörü için izin verilen maksimum değer.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class PSARIndicator(IndicatorMixin):
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        step: float = 0.02,
        max_step: float = 0.20,
        fillna: bool = False,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._step = step
        self._max_step = max_step
        self._fillna = fillna
        self._run()

    def _run(self):
        up_trend = True
        acceleration_factor = self._step
        up_trend_high = self._high.iloc[0]
        down_trend_low = self._low.iloc[0]

        self._psar = self._close.copy()
        self._psar_up = pd.Series(index=self._psar.index)
        self._psar_down = pd.Series(index=self._psar.index)

        for i in range(2, len(self._close)):
            reversal = False

            max_high = self._high.iloc[i]
            min_low = self._low.iloc[i]

            if up_trend:
                self._psar.iloc[i] = self._psar.iloc[i - 1] + (
                    acceleration_factor * (up_trend_high - self._psar.iloc[i - 1])
                )

                if min_low < self._psar.iloc[i]:
                    reversal = True
                    self._psar.iloc[i] = up_trend_high
                    down_trend_low = min_low
                    acceleration_factor = self._step
                else:
                    if max_high > up_trend_high:
                        up_trend_high = max_high
                        acceleration_factor = min(
                            acceleration_factor + self._step, self._max_step
                        )

                    low1 = self._low.iloc[i - 1]
                    low2 = self._low.iloc[i - 2]
                    if low2 < self._psar.iloc[i]:
                        self._psar.iloc[i] = low2
                    elif low1 < self._psar.iloc[i]:
                        self._psar.iloc[i] = low1
            else:
                self._psar.iloc[i] = self._psar.iloc[i - 1] - (
                    acceleration_factor * (self._psar.iloc[i - 1] - down_trend_low)
                )

                if max_high > self._psar.iloc[i]:
                    reversal = True
                    self._psar.iloc[i] = down_trend_low
                    up_trend_high = max_high
                    acceleration_factor = self._step
                else:
                    if min_low < down_trend_low:
                        down_trend_low = min_low
                        acceleration_factor = min(
                            acceleration_factor + self._step, self._max_step
                        )

                    high1 = self._high.iloc[i - 1]
                    high2 = self._high.iloc[i - 2]
                    if high2 > self._psar.iloc[i]:
                        self._psar[i] = high2
                    elif high1 > self._psar.iloc[i]:
                        self._psar.iloc[i] = high1

            up_trend = up_trend != reversal  # XOR

            if up_trend:
                self._psar_up.iloc[i] = self._psar.iloc[i]
            else:
                self._psar_down.iloc[i] = self._psar.iloc[i]

    # PSAR Değeri:
    def psar(self) -> pd.Series:
        psar_series = self._check_fillna(self._psar, value=-1)
        return pd.Series(psar_series, name="psar")

    # PSAR Yukarı Trend Değeri:
    def psar_up(self) -> pd.Series:
        psar_up_series = self._check_fillna(self._psar_up, value=-1)
        return pd.Series(psar_up_series, name="psarup")

    # PSAR Aşağı Trend Değeri:
    def psar_down(self) -> pd.Series:
        psar_down_series = self._check_fillna(self._psar_down, value=-1)
        return pd.Series(psar_down_series, name="psardown")

    # PSAR Yukarı Trend Değeri Göstergesi:
    def psar_up_indicator(self) -> pd.Series:
        indicator = self._psar_up.where(
            self._psar_up.notnull() & self._psar_up.shift(1).isnull(), 0)
        indicator = indicator.where(indicator == 0, 1)
        return pd.Series(indicator, index=self._close.index, name="psariup")

    # PSAR Aşağı Trend Değeri Göstergesi:
    def psar_down_indicator(self) -> pd.Series:
        indicator = self._psar_up.where(
            self._psar_down.notnull() & self._psar_down.shift(1).isnull(), 0)
        indicator = indicator.where(indicator == 0, 1)
        return pd.Series(indicator, index=self._close.index, name="psaridown")
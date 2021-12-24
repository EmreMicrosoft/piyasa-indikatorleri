# KST (Know Sure Thing Oscillator)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:know_sure_thing_kst

# Borsa döngüsünün birincil dalgalanmalarını daha iyi yansıtmak için
#  formülü, daha uzun ve daha baskın zaman aralıklarından daha fazla etkilenecek
#  şekilde tartıldığından, ana borsa döngüsü bağlantılarını belirlemek yararlıdır.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  roc1(int): roc1 periyodu.
#  roc2(int): roc2 periyodu.
#  roc3(int): roc3 periyodu.
#  roc4(int): roc4 periyodu.
#  window1(int): n1 düzleştirilmiş dönem.
#  window2(int): n2 düzleştirilmiş dönem.
#  window3(int): n3 düzleştirilmiş dönem.
#  window4(int): n4 düzleştirilmiş dönem.
#  nsig(int): sinyal için n dönem.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class KSTIndicator(IndicatorMixin):
    def __init__(
        self,
        close: pd.Series,
        roc1: int = 10,
        roc2: int = 15,
        roc3: int = 20,
        roc4: int = 30,
        window1: int = 10,
        window2: int = 10,
        window3: int = 10,
        window4: int = 15,
        nsig: int = 9,
        fillna: bool = False,
    ):
        self._close = close
        self._r1 = roc1
        self._r2 = roc2
        self._r3 = roc3
        self._r4 = roc4
        self._window1 = window1
        self._window2 = window2
        self._window3 = window3
        self._window4 = window4
        self._nsig = nsig
        self._fillna = fillna
        self._run()

    def _run(self):
        min_periods_n1 = 0 if self._fillna else self._window1
        min_periods_n2 = 0 if self._fillna else self._window2
        min_periods_n3 = 0 if self._fillna else self._window3
        min_periods_n4 = 0 if self._fillna else self._window4
        rocma1 = (
            (
                (
                    self._close
                    - self._close.shift(self._r1, fill_value=self._close.mean())
                )
                / self._close.shift(self._r1, fill_value=self._close.mean())
            )
            .rolling(self._window1, min_periods=min_periods_n1)
            .mean()
        )
        rocma2 = (
            (
                (
                    self._close
                    - self._close.shift(self._r2, fill_value=self._close.mean())
                )
                / self._close.shift(self._r2, fill_value=self._close.mean())
            )
            .rolling(self._window2, min_periods=min_periods_n2)
            .mean()
        )
        rocma3 = (
            (
                (
                    self._close
                    - self._close.shift(self._r3, fill_value=self._close.mean())
                )
                / self._close.shift(self._r3, fill_value=self._close.mean())
            )
            .rolling(self._window3, min_periods=min_periods_n3)
            .mean()
        )
        rocma4 = (
            (
                (
                    self._close
                    - self._close.shift(self._r4, fill_value=self._close.mean())
                )
                / self._close.shift(self._r4, fill_value=self._close.mean())
            )
            .rolling(self._window4, min_periods=min_periods_n4)
            .mean()
        )
        self._kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
        self._kst_sig = self._kst.rolling(self._nsig, min_periods=0).mean()

    def kst(self) -> pd.Series:
        kst_series = self._check_fillna(self._kst, value=0)
        return pd.Series(kst_series, name="kst")

    # Sinyal Çizgisi:
    def kst_sig(self) -> pd.Series:
        kst_sig_series = self._check_fillna(self._kst_sig, value=0)
        return pd.Series(kst_sig_series, name="kst_sig")

    def kst_diff(self) -> pd.Series:
        kst_diff = self._kst - self._kst_sig
        kst_diff = self._check_fillna(kst_diff, value=0)
        return pd.Series(kst_diff, name="kst_diff")
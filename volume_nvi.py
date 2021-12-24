# NVI (Negative Volume Index)
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:negative_volume_inde

# Negatif Hacim Endeksi (NVI), akıllı paranın ne zaman aktif olduğuna
#  karar vermek için hacimdeki değişikliği kullanan kümülatif bir göstergedir.
#  Paul Dysart bu göstergeyi ilk olarak 1930'larda geliştirdi. Dysart'ın
#  Negatif Hacim Endeksi, hacmin azaldığı günlerde akıllı paranın aktif olduğu
#  ve hacmin arttığı günlerde çok akıllı olmayan paranın aktif olduğu varsayımı
#  altında çalışır.

# [...] Hacim bir dönemden diğerine arttığında kümülatif NVI çizgisi değişmedi.
#  Başka bir deyişle, hiçbir şey yapılmadı. Stock Market Logic'ten Norman Fosback,
#  Net Avanslar için yüzde fiyat değişimini değiştirerek göstergeyi ayarladı.
#  Bu uygulama Fosback versiyonudur.

# Eğer bugünün hacmi dünün hacminden azsa:
#       nvi(t) = nvi(t-1) * (1 + (close(t) - close(t-1)) /close(t-1))
# Değilse: nvi(t) = nvi(t-1)

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  volume(pandas.Series): veri kümesi 'Volume' sütunu.
#  fillna(bool): True ise, nan değerlerini 1000 ile doldur.


import numpy as np
import pandas as pd
from _utilities import IndicatorMixin

class NegativeVolumeIndexIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, volume: pd.Series, fillna: bool = False):
        self._close = close
        self._volume = volume
        self._fillna = fillna
        self._run()

    def _run(self):
        price_change = self._close.pct_change()
        vol_decrease = self._volume.shift(1) > self._volume
        self._nvi = pd.Series(
            data=np.nan, index=self._close.index, dtype="float64", name="nvi"
        )
        self._nvi.iloc[0] = 1000
        for i in range(1, len(self._nvi)):
            if vol_decrease.iloc[i]:
                self._nvi.iloc[i] = self._nvi.iloc[i - 1] * (1.0 + price_change.iloc[i])
            else:
                self._nvi.iloc[i] = self._nvi.iloc[i - 1]

    def negative_volume_index(self) -> pd.Series:
        # Herhangi bir na olmaması, hata fırlatmasından daha iyidir (!)
        nvi = self._check_fillna(self._nvi, value=1000)
        return pd.Series(nvi, name="nvi")
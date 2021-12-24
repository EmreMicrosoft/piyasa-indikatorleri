# ROC (Rate of Change)
# https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum

# Basitçe Momentum olarak da adlandırılan Değişim Oranı (ROC) göstergesi,
#  bir dönemden diğerine fiyattaki yüzde değişimini ölçen saf bir momentum osilatörüdür.
#  ROC hesaplaması, mevcut fiyatı "n" dönem önceki fiyatla karşılaştırır.
#  Grafik, Değişim Hızı pozitiften negatife doğru hareket ederken sıfır çizgisinin
#  üstünde ve altında dalgalanan bir osilatör oluşturur. Bir momentum osilatörü
#  olarak ROC sinyalleri, merkez çizgisi geçişlerini, sapmaları ve aşırı alım/satım
#  okumalarını içerir. Farklılıklar, geri dönüşlerin habercisi olmaktan daha sık başarısız olur (!).
#  Merkez çizgisi geçişleri, özellikle kısa vadede, testereye eğilimli olsa da,
#  bu geçişler genel eğilimi belirlemek için kullanılabilir. Aşırı alım veya aşırı satım
#  uçlarını belirlemek, ROC'ye doğal gelir.

# Argümanlar:
#  close(pandas.Series): veri kümesi 'Kapat' sütunu.
#  window(int): n periyodu.
#  fillna(bool): True ise, nan değerlerini doldur.


import pandas as pd
from _utilities import IndicatorMixin

class ROCIndicator(IndicatorMixin):
    def __init__(self, close: pd.Series, window: int = 12, fillna: bool = False):
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _run(self):
        self._roc = (
            (self._close - self._close.shift(self._window))
            / self._close.shift(self._window)) * 100

    def roc(self) -> pd.Series:
        roc_series = self._check_fillna(self._roc)
        return pd.Series(roc_series, name="roc")
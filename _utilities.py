import math
import numpy as np
import pandas as pd


class IndicatorMixin:
    _fillna = False

	# fillna bayrağının True olup olmadığını kontrol et.
	# series(pandas.Series): veri kümesi 'Kapat' sütunu.
    # value(int): boşlukları doldurmak için değer; eğer -1
	#  ise 'doldurma' modunu kullanarak değerleri doldur.
    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        if self._fillna:
            series_output = series.copy(deep=False)
            series_output = series_output.replace([np.inf, -np.inf], np.nan)
            if isinstance(value, int) and value == -1:
                series = series_output.fillna(method="ffill").fillna(value=-1)
            else:
                series = series_output.fillna(method="ffill").fillna(value)
        return series

    @staticmethod
    def _true_range(
        high: pd.Series, low: pd.Series, prev_close: pd.Series
    ) -> pd.Series:
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range

# "Nans" değerlerine sahip satırları drop eder.
def dropna(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    number_cols = df.select_dtypes("number").columns.to_list()
    df[number_cols] = df[number_cols][df[number_cols] < math.exp(709)]  # big number
    df[number_cols] = df[number_cols][df[number_cols] != 0.0]
    df = df.dropna()
    return df


def _sma(series, periods: int, fillna: bool = False):
    min_periods = 0 if fillna else periods
    return series.rolling(window=periods, min_periods=min_periods).mean()


def _ema(series, periods, fillna=False):
    min_periods = 0 if fillna else periods
    return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()

# Her dizin için iki liste arasında minimum veya maksimum değeri bulur.
def _get_min_max(series1: pd.Series, series2: pd.Series, function: str = "min"):
    series1 = np.array(series1)
    series2 = np.array(series2)
    if function == "min":
        output = np.amin([series1, series2], axis=0)
    elif function == "max":
        output = np.amax([series1, series2], axis=0)
    else:
        raise ValueError('"f" değişken değeri "min" ya da "max" olmalıdır')

    return pd.Series(output)

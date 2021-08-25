"""마켓(binance)에서 데이터를 얻어오는 함수를 구현.
"""
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from utils.share import datetime_to_unixtime, enum_to_unixtime, to_thousands

class Binance:
    def __init__(self, symbol:str='BTCUSDT', interval:str='1h') -> None:
        self.symbol = symbol
        self.interval = interval

        self.dataframe = None
        self.load_dataframe()
    def get_data(self,start_str:str,end_str:str) -> pd.DataFrame:
        """Get Data from time index.
        """
        start_unix = to_thousands(datetime_to_unixtime(start_str))
        end_unix = to_thousands(datetime_to_unixtime(end_str))
        return self._slice_data_from_index(start_unix, end_unix)
    def _slice_data_from_index(self, start_unix:int,end_unix:int) -> pd.DataFrame:
        return self.dataframe.loc[end_unix:start_unix]

    def load_dataframe(self) -> None:
        self._read_csv_file() #1
        self._astype_unixcolumn_to_int() #2
        self._set_index_as_unix() #3
        assert self.dataframe is not None
    def _read_csv_file(self) -> None: #1
        try:
            self.dataframe = pd.read_csv('./assets/Binance_{}_{}.csv'.format(self.symbol, self.interval), usecols=['unix', 'open', 'high', 'low', 'close', 'Volume BTC'])
        except FileNotFoundError:
            print("File not found.", './assets/Binance_{}_{}.csv'.format(self.symbol, self.interval))
            import sys
            sys.exit(0)
    def _astype_unixcolumn_to_int(self) -> None: #2
        self.dataframe = self.dataframe.astype({'unix':int}) # float to int (소수점 없애고 정수화)
    def _set_index_as_unix(self) -> None: #3
        self.dataframe = self.dataframe.set_index('unix')
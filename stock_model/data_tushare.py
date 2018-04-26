import os
import queue
import threading

import tushare as ts
import pandas as pd


class tushare_Data:
	# use tushare to get closing price per month

    def __init__(self, start="2010-01-01", end="2018-04-01", freq="M", path="data\\price_data"):
        self.hist_data = []
        self.data = pd.DataFrame()
        self.stock_list = []
        self.queue = queue.Queue()

        self.path = path
        self.freq = freq
        self.start = start
        self.end = end
        self.num_of_threads = 8

        self._create_dir()
        self.get_stock_list()

    def _create_dir(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if not os.path.exists(self.path + "\\separate_{}".format(self.freq)):
            os.makedirs(self.path + "\\separate_{}".format(self.freq))

        if not os.path.exists(self.path + "\\total_{}".format(self.freq)):
            os.makedirs(self.path + "\\total_{}".format(self.freq))

    def get_stock_list(self):
        self.stock_list = os.listdir("data\\stock_data")
        self.stock_list = map(lambda x: x[:6], self.stock_list)
        """
        with open("stock_list.txt", "w") as file:
            for stock in self.stock_list:
                file.write(stock)
                file.write("\n")
            file.close()

        print(list(self.stock_list))
        return self.stock_list
        """

    def get_hist_data(self, code):

        print(code, threading.current_thread().name)
        if not os.path.isfile(self.path + "\\separate_{}\\{}.csv".format(self.freq, code)):
            code_data = ts.get_k_data(code=code, start=self.start, end=self.end, ktype=self.freq)[["date", "close"]]
            code_data.set_index("date", inplace=True)
            code_data.columns = [code]
            code_data.to_csv(self.path + "\\separate_{}\\{}.csv".format(self.freq, code))
        else:
            code_data = pd.read_csv(self.path + "\\separate_{}\\{}.csv".format(self.freq, code), index_col=0)

        return code_data

    def _threader(self):
        while True:
            code = self.queue.get()
            df = self.get_hist_data(code)
            self.hist_data.append(df)
            self.queue.task_done()

    def start_getting_data(self):
        for i in range(self.num_of_threads):
            thread = threading.Thread(target=self._threader)
            thread.daemon = True
            thread.start()

        for code in self.stock_list:
            self.queue.put(code)

        self.queue.join()

        self.data = self.data.join(self.hist_data, how="outer")
        self.data.index = pd.to_datetime(self.data.index, infer_datetime_format=True)
        self.data = self.data.resample("M").ffill()
        self.data = self.data.fillna(method="ffill")
        self.data = self.data.sort_index(axis=1)
        self.data.index.rename("date", inplace=True)
        self.data.to_csv(self.path + "\\total_{}\\tushare_data.csv".format(self.freq))
        print(self.data)
        return self.data


if __name__ == "__main__":
    hist_data = tushare_Data()
    hist_data.start_getting_data()

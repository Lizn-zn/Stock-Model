import os

import pandas as pd


class DataPrepare:

    def __init__(self, path=list(["data\\monthly", "data\\halfyear"])):
        self.path = path
        self.dir_monthly = os.listdir(path[0])
        self.dir_halfyear = os.listdir(path[1])

    def normalization(self):
        if not os.path.exists("data\\monthly_normal"):
            os.makedirs("data\\monthly_normal")

        if not os.path.exists("data\\halfyear_normal"):
            os.makedirs("data\\halfyear_normal")

        tmp = ["monthly_normal", "halfyear_normal"]
        for n, dir_ in enumerate((self.dir_monthly, self.dir_halfyear)):
            for feature in dir_:
                if feature.endswith(".csv"):
                    print(feature)
                    data = pd.read_csv(
                        self.path[n] + "\\" + feature, index_col=0)
                    mean = data.mean(axis=1, skipna=True)
                    std = data.std(axis=1, skipna=True)

                    for i, row in data.iterrows():
                        row[row > (mean[i] + 5 * std[i])
                            ] = mean[i] + 5 * std[i]
                        row[row < (mean[i] - 5 * std[i])
                            ] = mean[i] - 5 * std[i]
                        mean[i] = row.mean(skipna=True)
                        std[i] = row.std(skipna=True)
                        row = (row - mean[i]) / std[i]
                        data.loc[i] = row
                    data.to_csv("data\\{}\\{}".format(tmp[n], feature))


def get_names(monthly_dir="data\\monthly_normal", half_year_dir="data\\halfyear_normal", ):

    # Get the name of tables
    monthly_data_name = os.listdir(monthly_dir)
    half_year_data_name = os.listdir(half_year_dir)

    # Initialize DataFrame list
    monthly_data_list = []
    half_year_data_list = []

    # Time format index name
    month_data_range = pd.date_range(
        start="2010-01-01", end="2018-04-01", freq="1M")
    half_year_data_range = pd.date_range(
        start="2009-10-01", end="2018-11-01", freq="6M")

    # Read monthly data tables to DataFrames
    for data_name in monthly_data_name:
        print(data_name)
        tmp = pd.read_csv(monthly_dir + "\\" + data_name, index_col=0)
        tmp.index = month_data_range
        monthly_data_list.append(tmp)

    # Read heal-year data tables to DataFrames
    for data_name in half_year_data_name:
        print(data_name)
        tmp = pd.read_csv(half_year_dir + "\\" + data_name, index_col=0)
        tmp.index = half_year_data_range
        half_year_data_list.append(tmp.reindex(month_data_range))

    # Get codes of the stocks
    stocks = monthly_data_list[0].columns

    return [stocks, month_data_range, monthly_data_name, monthly_data_list, half_year_data_name, half_year_data_list]


def stock_df(save_dir="data\\stock_data_normal"):
    """
    Store data of a single stock in a single excel table
    :param monthly_dir: monthly data directory
    :param half_year_dir: half year data directory
    :param save_dir: stock data table saving path
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    stocks, month_data_range, monthly_data_name, monthly_data_list, half_year_data_name, half_year_data_list = get_names()
    # Create table for each stock
    for stock in stocks:
        print(stock)
        stock_data = pd.DataFrame(index=month_data_range)

        for (i, data_name) in enumerate(monthly_data_name):
            if(stock not in monthly_data_list[i]):
                print('The stock %s does not have month %s data' %
                      (str(stock), data_name))
                continue
            stock_data[data_name[:-4]] = monthly_data_list[i][stock]
        for (i, data_name) in enumerate(half_year_data_name):
            if(stock not in half_year_data_list[i]):
                print('The stock %s does not have year %s data' %
                      (str(stock), data_name))
                continue
            stock_data[data_name[:-4]] = half_year_data_list[i][stock]
        # Forward fill in the blank
        stock_data.dropna(axis=0, thresh=5, inplace=True)

        if(stock_data.empty):
            continue
        stock_data.fillna(method="ffill", inplace=True)
        stock_data.fillna(method="bfill", inplace=True)
        # Save to disk
        stock_data.to_csv(save_dir + "\\" + stock + ".csv")


if __name__ == "__main__":
    dp = DataPrepare()
    dp.normalization()
    stock_df()

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
                    data = pd.read_csv(self.path[0] + "\\" + feature, index_col=0)
                    mean = data.mean(axis=1, skipna=True)
                    std = data.std(axis=1, skipna=True)

                    for i, row in data.iterrows():
                        row[row > (mean[i] + 3 * std[i])] = mean[i] + 3 * std[i]
                        row[row < (mean[i] - 3 * std[i])] = mean[i] - 3 * std[i]
                        mean[i] = row.mean(skipna=True)
                        std[i] = row.std(skipna=True)
                        row = (row - mean[i]) / std[i]
                        data.loc[i] = row
                    data.to_csv("data\\{}\\{}".format(tmp[n], feature))




if __name__ == "__main__":
    dp = DataPrepare()
    dp.normalization()

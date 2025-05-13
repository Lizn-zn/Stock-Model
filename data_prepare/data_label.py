import os
import pandas as pd
import numpy as np


def label_data(path, nb_class=5, store_path="data\\label_data"):
    if not os.path.exists(path):
        print('could not find {}, please run data_tushare'.format(path))
        return
    if not os.path.exists(store_path):
        os.makedirs(store_path)

    df = pd.read_csv(path, index_col=0)
    for i in range(df.shape[1] - 1):
        temp_1 = np.array(df.iloc[:, i])
        temp_2 = np.array(df.iloc[:, i + 1])
        ratio = temp_2 / temp_1
        sort = np.argsort(ratio)
        nan = np.where(np.isnan(ratio[sort]))[0]

        if(nan.size != 0):
            length = nan[0]
        else:
            length = sort.shape[0]
        margin = np.arange(0, length + length / nb_class - 1,
                           length / nb_class).astype(np.int)
        for j in range(nb_class):
            df.iloc[sort[margin[j]:margin[j + 1]], i] = j + 1

    df.drop(df.columns[-1], axis=1, inplace=True)
    df.to_csv(store_path + "\\label.csv")
    print("label the data successfully, and the label is stored in {}".format(store_path))


if __name__ == '__main__':
    label_data('data\\price_data\\total_M\\wind_data.csv')
    print('get it')
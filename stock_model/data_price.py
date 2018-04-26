import os
import pandas as pd


def merge_data(directory, store_path="data\\price_data\\total_M"):
    if not os.path.exists(directory):
        print('could not find {}, please run data_tushare'.format(directory))
        return
    # Get table names
    excel_list = os.listdir(directory)

    # Initialize dataframe
    df = pd.DataFrame()
    df_list = []

    for excel in excel_list:

        # Continue if it is not a table
        if not (excel.endswith(".csv") or excel.endswith(".xlsx")):
            continue

        if excel.startswith("~$"):
            continue

        # Read data from one table
        df_new = pd.read_excel(directory + "\\" + excel,
                               index_col=0, skip_footer=1)
        df_new.index.rename(name="Code", inplace=True)
        df_new.drop("证券简称", axis=1, inplace=True)

        # Add this DataFrame to DataFrame list
        df_list.append(df_new)

    # Concat all the DataFrames in DataFrame list
    df = pd.concat(df_list, join='outer', axis=1)

    # Time format index name
    month_data_range = pd.date_range(
        start="2010-01-01", end="2018-04-01", freq="1M")

    df.columns = month_data_range

    if(not os.path.exists(store_path)):
        os.makedirs(store_path)
    df.to_csv(store_path + "\\wind_data.csv")

    print("concat the data successfully, and the whole date is stored in {}".format(store_path))


if __name__ == '__main__':
    merge_data("收盘价格")

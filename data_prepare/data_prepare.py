import os

import pandas as pd


def concat_data(directory, subs_col=None, period="monthly", store_path=None):
    """
    Concat data
    :param directory: data file directory
    :param subs_col: substitute column name
    :param period: data period
    :param store_path: store path
    :return: a dataframe with concat data
    """

    print("Concating data in directory : " + directory)

    # Create dir
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data\\{}".format(period)):
        os.makedirs("data\\{}".format(period))

    if store_path is None:
        store_path = "date\\" + directory + ".csv"

    # Get table names
    excel_list = os.listdir(directory)

    # Initialize dataframe
    df = pd.DataFrame()
    df_list = []

    is_written = False

    for excel in excel_list:

        # Continue if it is not a table
        if not (excel.endswith(".csv") or excel.endswith(".xlsx")):
            continue

        if excel.startswith("~$"):
            continue

        year = excel[:4]

        # Read data from one table
        df_new = pd.read_excel(directory + "\\" + excel, index_col=0)
        df_new.index.rename(name="Code", inplace=True)
        df_new.drop("证券简称", axis=1, inplace=True)

        if not is_written:
            names = df_new.columns.values
            temp = list(map(lambda x: x[0].split('\n')[
                        0] + ' : ' + x[1], zip(names, subs_col)))
            file_text.write('\n'.join(temp))
            is_written = True

        # Substitute columns in Chinese Mandarin by English name
        if subs_col is not None:
            if period == "halfyear":
                term = excel[5: 8]
                term_map = {"mid": "_10", "end": "_04", "new": "_10"}
                subs_col_name = [name + "_" + str(int(year) + int(term_map[term] == "end")) + term_map[term]
                                 for name in subs_col]
                df_new.columns = subs_col_name

            elif period == "monthly":
                month = "_" + excel[5: 7]
                subs_col_name = [name + "_" +
                                 year + month for name in subs_col]
                df_new.columns = subs_col_name

            else:
                raise ValueError

        # Add this DataFrame to DataFrame list
        df_list.append(df_new)

    # Concat all the DataFrames in DataFrame list
    df = df.join(df_list, how="outer")

    # Keep stocks in Shanghai and Shenzhen Stock Exchange
    m, n = df_list[0].shape
    df.drop([df.index[m - 1], df.index[m - 2]], axis=0, inplace=True)
    keep_index = df.index[df.index.str.startswith(
        "60") | df.index.str.startswith("00")]
    df = df.ix[keep_index]

    df.sort_index(axis=1, inplace=True)

    # Save data for each feature
    for i in range(n):
        feature_size = len(df_list)
        tmp_df = df.ix[:, i * feature_size: i * feature_size + feature_size].T

        # Get the name of each feature
        name = df.columns[i * feature_size]
        name = name[:name.find("20") - 1]
        tmp_df.index.rename(name="Code", inplace=True)

        mean = tmp_df.mean(axis=1)
        for column in tmp_df.columns:
            if tmp_df[column].empty:
                tmp_df[column] = mean

        print("Saving split data : {}".format(name))
        tmp_df.to_csv("data\\" + period + "\\" + name + ".csv")

    # Save this DataFrame
    df.to_csv(store_path)
    return df


def get_names(monthly_dir="data\\monthly", half_year_dir="data\\halfyear", ):

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


def stock_df(save_dir="data\\stock_data"):
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
        stock_data.dropna(axis=0, thresh=5,inplace=True)

        if(stock_data.empty):
            continue
        stock_data.fillna(method="ffill", inplace=True)
        stock_data.fillna(method="bfill", inplace=True)
        # Save to disk
        stock_data.to_csv(save_dir + "\\" + stock[:-3] + ".csv")


if __name__ == "__main__":
    # EPS: Earning per share; NP: net profit; NA: net asset; ROE: Rate of Return on Common Stockholders’ Equity
    # ps: per share; EM: Equity Multiplier; GS: gross sales; CaR: Cash Ratio; DTAR: Debt to tangible assets ratio
    # gr: growth rate; CR: current ratio; AR: Acid-test Ratio; LDOR: Long Term Debt and Operation Asset Ratio
    # yoy: on year-on-year base; LTDR: Long Term Debt Ratio; bo: by operation

    file_text = open('data_discribtion.txt', 'w')

    directory_names = ["成长能力与偿债能力", "技术指标", "财务质量", "估值指标"]

    col_growth = ["EPS_gr_yoy", "GS_gr_yoy", "NP_gr_yoy", "NA_gr_yoy",
                  "CF_gr_yoy", "CF_bo_gr_yoy", "ROE", "EM",
                  "CR", "AR", "CaR", "DTAR", "LDOR", "LTDR"]
    concat_data(directory_names[0], subs_col=col_growth,
                period="halfyear", store_path="data\\growth_and_debt.csv")

    col_tech = ["DMA", "DMI", "MACD", "BBI", "BIAS", "CCI", "DPO", "ARBR",
                "CR", "PSY", "BBIBOLL", "BOLL", "MktSyn", "MI", "ADTM", "ATR"]
    concat_data(directory_names[1], subs_col=col_tech,
                period="monthly", store_path="data\\tech.csv")

    col_fin = ["ROE_ave", "ROE_flat", "ROA", "ROTA", "ROIC", "ROP", "NPMOS", "GPMOS",
               "ROSTC", "AD_TI", "AD_OP", "DAR", "CAT", "NCAT", "TAT"]
    concat_data(directory_names[2], subs_col=col_fin,
                period="halfyear", store_path="data\\finance.csv")

    col_valuation = ["CAP_1", "CAP_2", "PE_TTM", "PE_TTM_2", "PE_LYR", "PB", "PS_TTM", "PS_LYR",
                     "PCF_OPER_TTM", "PCF_NF_TTM", "PCF_OPER_LYR", "PCF_NF_LYR"]
    concat_data(directory_names[3], subs_col=col_valuation,
                period="monthly", store_path="data\\valuation.csv")

    stock_df()

    file_text.close()

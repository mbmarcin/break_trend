import pandas as pd
from statistics import mean

def get_data(dir0="..\..\data_projects"):
    df0 = pd.read_excel(dir0+"\\"+"tempTrendgrupa.xlsx")
    df0['id'] = df0.iloc[:, 0].astype('str') + df0.iloc[:, 1].astype('str')
    return df0

def best_fit_slope(xs, ys):
    """
    machine learning regression
    """
    m = (((mean(xs)*mean(ys)) - mean(xs*ys))/((mean(xs)*mean(xs)) - mean(xs*xs)))
    #b = mean(ys) - m*mean(xs)
    return m #,b

def table_id(df, year):
    temp = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])
    return temp.iloc[:, 4].drop_duplicates().to_frame()

def max_year_month(df):
    """
    :param df:
    :return: max year and max month of table
    """
    max_year = int(df.iloc[:, 0].max())
    max_year_month0 = df.loc[df.iloc[:, 0] == max_year]  # ------------
    max_year_month1 = int(max_year_month0.iloc[:, 1].max())  # ------------ Think about it
    return max_year, max_year_month1

def slope_per_range(year=0):
    return year

def cumulative_slope_per_month(df, year):
    df1 = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])
    for i in list(df1.iloc[:, 2].drop_duplicates()):
        if len(df1.loc[df1.iloc[:, 2] == i]) >= 3:
            #x = df1.loc[df1.iloc[:, 2] == i]
            df_main = pd.merge(table_id(df, year), df1.loc[df1.iloc[:, 2] == i], on='id', how='left').fillna(0)
            print(df_main)
    #return x


print(cumulative_slope_per_month(get_data(), 2019))









df = get_data()
#print(get_data().head())
a, b = max_year_month(df)
#print(table_id(2019, get_data()).head())


# aktualny rok, badanie trendu po kolei
# dorzucić max rok dla uniwersalności funkcji

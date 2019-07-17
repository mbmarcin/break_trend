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

def table_id(year, df):
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

def cumulative_slope_per_month(df, year):
    pass

def slope_per_range():
    pass











df = get_data()
#print(get_data().head())
a, b = max_year_month(df)
#print(table_id(2019, get_data()).head())


# aktualny rok, badanie trendu po kolei
# dorzucić max rok dla uniwersalności funkcji

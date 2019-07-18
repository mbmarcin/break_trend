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
    try:
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) / ((mean(xs) * mean(xs)) - mean(xs * xs)))
    except ZeroDivisionError:
        return 0
    #b = mean(ys) - m*mean(xs)
    return m #,b

def slope_per_month(s):
    """
    input series object, output df with mc(index) and slope id
    """
    target = list(s[:3])
    slope_ = list()
    slope_.append(best_fit_slope(pd.Series(target), list(range(len(target)))))
    for i in s[3:]:
        target.append(i)
        slope_.append(best_fit_slope(pd.Series(target), list(range(len(target)))))
    return pd.DataFrame({'mc_slope': slope_, 'mc': list(range(3, len(s)+1))})

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
    """
    1.minimum 3 months activity
    :param df: df
    :param year: int
    :return: df
    """
    df1 = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])
    for i in list(df1.iloc[:, 2].drop_duplicates()):
        if len(df1.loc[df1.iloc[:, 2] == i]) >= 3: #1.minimum 3 months activity
            df_main0 = pd.merge(table_id(df, year), df1.loc[df1.iloc[:, 2] == i], on='id', how='left').fillna(0)
            df_main1 = pd.merge(df_main0, slope_per_month(df_main0.iloc[:, 4]), on='mc', how='left').fillna(0)
            return df_main1

        else:
            pass



dfx = cumulative_slope_per_month(get_data(), 2019)
print(dfx)
#print(dfx.iloc[0:3, 4])
#dat.iloc[row, column]

#df = get_data()
#print(get_data().head())
#a, b = max_year_month(df)
#print(table_id(2019, get_data()).head())

# aktualny rok, badanie trendu po kolei
# dorzucić max rok dla uniwersalności funkcji

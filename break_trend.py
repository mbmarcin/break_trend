import pandas as pd
from statistics import mean


def get_data(dir0="..\..\data_projects"):
    df0 = pd.read_excel(dir0 + "\\" + "tempTrendgrupa.xlsx")
    df0['id'] = df0.iloc[:, 0].astype('str') + df0.iloc[:, 1].astype('str')
    df0.iloc[:, 2] = df0.iloc[:, 2].str.upper()
    # df0['id1'] = df0.iloc[:, 1]
    return df0


def best_fit_slope(xs, ys):
    """
    machine learning regression
    """
    try:
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) / ((mean(xs) * mean(xs)) - mean(xs * xs)))
    except ZeroDivisionError:
        return 0
    # b = mean(ys) - m*mean(xs)
    return m  # ,b


def slope_per_month(s, col):
    """
    input series object, output df with mc(index) and slope id
    """
    target = list(s[:2])
    slope_ = list()
    slope_.append(best_fit_slope(pd.Series(target), list(range(len(target)))))
    for i in s[2:]:
        target.append(i)
        slope_.append(best_fit_slope(pd.Series(target), list(range(len(target)))))
    return pd.DataFrame({'mc_slope': slope_, col: list(range(2, len(s) + 1))})

# test slope
"""
x = [5,8,2,1,7,9,7,6]
print(
    slope_per_month(pd.Series(x), 'col').info()
)
"""


def table_id(df, *year):
    temp0 = df.iloc[:, [0, 1, 4]].drop_duplicates()
    temp1 = temp0.loc[temp0.iloc[:, 0].isin(year)].sort_values(by=[temp0.columns[0], temp0.columns[1]])
    return temp1.reset_index(drop=True)

# test table id
"""
print(
table_id(get_data(), 2019)
)
"""

def max_year_month(df):
    """
    :param df:
    :return: max year and max month of table
    """
    max_year = int(df.iloc[:, 0].max())
    max_year_month0 = df.loc[df.iloc[:, 0] == max_year]  # ------------
    max_year_month1 = int(max_year_month0.iloc[:, 1].max())  # ------------ Think about it
    return max_year, max_year_month1


def to_save(*l):
    for i in l:
        i.name = i
        i.to_csv('{}.txt'.format(i.name), sep=';', index=False, header=True)
        # print('save {}'.format(i))
        """
        def write_csv():
        df2 = pd.DataFrame()
        for name, df in data.items():
        df2 = df2.append(df)
        df2.to_csv('mydf.csv')
        """


def slope_per_range(year=0):
    return year


def check_trend(ss):
    pass
    """
    revers = ss.iloc[::-1]
    if revers[len(revers)-1] < 0:
        '#check trend minus'
        l_temp = list()
        for val in revers:
            if val <= 0:
                l_temp.append(val)
            else:
                break
        '#check deeping'
        if len(l_temp) > 1:
            ddp = [l_temp[i] < l_temp[i + 1] for i in range(len(l_temp)-1)] # sprawdzić dla wszystkich mc ujemne rosnąco
            return len(l_temp), int(ddp.count(True) == len(l_temp)-1), -1
        else:
            return len(l_temp), 0, -1
    elif revers[len(revers)-1] > 0:
        '#check trend plus'
        l_temp = list()
        for val in revers:
            if val > 0:
                l_temp.append(val)
            else:
                break
        '#check deeping'
        if len(l_temp) > 1:
            ddp = [l_temp[i] > l_temp[i + 1] for i in range(len(l_temp)-1)]
            return len(l_temp), int(ddp.count(True) == len(l_temp)-1), 1
        else:
            return len(l_temp), 0, 1
    else:
        return 0, 0, 0
"""

def check_value(ss):
    """
    :param ss:
    :return: True or False
    """
    revers = ss.iloc[::-1]

    pass





def cumulative_slope_per_month(df, year):
    """
    1.minimum 3 months activity
    :param df: df
    :param year: int
    :return: df
    """

    df1 = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])

    #tt = list()  # table with all slops
    result = pd.DataFrame(columns=('year', 'id', 'break_point', 'deep', 'slope', 'activity'))
    row = 0
    counter = list()
    all = len(df1.iloc[:, 2].drop_duplicates())
    for i in df1.iloc[:, 2].drop_duplicates():
        if len(df1.loc[df1.iloc[:, 2] == i]) >= 2:  # 1.minimum 2 months activity before 3 months

            df_main0 = pd.merge(table_id(df, year),
                                df1.loc[df1.iloc[:, 2] == i],
                                on='id',
                                how='left',
                                suffixes=('_df1', '_df2')).fillna(0)

            col = df_main0.columns[1]

            df_main1 = pd.merge(df_main0,
                                slope_per_month(df_main0.iloc[:, 6], col),
                                on=col,
                                how='left',
                                suffixes=('_df1', '_df2')).fillna(0)


            #tt.append(df_main1.iloc[:, [3, 5]]) #----------------------------------------------------------------------look at this

            '#check break trend'
            ser = df_main1.iloc[:, 7]
            a, b, c = check_trend(ser) # for all values



            '#add row with result'
            result.loc[row] = [year, i, a, b, c, len(df1.loc[df1.iloc[:, 2] == i])]
            row += 1
            counter.append(i)
            print(df_main1)

            '#print progress'
            if len(counter) % 10 == 0:
                print('Trend analysis: {}/{}'.format(len(counter), all))
            else:
                pass
        else:
            pass

    return result

""" if który sprawdza czy jest poprzedni rok ------------------------------------------------------
    if df0.loc[df0.iloc[:, 0].isin([year_id-1])].empty is True:
        print('missing the previous year')
    else:
        df1 = df0.loc[df0.iloc[:, 0].isin([year_id, year_id-1])]
"""

def compare_sales(df0, df_result):

    y, m = max_year_month(df0) # to może iść do ogółu
    list_df = list()
    for i in df_result.iloc[:, 1].drop_duplicates():
        df_n = df0.loc[df0.iloc[:, 2] == i]
        df_main0 = pd.merge(table_id(get_data(), *list(get_data().iloc[:, 0].drop_duplicates())),
                            df_n,
                            on='id',
                            how='left',
                            suffixes=('_df1', '_df2')).fillna(0)

        df1 = df_result.loc[df_result.iloc[:, 1] == i]  # df for break point
        break_point = int(df1.iloc[:, 2])

        sum_month = list()
        for year in df_main0.iloc[:, 0].drop_duplicates():
            df_year = df_main0.loc[(df_main0.iloc[:, 0] == year) & (df_main0.iloc[:, 1] <= m)]
            sum_month.append(df_year.iloc[:, 6].tail(break_point).sum())

        df_f = df1.copy()
        df_f['sales'] = sum_month[1] - sum_month[0]
        list_df.append(df_f)
        print(len(list_df))
    to_file = pd.concat(list_df)
    print('save a file')
    return to_file #to_file.to_csv('brekTrendTEST.txt', sep=';', index=False, header=True)


print(
    #compare_sales(get_data(), cumulative_slope_per_month(get_data(), 2019))
    cumulative_slope_per_month(get_data(), 2019)
    #table_id(get_data(), 2019)
    #get_data()
)
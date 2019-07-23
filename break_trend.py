import pandas as pd
from statistics import mean


def get_data(dir0="..\..\data_projects"):
    df0 = pd.read_excel(dir0 + "\\" + "tempTrendgrupa.xlsx")
    df0['id'] = df0.iloc[:, 0].astype('str') + df0.iloc[:, 1].astype('str')
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
    return pd.DataFrame({'mc_slope': slope_, 'mc': list(range(3, len(s) + 1))})


def table_id(df, *year, prm=0):
    if prm == 0:
        temp = df.loc[df.iloc[:, 0].isin(year)].sort_values(by=[df.columns[0], df.columns[1]])
        return temp.iloc[:, 4].drop_duplicates().to_frame()
    else:
        temp0 = df.iloc[:, [0, 1, 4]].drop_duplicates()
        temp1 = temp0.loc[temp0.iloc[:, 0].isin(year)].sort_values(by=[temp0.columns[0], temp0.columns[1]])
        return temp1.reset_index(drop=True)


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


def cumulative_slope_per_month(df, year):
    """
    1.minimum 3 months activity
    :param df: df
    :param year: int
    :return: df
    """

    df1 = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])

    # tt = list()  # table with all slops
    result = pd.DataFrame(columns=('year', 'id', 'break_point', 'dir', 'activity'))
    row = 0
    counter = list()
    all = len(df1.iloc[:, 2].drop_duplicates())
    for i in list(df1.iloc[:, 2].drop_duplicates()):
        if len(df1.loc[df1.iloc[:, 2] == i]) >= 3:  # 1.minimum 3 months activity
            df_main0 = pd.merge(table_id(df, year),
                                df1.loc[df1.iloc[:, 2] == i],
                                on='id',
                                how='left').fillna(0)
            df_main1 = pd.merge(df_main0,
                                slope_per_month(df_main0.iloc[:, 4]),
                                on=df_main0.columns[2],
                                how='left').fillna(0)

            # tt.append(df_main1.iloc[:, [3, 5]]) #----------------------------------------------------------------------look at this

            '#check break trend'
            ss = df_main1.iloc[:, 5]
            reverse = ss.iloc[::-1]

            l_temp = list()
            for val in reverse.iloc[:len(reverse) - 2]:
                if val < 0:
                    l_temp.append(val)
                else:
                    break

            '#check direction trend'
            if len(l_temp) > 0:
                dd = [l_temp[i] < l_temp[i + 1] for i in range(len(l_temp) - 1)]
                try:
                    dir_ = round(dd.count(True) / (len(l_temp) - 1) * -1, 2)
                except ZeroDivisionError:
                    dir_ = -1
            else:
                dir_ = 0

            '#add row with result'
            if len(l_temp) > 0:
                result.loc[row] = [year, i, len(l_temp), dir_, len(df1.loc[df1.iloc[:, 2] == i])]
                row += 1
                counter.append(i)
            else:
                pass

            '#print progress'
            if len(counter) % 10 == 0:
                print('Trend analysis: {}/{}'.format(len(counter), all))
            else:
                pass
        else:
            pass

    # function for save tables
    """
    result0 = pd.concat(tt)
    ll = [result, result0]
    to_save(*ll)
    """
    # result0.to_csv('result0.txt', sep=';', index=False, header=True)
    # result.to_csv('result.txt', sep=';', index=False, header=True)

    return result


""" if który sprawdza czy jest poprzedni rok ------------------------------------------------------
    if df0.loc[df0.iloc[:, 0].isin([year_id-1])].empty is True:
        print('missing the previous year')
    else:
        df1 = df0.loc[df0.iloc[:, 0].isin([year_id, year_id-1])]
"""


def compare_sales(df0, df_result):
    for i in list(df_result.iloc[:, 1].drop_duplicates()):
        df0 = df0.loc[df0.iloc[:, 2] == i]
        df_main0 = pd.merge(table_id(get_data(), *list(get_data().iloc[:, 0].drop_duplicates()), prm=1),
                            df0, on='id',
                            how='left',
                            suffixes=('_df1', '_df2')).fillna(0)

        df1 = df_result.loc[df_result.iloc[:, 1] == i]  # df for break point
        break_point = int(df1.iloc[:, 2])

        # df1 = df0.loc[(df0.iloc[:, 1].isin(list_mth)) & (df0.iloc[:, 2] == 'XXXGR18')]
        print(df_main0)
        break


print(
    compare_sales(get_data(), cumulative_slope_per_month(get_data(), 2019))
    # cumulative_slope_per_month(get_data(), 2019)

)

"""
    df1 = df0.loc[df0.iloc[:, 0].isin([year_id, year_id-1])]
    df2 = df1.loc[df1.iloc[:, 1].isin([list_id])]
    x1 = 4
    max_ = 7
    for i in range((max_-x1),max_):
    print(i)
    df1 = df0.loc[(df0.iloc[:, 1].isin(list_mth)) & (df0.iloc[:, 2] == 'XXXGR18')]
    # df1 = df1.loc[df1.grupoBRAND == 'XXXGR18']
    df2 = df1.pivot_table(values='wart', index='mc', columns='rok').reset_index()
    df2['diff_'] = round(df2.iloc[:, 2] / df2.iloc[:, 1] - 1, 2)
    df2['diff'] = df2.iloc[:, 2] - df2.iloc[:, 1]
    print(df2)
    print(df1.iloc[:, 0].drop_duplicates())
"""

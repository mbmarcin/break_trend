import pandas as pd
from statistics import mean


def get_data(dir0="..\..\data_projects"):
    try:
        df0 = pd.read_csv(dir0 + "\\" + "tempTrendgrupa.txt", sep=';')
        df0['id'] = df0.iloc[:, 0].astype('str') + df0.iloc[:, 1].astype('str')
        df0.iloc[:, 2] = df0.iloc[:, 2].str.upper()
        return df0
    except IOError:
        print('Nie mogę wczytać danych, sprawdź plik.')
        return pd.DataFrame()


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


def table_id(df, *year):
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


def slope_per_range(year=0):
    return year


def check_deep_trend(list_slope, list_sales):
    """
    :param list_slope: list of ids trend
    :param list_sales: sales
    :return: falling
    """
    qty_mth_deep_minus = list()
    i = 0
    prm2 = len(list_slope) - 1

    while i < prm2:
        if int(list_slope[i] < list_slope[i + 1]) == 1:
            qty_mth_deep_minus.append(1)
            i += 1
        elif int(list_slope[i] < list_slope[i + 1]) == 0 and int(list_sales[i] < list_sales[i + 1]) == 1:
            qty_mth_deep_minus.append(1)
            i += 1
        else:
            break

    return len(qty_mth_deep_minus)


def check_series_trend(list_slope, list_sales):
    """
    :param list_slope:
    :param list_sales:
    :return: parameters of trend
    """
    revers = list_slope.iloc[::-1]
    revers_s = list_sales.iloc[::-1]
    qty_mth_trend = list()

    '#check trend minus'
    if revers[len(revers)-1] < 0:
        for val in revers:
            if val <= 0:
                qty_mth_trend.append(val)
            else:
                break

        m = check_deep_trend(list(qty_mth_trend), list(revers_s))
        c = len(qty_mth_trend)

        return c*-1, m*-1

    elif revers[len(revers) - 1] > 0:
        for val in revers:
            if val > 0:
                qty_mth_trend.append(val)
            else:
                break
        m = check_deep_trend(list(qty_mth_trend), list(revers_s))
        c = len(qty_mth_trend)

        return c, m*-1

    else:
        return 0, 0


def check_empty_months(series):

    qty_empty_mth = list()
    i = 0
    list_ = list(series[::-1])
    while i < len(series[::-1]) - 1:
        if list_[i] == 0:
            qty_empty_mth.append(1)
            i += 1
        else:
            break
    return len(qty_empty_mth)


def cumulative_slope_per_month(df, year):
    """
    1.minimum 2 months activity
    :param df: df0 input data
    :param year: int year to analysis
    :return: save data slops, result and return result
    """
    df1 = df.loc[df.iloc[:, 0] == year].sort_values(by=[df.columns[0], df.columns[1]])

    tt = list()  # table with all slops
    result = pd.DataFrame(columns=('year', 'id', 'break_point', 'dir_m', 'activity', 'empty_mth'))
    row = 0
    counter = list()
    all_ = len(df1.iloc[:, 2].drop_duplicates())
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

            tt.append(df_main1.iloc[:, [0, 1, 5, 7]])

            '#check break trend'
            trend, dir_minus = check_series_trend(df_main1.iloc[:, 7], df_main1.iloc[:, 6])
            empty_m = check_empty_months(df_main1.iloc[:, 6])

            '#add row with result'
            result.loc[row] = [year, i, trend, dir_minus, len(df1.loc[df1.iloc[:, 2] == i]), empty_m]
            row += 1
            counter.append(i)

            '#print progress'
            if len(counter) % 10 == 0:
                print('Trend analysis: {}/{}'.format(len(counter), all_))
            else:
                pass
        else:
            pass
    all_slopes = pd.concat(tt)
    all_slopes.to_csv('allSlops.txt', sep=';', index=False, header=True)
    result.to_csv('breakTrend.txt', sep=';', index=False, header=True)
    print('files saved: allSlops.txt, breakTrend.txt')
    return result


def compare_sales(df0, df_result):
    y, m = max_year_month(df0)
    list_df = list()
    all_ = len(list(df_result.iloc[:, 1].drop_duplicates()))
    #tempL = list(['GR22AKA'])
    for i in df_result.iloc[:, 1].drop_duplicates():
        df_n = df0.loc[df0.iloc[:, 2] == i]
        df_main0 = pd.merge(table_id(df0, *list(df0.iloc[:, 0].drop_duplicates())),
                            df_n,
                            on='id',
                            how='left',
                            suffixes=('_df1', '_df2')).fillna(0)

        df1 = df_result.loc[df_result.iloc[:, 1] == i]  # df for break point
        break_point = int(df1.iloc[:, 2])

        sum_month = list()
        for year in df_main0.iloc[:, 0].drop_duplicates():
            df_year = df_main0.loc[(df_main0.iloc[:, 0] == year) & (df_main0.iloc[:, 1] <= m)]
            sum_month.append(df_year.iloc[:, 6].tail(abs(break_point)).sum())
        df_f = df1.copy()
        df_f['sales'] = sum_month[1] - sum_month[0]
        list_df.append(df_f)

        '#print progress'
        if len(list_df) % 10 == 0:
            print('Sales analysis: {}/{}'.format(len(list_df), all_))
        else:
            pass
    to_file = pd.concat(list_df)
    print('saving a file breakTrend')
    return to_file.to_csv('breakTrend.txt', sep=';', index=False, header=True)

def main():
    print("Wczytuje dane...")
    df0 = get_data()
    if df0.empty is False:
        years = list(df0.iloc[:, 0].drop_duplicates())
        print("Dostępne lata do analizy: {}".format(years))
        y = input('Dla którego roku zbadać dane?: ')

        try:
            slops = cumulative_slope_per_month(df0, int(y))
            ay = int(y)
        except ValueError:
            print("Wpisz odpowiedni rok i spróbuj ponowanie")

        if ay > 0 and min(years) == ay-1:
            q = input('Czy porównać sprzedaż dla tabeli trendów: ')

            if q == 't' or q == 'y':
                compare_sales(df0, slops)
                print("end")
            else:
                print("end")
        else:
            print("Data is missing a year back to compare sales.")
    else:
        pass



    #get_data().iloc[:, 0].drop_duplicates()
    #pass




#print(
    #compare_sales(get_data(), cumulative_slope_per_month(get_data(), 2019))
#cumulative_slope_per_month(get_data(), 2019)
    #table_id(get_data(), 2019)
main()
#print(get_data())
#)
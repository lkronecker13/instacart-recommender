
import datetime

# Orders in interval
def orders_around_interval_of_length(df_orders, current_date, interval_length):
    start_date = current_date - datetime.timedelta(days=interval_length)
    start_date = '20' + start_date.strftime('%y-%m-%d %H:%M:%S')
    print(start_date)
    end_date = current_date + datetime.timedelta(days=interval_length)
    end_date = '20' + end_date.strftime('%y-%m-%d %H:%M:%S')

    df_orders_sliced = df_orders.loc[start_date:end_date]
    return df_orders_sliced

# # Orders in week
def get_orders_in_week(df_orders, week_number):
    return df_orders.loc[df_orders['week_of_year'] == week_number]

# # Orders in Month
def get_orders_in_month(df_orders, month_number):
    year = 2016
    initial_date = '{}-{}'.format(str(year), month_number)
    next_month_string = get_next_time_unit(month_number)
    final_date = '{}-{}'.format(str(year), next_month_string)

    if int(month_number) == 12:
        df_slice = df_orders.loc[df_orders.index >= initial_date]
    else:
        df_slice = df_orders.loc[(df_orders.index >= initial_date) & (df_orders.index <= final_date)]

    return df_slice

# # Orders in day
def get_orders_in_day(df_orders, month_number, day_number):
    year = 2016
    df_orders = df_orders.set_index('order_date')
    initial_date = '{}-{}-{} 00:00:00'.format(str(year), month_number, day_number)
    final_date = '{}-{}-{} 23:00:00'.format(str(year), month_number, day_number)
    return df_orders.loc[(df_orders.index >= initial_date) & (df_orders.index <= final_date)]


def get_next_time_unit(time_unit):
    time_unit_string = str(int(time_unit)+1)
    if int(time_unit)<10:
        time_unit_string = '0'+str(int(time_unit)+1)
    return time_unit_string
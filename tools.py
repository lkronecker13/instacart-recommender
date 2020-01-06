import matplotlib.pyplot as plt
import pickle


def get_nth_group(df_group, group_number):
    # Use first one of the groupby keys to visualize one of the groups
    tmp_key = list(df_group.groups.keys())[group_number]
    group = df_group.get_group(tmp_key)
    print('Will get group using key: {}'.format(tmp_key))
    print('Group shape: {}'.format(group.shape))
    return group


def create_bar_chart(x, y, x_label, y_label):
    plt.xticks(rotation=90)
    plt.bar(x, y, label=x_label, align='center')
    plt.plot(x, y, color='purple', lw=2, marker='s')
    plt.legend()
    plt.grid()
    plt.ylabel(y_label);


def create_scatter_plot(x, y, x_label, y_label):
    plt.scatter(x, y, label=x_label)
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid()
    plt.ylabel(y_label);


def create_hist(data, bins, x_label, y_label):
    plt.hist(data, bins=bins, label=x_label)
    plt.legend()
    plt.grid()
    plt.ylabel(y_label);

### Persistence helpers

def save_sequences_to_disk(sequences, file_name):
    f = open('{}.pkl'.format(file_name), 'wb')
    pickle.dump(sequences, f)
    f.close()


def load_file(file_name):
    file = open(file_name, 'rb')
    object_file = pickle.load(file)
    file.close()
    return object_file


### Time processing helpers

def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

def days_in_month(month, year):
    number_of_days = None
    if month in ['September', 'April', 'June', 'November']:
        number_of_days = 30
    elif month in ['January', 'March', 'May', 'July', 'August','October','December']:
        number_of_days = 31
    elif month == 'February' and is_leap_year(year) == True:
        number_of_days = 29
    elif month == 'February' and is_leap_year(year) == False:
        number_of_days = 28
    return number_of_days

def day_of_week(day_of_week):
    day_name = None
    if day_of_week == 0:
        day_name = 'Sunday'
    elif day_of_week == 1:
        day_name = 'Monday'
    elif day_of_week == 2:
        day_name = 'Tuesday'
    elif day_of_week == 3:
        day_name = 'Wednesday'
    elif day_of_week == 4:
        day_name = 'Thursday'
    elif day_of_week == 5:
        day_name = 'Friday'
    elif day_of_week == 6:
        day_name = 'Saturday'
    return day_name

month_name = {'1':'January',
		'2':'February',
		'3':'March',
		'4':'April',
		'5':'May',
		'6':'June',
		'7':'July',
		'8':'August',
		'9':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}
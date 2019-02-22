import csv
import pandas as pd
import matplotlib.pyplot as plt

the_file = 'metro-bike-share-trip-data.csv'


def numbers_of_lines(file):  # Show how many lines are there
    with open(file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        i = 0
        for line in csv_reader:
            i += 1
        return i


def header(file):  # Shows the header of list
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file)
        header_list = []
        i = 0
        for line in csv_reader:
            header_list.append(line)
            if (i == 0):
                break
        return header_list


def average_duration_time(file):  # Shows the average time for all entries
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)
        total = 0
        for row in reader:
            duration = row['Duration']
            total = total + int(duration)
        return (total / numbers_of_lines(file)) / 60


def lat_long_interval(file):  # Shows the interval of lattitude and longitude
    reader = pd.read_csv(file, dtype={"Starting Station Latitude": float, "Starting Station Longitude": float},
                         low_memory=False)
    reader = reader[reader['Starting Station Latitude'] != 0]
    start_interval = reader['Starting Station Latitude'].min()
    end_interval = reader['Starting Station Longitude'].min()
    print("The interval is: " + str(start_interval) + " : " + str(end_interval) + "\n")


def number_of_bikes(file):  # Shows the number of bikes used
    reader = pd.read_csv(file, low_memory=False)
    bikes = reader['Bike ID'].value_counts(dropna=False)  # shows how many bikes are from one id
    count = reader['Bike ID'].nunique()
    return count


def group_plan_duration(file):  # Group data by Plan Duration and duration and takes the average duration
    reader = pd.read_csv(file, low_memory=False)
    plan_duration = reader.groupby('Plan Duration')['Duration'].mean()
    to_seconds = plan_duration / 60
    return to_seconds


def group_trip_route(file):  # Group data by Trip Route Category and takes the average duration
    reader = pd.read_csv(file, low_memory=False)
    trip_route = reader.groupby('Trip Route Category')['Duration'].mean()
    to_seconds = trip_route / 60
    return to_seconds


def group_passholder(file):  # Group data by Passholder Type and takes the average duration
    reader = pd.read_csv(file, low_memory=False)
    group_pass = reader.groupby('Passholder Type')['Duration'].mean()
    to_seconds = group_pass / 60
    return to_seconds


def group_by_all(file):  # Group data by Trip Route Category,Passholder type, Plan duration and takes the average duration
    reader = pd.read_csv(file, low_memory=False)
    group_all = reader.groupby(['Passholder Type', 'Plan Duration', 'Trip Route Category'])['Duration'].mean()
    to_seconds = group_all / 60
    return to_seconds


def show_plot_bar(func):  # Show simple plot bar
    ax = func.plot(kind='bar', figsize=(10, 7), fontsize=8)
    for i in ax.patches:
        ax.text(i.get_x() + 0.2, i.get_height() / 2, str(round(int(i.get_height()))), fontsize=15)
    ax.set_ylabel("Average Duration(min)", fontsize=14);
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.show()


def recreate_plot(file):
    reader = pd.read_csv(file, low_memory=False)
    group1 = (reader.groupby(['Passholder Type', 'Trip Route Category'])['Duration'].mean()) / 60
    axes = group1.unstack('Trip Route Category').plot(kind='bar', figsize=(14, 6), subplots=True, layout=(1, 2),
                                                      sharey=True)
    colors = plt.cm.jet(pd.np.linspace(0, 1, len(group1)))
    for ax in axes.flat:
        # print(ax)
        for i, bars in enumerate(ax.patches):
            bars.set_color(colors[i])
            # print(bars)
            ax.text(bars.get_x() + 0.18, bars.get_height() / 2, str(round(float(bars.get_height()))), fontsize=12)
            ax.grid(True)
            ax.set_axisbelow(True)
            ax.set_ylabel("Average Duration(min)", fontsize=14)
    print(group1)
    plt.show()

def sum_of(file):
    reader = pd.read_csv(file, low_memory=False)
    group1 = (reader.groupby(['Passholder Type'])['Duration'].sum())/3600
    ax = group1.plot(kind='bar', figsize=(10, 7), fontsize=8)
    for i in ax.patches:
        ax.text(i.get_x() + 0.08, i.get_height() / 2, str(round(int(i.get_height()))), fontsize=15)
    ax.set_ylabel("Sum Duration(hour)", fontsize=14);
    ax.grid(True)
    ax.set_axisbelow(True)
    plt.show()


print("The header is: \n" + str(header(the_file)) + "\n")
print("The numbers of lines: " + str(numbers_of_lines(the_file)) + "\n")
print("The average duration is: %.2f" % average_duration_time(the_file)+ "\n")
lat_long_interval(the_file)
print("The numbers of different bikes used: " + str(number_of_bikes(the_file))+ "\n")
print(str(group_plan_duration(the_file))+ "\n")
print(str(group_trip_route(the_file))+ "\n")
print(str(group_passholder(the_file))+ "\n")
print(group_by_all(the_file))

show_plot_bar(group_plan_duration(the_file))
show_plot_bar(group_trip_route(the_file))
show_plot_bar(group_passholder(the_file))
show_plot_bar(group_by_all(the_file))
recreate_plot(the_file)
sum_of(the_file)
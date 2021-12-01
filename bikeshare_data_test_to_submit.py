import csv
import time
from datetime import datetime
from collections import Counter

# Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''

    print("Hello! Let's explore some US bikeshare data!")
    while True:
        city = str(input('Would you like to see data for Chicago, New York, or Washington?\n'))

        if  city.lower() in "new york":
            city = new_york_city
            break
        elif city.lower() in "washington":
            city = washington
            break
        elif city.lower() in "chicago":
            city = chicago
            break
        else:
            print("\nSorry! That's not a valid input.")
            continue
    with open(city,'r') as city_1:
        city_file = csv.DictReader(city_1)
        city_reader = [row for row in city_file]

    return city_reader


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) Specified time filter
    '''

    while True:
        time_period = input('Would you like to filter the data by month, day, or not at all? '
                            'Type "none" for no time filter.\n')
        if time_period.lower() in "month":
            time_period = "month"
            break
        elif time_period.lower() in "day":
            time_period = "day"
            break
        elif time_period.lower() in "none":
            time_period = "none"
            break
        else:
            print("\nSorry, that's not a valid input!")
            continue
    return time_period


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (int) Specified month
    '''

    month_number_list = [1, 2, 3, 4, 5, 6]
    while True:
        month = int(input('\nWhich month? January, February, March, April, May, or June?\n'
                          'Please enter the month as an integer.'))
        if month not in month_number_list:
            print("\nSorry! That's not a valid input.")
        else:
            break
    return month


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) Specified day of the week
    '''

    day_number_list = [1, 2, 3, 4, 5, 6, 7]
    while True:
        day = int(input('\nWhich day? Please type your response as one of the following:\n'
                        '\nPlease enter the month as an integer from 1 to 7.'))
        if day not in day_number_list:
            print("\nSorry! That's not a valid input.")
        else:
            break
    return day


def popular_month(city_reader):
    '''Calculates the most popular month for journeys

    Args:
        city_reader
    Returns:
        (dict) Number of time each month appeared in a journey for start time
    '''

    month_list = ["January", "February", "March", "April", "May", "June"]
    month_counts = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}

    for row in city_reader:

        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        pop_month_1 = str(dtetme.month)
        month_counts[pop_month_1] += 1

    most_popular_month = int(max(month_counts, key=month_counts.get))
    print("The most popular month was " + month_list[most_popular_month - 1])

    return month_counts


def popular_day(city_reader, time_period, month):
    '''Calculates the most popular day of the week for journeys

    Args:
        city_reader, time_period, month
    Returns:
        (dict) Number of time each day appeared in a journey for start time
    '''

    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')

        if time_period == "month" and dtetme.month == month:
            pop_day_1 = str(dtetme.isoweekday())
            day_counts[pop_day_1] += 1

        elif time_period != "month":
            pop_day_1 = str(dtetme.isoweekday())
            day_counts[pop_day_1] += 1

    most_popular_day = int(max(day_counts, key=day_counts.get))
    print("The most popular day was " + day_list[most_popular_day - 1])

    return day_counts


def popular_hour(city_reader, time_period, month, day):
    '''Calculates the most popular hour for journeys

    Args:
        city_reader, time_period, month, day
    Returns:
        (dict) Number of time each hour appeared in a journey for start time
    '''

    hour_counts = dict.fromkeys(range(0, 24), 0)

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        pop_hour_1 = dtetme.hour

        if time_period == "month" and dtetme.month == month:
            hour_counts[pop_hour_1] += 1

        elif time_period == "day" and dtetme.isoweekday() == day:
            hour_counts[pop_hour_1] += 1

        else:
            hour_counts[pop_hour_1] += 1

    most_popular_hour = int(max(hour_counts, key=hour_counts.get))
    print("The most popular hour was " + str(most_popular_hour) + ":00 hours")

    return hour_counts


def trip_duration(city_reader, time_period, month, day):
    '''Calculates the most total and average trip duration for journeys

    Args:
        city_reader, time_period, month, day
    Returns:
        (int) Total trip duration in seconds
        (int) Average trip duration in seconds
    '''

    total_duration = 0
    trip_count = 0

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        duration = row['Trip Duration']

        if time_period == "month" and dtetme.month == month:
            total_duration += int(float(duration))
            trip_count += 1

        elif time_period == "day" and dtetme.isoweekday() == day:
            total_duration += int(float(duration))
            trip_count += 1

        else:
            total_duration += int(float(duration))
            trip_count += 1

    average_duration = total_duration/trip_count
    print("The total trip duration in seconds was: " + str(total_duration))
    print("The average trip duration in seconds was: " + str(average_duration))

    return total_duration, trip_count


def popular_stations(city_reader, time_period, month, day):
    '''Calculates the most popular start and end stations

    Args:
        city_reader, time_period, month, day
    Returns:
        (str) Most popular start station
        (str) Most popular end station
    '''

    start_station_list = []
    end_station_list = []

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        start_station = row['Start Station']
        end_station = row['End Station']

        if time_period == "month" and dtetme.month == month:
            start_station_list.append(start_station)
            end_station_list.append(end_station)

        elif time_period == "day" and dtetme.isoweekday() == day:
            start_station_list.append(start_station)
            end_station_list.append(end_station)

        else:
            start_station_list.append(start_station)
            end_station_list.append(end_station)

    Counter(start_station_list)
    Counter(end_station_list)
    print("The most popular start station is " + Counter(start_station_list).most_common(1)[0][0])
    print("The most popular end station is " + Counter(end_station_list).most_common(1)[0][0])

    return Counter(start_station_list), Counter(end_station_list)


def popular_trip(city_reader, time_period, month, day):
    '''Calculates the most popular trip from start station to end station

    Args:
        city_reader, time_period, month, day
    Returns:
        (str) Most popular trip from start to end station
    '''

    journey_list = []

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        start_station = row['Start Station']
        end_station = row['End Station']
        journey = (start_station + " to " + end_station)

        if time_period == "month" and dtetme.month == month:
            journey_list.append(journey)

        elif time_period == "day" and dtetme.isoweekday() == day:
            journey_list.append(journey)

        else:
            journey_list.append(journey)

    Counter(journey_list)
    print("The most popular start station is from " + Counter(journey_list).most_common(1)[0][0])

    return Counter(journey_list)


def users(city_reader, time_period, month, day):
    '''Calculates the number of different types of users - customers, subscribers and dependents

    Args:
        city_reader, time_period, month, day
    Returns:
        (int) The number of customers
        (int) The number of subscribers
        (int) The number of dependents
    '''

    user_type = {'Customer': 0, 'Subscriber': 0, 'Dependent': 0, '': 0}

    for row in city_reader:
        dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        user = row['User Type']

        if time_period == "month" and dtetme.month == month:
            user_type[user] += 1

        elif time_period == "day" and dtetme.isoweekday() == day:
            user_type[user] += 1

        else:
            user_type[user] += 1

    customer_number = user_type['Customer']
    subscriber_number = user_type['Subscriber']
    dependent_number = user_type['Dependent']
    print("The number of customers was " + str(customer_number))
    print("The number of subscribers was " + str(subscriber_number))
    print("The number of dependents was " + str(dependent_number))

    return customer_number, subscriber_number, dependent_number


def gender(city_reader, time_period, month, day):
    '''Calculates the number of users of different gender if information is available

    Args:
        city_reader, time_period, month, day
    Returns:
        none.
    '''

    gender_dict = {'Male': 0, 'Female': 0, '': 0}

    try:  # As Washington has no gender data
        for row in city_reader:
            dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
            user_gender = row['Gender']

            if time_period == "month" and dtetme.month == month:
                gender_dict[user_gender] += 1

            elif time_period == "day" and dtetme.isoweekday() == day:
                gender_dict[user_gender] += 1

            else:
                gender_dict[user_gender] += 1

        male_number = gender_dict['Male']
        female_number = gender_dict['Female']
        print("The number of male users was " + str(male_number))
        print("The number of female users was " + str(female_number))
    except KeyError:
        print("No gender information available.")


def birth_years(city_reader, time_period, month, day):
    '''Calculates the earliest, most  recent and most popular birth years if information available

    Args:
        city_reader, time_period, month, day
    Returns:
        none.
    '''

    birth_date_list = []

    for row in city_reader:
        try:
            dtetme = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
            birth_date = int(float(row['Birth Year']))

            if time_period == "month" and dtetme.month == month:
                birth_date_list.append(birth_date)

            elif time_period == "day" and dtetme.isoweekday() == day:
                birth_date_list.append(birth_date)

            else:
                birth_date_list.append(birth_date)

        except KeyError:
            pass

        except ValueError:
            pass
    try:
        min_year = min(birth_date_list)
        max_year = max(birth_date_list)
        most_common_year = Counter(birth_date_list).most_common(1)[0][0]
        print("The earliest birth year is: " + str(min_year))
        print("The most recent birth year is: " + str(max_year))
        print("The most popular birth year is: " + str(most_common_year))

    except:
        print("No birth year information available.")


def display_data(city_reader):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        none.
    '''

    display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. ')

    row_list = [1, 2, 3, 4, 5]

    while 'yes' in display:

        try:
            for number in row_list:
                row = city_reader[number]

                print("Start Time: " + row['Start Time'] + ",   End Time: " + row['End Time']
                      + ",   Trip Duration (in seconds): " + row['Trip Duration']
                      + ",   Start Station: " + row['Start Station']
                      + ",   End Station: " + row['End Station']
                      + ",   User Type: " + row['User Type']
                      + ",   Gender: " + row['Gender']
                      + ",   Birth Year: " + row['Birth Year'])

            row_list = [number + 5 for number in row_list]
            print(row_list)

        except KeyError:
            for number in row_list:
                row = city_reader[number]

                print("Start Time: " + row['Start Time'] + ",   End Time: " + row['End Time']
                      + ",   Trip Duration (in seconds): " + row['Trip Duration']
                      + ",   Start Station: " + row['Start Station']
                      + ",   End Station: " + row['End Station']
                      + ",   User Type: " + row['User Type'])

            row_list = [number + 5 for number in row_list]
            # print(row_list)

        display = input('Would you like to view more individual trip data?'
                        'Type \'yes\' or \'no\'. ')


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''

    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    month = day = None
    if time_period == "month":
        month = get_month()
    elif time_period == "day":
        day = get_day()

    print('Calculating the first statistic...')
    start_time = time.time()

    # What is the most popular month for start time?
    if time_period == 'none':
        pop_month = popular_month(city)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        pop_day = popular_day(city, time_period, month)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular hour of day for start time?

    pop_hour = popular_hour(city, time_period, month, day)
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    duration = trip_duration(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    pop_station = popular_stations(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    pop_strip = popular_trip(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    user_count = users(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    gender_count = gender(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the earliest, most recent, and most popular birth years?
    birth_year = birth_years(city, time_period, month, day)

    print("That took %s seconds." % (time.time() - start_time))

    #Display five lines of data at a time if user specifies that they would like to
    display_data(city)

    # Restart?
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
    statistics()
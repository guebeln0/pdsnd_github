import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york', 'washington']
    while True:
        city = input('\nYou can explore Chicago, New York or Washington. Type the city name you would like to explore?').lower()
        if city in cities:
            break
        else:
            print('I didn\'t understand that, {} is not a valid city name. Please check your spelling\n'.format(city.title()))
            continue

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('\nWhich month are you interested in?\nPlease type all or one of the following month January, February, March, April, May or June').lower()
        if month in months:
            break
        else:
            print('I didn\'t understand that, {} is not a valid month. Please check your spelling\n'.format(month.title()))
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('\nWhich day(s) are you interested in?\nPlease type all or Monday, Tuesday, Wednesday, Thurday, Friday, Saturday or Sunday ').lower()
        if day in days:
            break
        else:
            print('I didn\'t understand that, {} is not a day. Please check your spelling\n'.format(day.title()))
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    # New column month 1 = January ... 6 = June
    df['month'] = df['Start Time'].dt.month

    # New column day_of_week 0 = Monday ... 6 = Sunday
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
         days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
         day = days.index(day)
         df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = df['month'].mode()[0]
    print('Most common month: ', months[common_month-1])

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', days[common_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].value_counts().idxmax()
    print('Most common hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most used start station: ", popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['Start Station'].mode()[0]
    print("Most used end station: ", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)[:1]
    print("Most travels where made between:\n", popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the travel time in minutes
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time in the period: {:.0f} min'.format(total_travel_time / 60))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time in the period: {:.2f} min'.format(mean_travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())


    # TO DO: Display counts of gender

    # Washington has no information on its users gender or date of birth
    if city != 'washington':
        # I decided to ignore the unknown / NaN values and assume the percentage is evenly distrubed
        # male is the count of male gender
        # female is the count of female gender
        male,female = df['Gender'].value_counts()[['Male','Female']]
        # The percentage is calculated based on know user gender
        print("In our selection we have subscribers:\n",
        male, "men or {:.2f}".format(100*male / (male+female)), '%\n',
        female, 'women',  'or',  "{:.2f}".format(100*female / (male+female)), '%')

        # TO DO: Display earliest, most recent, and most common year of birth
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common_birthyear = df['Birth Year'].mode()[0]

        print("\nOur youngest suscriber was born in {:.0f}\nOur oldest subscriber was born in {:.0f}\nMost subscriber were born in {:.0f},".format(youngest, oldest, common_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # Displays 5 raws of data at the time and prompt the user if they want to see more
    j = 0
    print(df.size)
    while j < df.size + 5:
        print(df[j:j+5])
        raw_data = input('\nWould you like to see more? Enter yes or no.\n')
        if raw_data == 'yes':
            j+= 5
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        raw_data_request = input('\nWould you like to see some of the raw data for trip information? Enter yes or no.\n')
        if raw_data_request.lower() == 'yes':
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # ask user to input a specific city
    city = input("\nWhich city would you like to see data about?: chicago, new york, washington \n").lower()
    # if user entered a wrong choice, program ask him to choose a valid choice
    while (city not in CITY_DATA):
        print("enter a valid choice")
        city = input("Which city would you like to see data about?: chicago, new york, washington \n").lower()

    # ask user to input a specific month
    month = input('\nWhich month would you like to see data about?: all, january, february, ... , june \n').lower()
    # if user entered a wrong choice, program ask him to choose a valid choice
    while (month != 'all' and month not in months):
        print('please enter a valid choice')
        month = input('Which month would you like to see data about?: all, january, february, ... , june \n').lower()

    # ask user to input a specific month
    day = input('\nWhich day would you like to see data about?: all, monday, tuesday, ... sunday \n').lower()
    # if user entered a wrong choice, program ask him to choose a valid choice
    while (day != 'all' and day not in days):
        print('please enter a valid choice')
        day = input('Which day would you like to see data about?: all, monday, tuesday, ... sunday \n').lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data from spreadsheet
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # create new columns for analysis
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df["Start Time"].dt.day_name()
    df["day_of_month"] = df['Start Time'].dt.day
    df['hour'] = df["Start Time"].dt.hour

    # if user does not choose all, we filter data as he wanted
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # if user does not choose all, we filter data as he wanted
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(most_common_month))

    # display the most common day of week
    most_common_Dweek = df['day_of_week'].mode()[0]
    # display the most common day of month
    most_common_Dmonth = df["day_of_month"].mode()[0]
    print('The most common day of week is: {}'.format(most_common_Dweek))
    print('The most common day of month is: {}'.format(most_common_Dmonth))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("The most common start station is: {}".format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("The most common end station is: {}".format(end_station))

    # display most frequent combination of start station and end station trip
    common_start_end = (df["Start Station"] + '-' + df["End Station"]).mode()[0]
    print("The most frequent combination of start station and end station trip is: {}".format(common_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    counts = df['Trip Duration'].sum()
    print("Total travel time: {}".format(counts))

    # display mean travel time
    avg = df['Trip Duration'].mean()
    print("mean travel time: {}".format(avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].value_counts()
    print("counts of user types: \n{}\n".format(user_type))

    # Display counts of gender
    # washington dataset has no gender, so if the user entered it
    # we throw an excecption: gender is not available
    try:
        gen = df["Gender"].value_counts()
        print("counts of user gender: \n{}\n".format(gen))
    except:
        print('No gender available in this data\n')

    # Display earliest, most recent, and most common year of birth
    # washington dataset has no birth year, so if the user entered it
    # we throw an excecption: birth year is not available
    try:
        early = int(df['Birth Year'].min())
        print("earliest year of birth: {}".format(early))
        recent = int(df['Birth Year'].max())
        print("most recent year of birth: {}".format(recent))
        most = int(df['Birth Year'].mode()[0])
        print("most common year of birth: {}".format(most))
    except:
        print('No birth year available in this data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def show_data(df):
    """show a sample of data"""
    ask = input("Do you want to see a sample of data?: yes or no\n").lower()
    counter = 5
    while ask == "yes":
        print(df.head(counter))
        print('-'*40)
        counter += 5
        ask = input("Do you want to see more data?: yes or no\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        print('-'*40)
        if restart.lower() != 'yes':
            print("Thanks for using my program!")
            break

if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAYS_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input('\nPlease enter a city (Chicago, New York City, or Washington): ').lower()
            
            # check if the city is in our dataset
            if city in CITY_DATA:
                break
            
            # if the city is not valid, alert the user before re-requesting input
            print('Invalid input. Please try again.')

        except:
            print('Invalid input. Please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nPlease enter a month to filter on (January, February, March, April, May, June). If you do not wish to filter by month, enter "all": ').lower()
            
            # if month is 'all' or if the month is a valid month in the list MONTHS (0-Jan to 5-Jun)
            if month == 'all' or month in MONTHS[0:6]:
                break
            
            # if the month is not valid, alert the user before re-requesting input
            print('Invalid input. Please try again.')
        
        except:
            print('Invalid input. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nPlease enter a day of the week to filter on (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). If you do not wish to filter by day, enter "all": ').lower()

            # if day is 'all' or if the day is a valid day in the list DAYS_WEEK
            if day == 'all' or day in DAYS_WEEK:
                break
            
            # if the month is not valid, alert the user before re-requesting input
            print('Invalid input. Please try again.')
        
        except:
            print('Invalid input. Please try again.')

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day of the week: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (round(time.time() - start_time,3)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station for a trip: {}'.format(pd.Series(df['Start Station'] + ' -- ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (round(time.time() - start_time,3)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {} seconds'.format(round(df['Trip Duration'].sum(),1)))

    # display mean travel time
    print('Mean travel time: {} seconds'.format(round(df['Trip Duration'].mean(),1)))

    print("\nThis took %s seconds." % (round(time.time() - start_time,3)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Summary of user types:\n{}'.format(df['User Type'].value_counts()))

    if 'Gender' in df.columns:
        # Display counts of gender
        print('\nSummary of genders:\n{}'.format(df['Gender'].value_counts()))

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('\nEarliest birth year: {}\nMost recent birth year: {}\nMost common birth year: {}'.format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (round(time.time() - start_time,3)))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data from the bikeshare df, printing 5 rows at a time until the user requests to stop."""

    start = 0
    stop = 5

    while True:
        # if the index start variable is greater than or equal to the length, we have reached the end of the df
        if start >= len(df):
            print('\nReached the end of the dataset.')
            break
        
        # if the index stop variable is greater than or equal to the length, we have less than 5 rows left to print, so print to the end of the df
        elif stop >= len(df):
            pd.set_option('display.max_columns',200)
			print(df.iloc[start:,:])
            print('\nReached the end of the dataset.')
            break

        else:
            pd.set_option('display.max_columns',200)
			print(df.iloc[start:stop,:])
        
            # ask user whether they would like to see 5 more rows of raw data or not
            restart = input('\nWould you like to see 5 more rows? Enter yes or no.\n').lower()
            if restart != 'yes':
                break
            
            # change index start/stop variables to look at the next 5 rows
            start += 5
            stop += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_raw_data = input('\nWould you like to view the raw data? Enter yes or no.\n').lower()
        if view_raw_data == 'yes':
            display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

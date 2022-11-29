import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data! \n\nYou will be asked for some inputs in a second, \nif you get asked again by this program, your answer \nwas not valid. Do be mindful of your spelling and \nmake sure you have entered a month/day/city \nfrom the given options.\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower().strip() not in ['chicago','new york city','washington']:
        city = input('\nEnter the city that you are interested in from Chicago, \nNew York City and Washington:\n')

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower().strip() not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        month = input('\nEnter the month from Jan-Jun for which you would \nlike to see data, or just type "all" to see all \navailable data:\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.title() not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']:
        day = input('\nEnter the day of the week you are interested in \nfrom or just type "all" to see all available data:\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze, options are Chicago, New York  City or Washington
        (str) month - name of the month to filter by, or "all" to apply no month filter, data only available for January-June
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    filename = CITY_DATA[city.lower().strip()]

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month.lower().strip() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_no = months.index(month.lower().strip())+1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month_no]
    elif month == 'all':
        df=df
    
    # filter by day of week if applicable
    if day.title() != 'All':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    elif day.title() == 'All':
        df=df

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months_dic= {   '1':'January',
                    '2':'February',
                    '3':'March',
                    '4':'April',
                    '5':'May',
                    '6':'June'}
    print("The most popular month was: {}".format(months_dic[str(popular_month)]))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of the week was: {}".format(popular_day))


    # display the most common start hour

    hours = df.groupby('hour').size().to_frame('size').sort_values('size',ascending=False)
    hours['hours'] = hours.index
    popular_hour = hours.iloc[0,1]
    print("The most Frequent Start Hour was: {}".format(popular_hour))


    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: {}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['journey'] = df['Start Station'] +' to \n'+ df['End Station']
    popular_journey = df['journey'].mode()[0]
    print("The most travelled journey was from {}".format(popular_journey))

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_time = df['Trip Duration'].sum()
    total_time = pd.Timedelta(seconds = total_time)

    
    print('The total time of all the journeys travelled was {}.'.format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_time = pd.Timedelta(seconds = mean_time)
    
    print('The total mean journey time was {}'.format(mean_time))
 

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame('User counts')
    print('Types and numbers of users:')
    print(user_types)
    try:
        # Display counts of gender
        gender = df['Gender'].value_counts().to_frame('Gender counts')
        gender_na =df ['Gender'].isna().sum()

        undisclosed_row = [{'Gender counts': gender_na}]
        new_table = pd.DataFrame(undisclosed_row, index = ['Undisclosed'])
        gender = pd.concat([gender,new_table])

        print('The users\' breaks down as follows:\n')
        print(gender)
        common_year = int(df['Birth Year'].mode()[0])
        first_year = int(df['Birth Year'].min())
        last_year = int(df['Birth Year'].max())
        print('\nThe oldest users in the dataset were born in {}, the youngest in {}, \nwhilst the most common year of birth among users was {}.'.format(first_year,last_year,common_year))

    except KeyError:
        print('There is no gender or birth year for Washington for Washington')

        # Display earliest, most recent, and most common year of birth
    
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    while True:
        print('\nHere is a sample of the raw data:')
        print(df.sample(5))
        view_more = input("Do you want to see more raw data? Type 'yes' to see more:\n")
        if view_more != "yes":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# list of days, months & cities
months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
cities = ['chicago', 'new york city', 'washington']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city, month and day 
    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington?\n").lower()
        city = city.lower()
        if city.lower() not in cities:
            print("\nPlease enter the correct city from the following: {}".format(cities))
            continue
        else:
            break

    while True:
        month = input("\nTo filte data by month, please enter month name from January to June. If not, enter all.\n")
        month = month.lower()
        if month.lower() not in months:
            print("\nPlease enter the correct month from the following: {}".format(months))
            continue
        else:
            break

    while True:
        day = input("\nTo filter data by day, please enter name of the day Sunday to Saturday. If not, enter all.\n")
        day = day.lower()
        if day.lower() not in days:
            print("\nPlease enter the correct day from the following: {} ".format(days))
            continue
        else:
            break

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

    # extract month and day of week 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 

    # filter by month 
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day 
    if day != 'all':
        day_of_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        df = df[df['day_of_week'] == day.title()] 

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Start Time'].dt.month_name()
    common_month = common_month.mode()[0]
    print('The Most Common Month Is: \n', common_month)

    # display the most common day of week
    common_day_of_week = df['Start Time'].dt.day_name()
    common_day_of_week = common_day_of_week.mode()[0]
    print('The Most Common Day of The Week Is: \n', common_day_of_week)

    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour
    common_start_hour = common_start_hour.mode()[0]

    print('The Most Common Starting Hour Is: \n', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The Most Common Starting Station Is: \n", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The Most Common Ending Station Is: \n", common_end_station)

    # display most frequent combination of start station and end station trip
    combos = df.groupby(['Start Station', 'End Station']).size().sort_values().tail(1)
    print('Combination of Common Start & End Station Is:\n', combos)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The Total Travel Time Is: \n", total_travel_time)

    # display mean travel time
    mean_travel = round(df['Trip Duration'].mean(), 1) 
    print("The Mean Travel Time Is: \n", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()   
    print("Displaying User Type Counts:\n", user_types)

    # Display counts of gender
    if city != 'washington': # wash doesn't have Gender
        gender = df['Gender'].value_counts()      
        print("Displaying Gender Counts:\n", gender)

    # Display earliest, most recent, and most common year of birth
    if city != 'washington': 
        earlies_birth_year = df['Birth Year'].min()       
        print("The Earlies Year of Birth Is:\n", int(earlies_birth_year))

        recent_birth_year = df['Birth Year'].max()       
        print("The Most Recent Year of Birth Is:\n", int(recent_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]        
        print("The Most Common Year of Birth Is:\n", int(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        # display_raw_data(df)
        
        while True:
            restart = input('\nWould you like to restart? Please enter yes or no.\n').lower() 
            if restart in ('yes', 'no'):
                break
            print("\nI do not recognize what you entered. Please enter 'yes' or 'no'!\n") 
        if restart == 'yes':
            continue
        else:
            print("\nI hope you enjoed viewing US Bikeshare Data! \nGood bye now!") 
            break
           

if __name__ == "__main__":
	main()

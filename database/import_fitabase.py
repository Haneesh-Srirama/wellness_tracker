import os
import pandas as pd
import sqlite3

DB_NAME = 'wellness_tracker.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def read_and_combine(filename):
    """Search the base directory for the file and concatenate them."""
    base_dir = '.'
    dfs = []
    for root, dirs, files in os.walk(base_dir):
        if filename in files and 'Fitabase Data' in root:
            file_path = os.path.join(root, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)
            
    if not dfs:
        return pd.DataFrame()
        
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def import_fitabase_data():
    print("Loading datasets...")
    # Activity (Steps, Calories)
    activity_df = read_and_combine('dailyActivity_merged.csv')
    if not activity_df.empty:
        # Convert ActivityDate to standard Date fmt string YYYY-MM-DD
        activity_df['Date'] = pd.to_datetime(activity_df['ActivityDate']).dt.strftime('%Y-%m-%d')
        activity_df = activity_df[['Id', 'Date', 'TotalSteps', 'Calories', 'SedentaryMinutes']]
    
    # Sleep
    sleep_df = read_and_combine('sleepDay_merged.csv')
    if not sleep_df.empty:
        sleep_df['Date'] = pd.to_datetime(sleep_df['SleepDay']).dt.strftime('%Y-%m-%d')
        # We need TotalMinutesAsleep in hours
        sleep_df['SleepHours'] = sleep_df['TotalMinutesAsleep'] / 60.0
        # sleep records might have duplicates for a day if taking multiple naps, group by Date and Id
        sleep_df = sleep_df.groupby(['Id', 'Date'], as_index=False)['SleepHours'].sum()
    
    # Heart Rate
    hr_df = read_and_combine('heartrate_seconds_merged.csv')
    if not hr_df.empty:
        hr_df['Date'] = pd.to_datetime(hr_df['Time']).dt.strftime('%Y-%m-%d')
        # Average heart rate per day
        hr_df = hr_df.groupby(['Id', 'Date'], as_index=False)['Value'].mean()
        hr_df.rename(columns={'Value': 'HeartRate'}, inplace=True)
    
    print("Merging metrics...")
    # Merge them all
    merged_df = activity_df
    if not sleep_df.empty:
        merged_df = pd.merge(merged_df, sleep_df, on=['Id', 'Date'], how='left')
    else:
        merged_df['SleepHours'] = 8.0 # default if missing
        
    if not hr_df.empty:
        merged_df = pd.merge(merged_df, hr_df, on=['Id', 'Date'], how='left')
    else:
        merged_df['HeartRate'] = 75 # default
        
    # Fill NAs
    merged_df['SleepHours'] = merged_df['SleepHours'].fillna(merged_df['SleepHours'].mean())
    merged_df['HeartRate'] = merged_df['HeartRate'].fillna(merged_df['HeartRate'].mean())
    merged_df['TotalSteps'] = merged_df['TotalSteps'].fillna(0)
    merged_df['Calories'] = merged_df['Calories'].fillna(0)
    merged_df['SedentaryMinutes'] = merged_df['SedentaryMinutes'].fillna(0)
    
    # Generate Mock values for Screen Time and Productivity
    merged_df['ScreenTime'] = (merged_df['SedentaryMinutes'] / 60.0) * 0.4 # assume 40% of sedentary is screen time
    
    # Productivity (1-10) -> scale based on Sleep and active steps
    def calc_prod(row):
        base = 5.0
        # sleep 7-9 hours is optimal (+2)
        if 7 <= row['SleepHours'] <= 9:
            base += 2
        elif row['SleepHours'] < 6:
            base -= 2
        # steps > 8000 is good (+2)
        if row['TotalSteps'] > 8000:
            base += 2
        elif row['TotalSteps'] < 3000:
            base -= 1
        return min(10, max(1, int(base)))
        
    merged_df['Productivity'] = merged_df.apply(calc_prod, axis=1)

    print(f"Total merged records: {len(merged_df)}")
    
    # Insert to DB
    print("Saving to database...")
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ensure users exist
    unique_users = merged_df['Id'].unique()
    for uid in unique_users:
        cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (str(uid),))
    
    # Insert Metrics
    for index, row in merged_df.iterrows():
        username = str(row['Id'])
        date_str = row['Date']
        steps = int(row['TotalSteps'])
        calories = int(row['Calories'])
        heart_rate = int(row['HeartRate'])
        screen_time = float(row['ScreenTime'])
        sleep_hours = float(row['SleepHours'])
        productivity = int(row['Productivity'])
        
        cursor.execute('''
            INSERT INTO daily_metrics (username, date, steps, calories, heart_rate, screen_time, sleep_hours, productivity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username, date) DO UPDATE SET
                steps=excluded.steps,
                calories=excluded.calories,
                heart_rate=excluded.heart_rate,
                screen_time=excluded.screen_time,
                sleep_hours=excluded.sleep_hours,
                productivity=excluded.productivity
        ''', (username, date_str, steps, calories, heart_rate, screen_time, sleep_hours, productivity))
        
    conn.commit()
    conn.close()
    print("Fitabase Data successfully loaded into SQLite.")

if __name__ == "__main__":
    import_fitabase_data()

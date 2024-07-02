import pandas as pd
import os
from datetime import datetime, timedelta

def preprocess_data():
    # Load the combined data and tax data
    combined_df = pd.read_csv('/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/combined_data.csv')
    combined_df['room_id'] = combined_df['room_id'].astype(str)
    tax_data = pd.read_csv('/Users/zhangshuyi/Desktop/airbnb_scrape/Tax.csv')

    # Remove rows with empty 'daily original price'
    combined_df.dropna(subset=['daily_price'], inplace=True)

    # Fill 'daily_original_price' with the highest value of 'daily_price' for rows with the same 'room_id' if it is missing
    combined_df['daily_original_price'] = combined_df.groupby('room_id')['daily_price'].transform(
        lambda x: x.fillna(x.max()) if x.max() is not None else x
    )

    # Create 'Tax' and 'Lodging Tax' columns
    combined_df = combined_df.merge(tax_data[['state', 'Total State Tax']], how='left', on='state')

    # Create 'Bundle' column
    combined_df['Bundle'] = combined_df['duration'].apply(lambda x: 1 if x > 1 else 0)

    #  Create 'check-out date' column
    combined_df['check-in date'] = pd.to_datetime(combined_df['start_date'])
    combined_df['check-out date'] = combined_df['check-in date'] + pd.to_timedelta(combined_df['duration'], unit='D')

    # Create 'Weekend' and 'Holiday' columns
    def is_weekend_or_holiday(check_in, check_out):
        holidays = []  # Add holiday dates here as datetime objects
        day_count = (check_out - check_in).days + 1
        for single_date in (check_in + timedelta(n) for n in range(day_count)):
            if single_date.weekday() >= 5 or single_date in holidays:  # Saturday=5, Sunday=6
                return 1
        return 0

    combined_df['Weekend'] = combined_df.apply(lambda row: is_weekend_or_holiday(row['check-in date'], row['check-out date']), axis=1)
    combined_df['Holiday'] = combined_df['Weekend']  # Assuming holidays are included in the weekend check

    numerical_columns = combined_df.select_dtypes(include=['number']).columns
    non_numerical_columns = combined_df.select_dtypes(exclude=['number']).columns

    aggregated_df = combined_df.groupby(['room_id', 'start_date', 'scrape_date'], as_index=False).agg(
        {**{col: 'mean' for col in numerical_columns},
         **{col: 'first' for col in non_numerical_columns}})
    
    aggregated_df.dropna(subset=['Total State Tax'], inplace=True)

    aggregated_df['daily_discount_rate'] = aggregated_df['daily_price'] / aggregated_df['daily_original_price']
    aggregated_df['booked'] = aggregated_df['status'].apply(lambda x: 1 if x == 'available' else 0)
    aggregated_df['start_date'] = pd.to_datetime(aggregated_df['start_date'])
    aggregated_df['week'] = aggregated_df['start_date'].dt.isocalendar().week
    weekly_occupancy = aggregated_df.groupby(['room_id', 'week'])['booked'].mean().reset_index()
    weekly_occupancy.columns = ['room_id', 'week', 'weekly_occupancy_rate']
    aggregated_df = aggregated_df.merge(weekly_occupancy, on=['room_id', 'week'], how='left')

    aggregated_df['weekly_revenue'] = aggregated_df['daily_price'] * 7 * aggregated_df['weekly_occupancy_rate']

    output_dir = '/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/'
    os.makedirs(output_dir, exist_ok=True)
    aggregated_df.to_csv(os.path.join(output_dir, 'data_preprocessed.csv'), index=False)

    print('Preprocessed CSV file has been created successfully.')

    return aggregated_df

def fill_missing_values(df):
    df['room_id'] = df['room_id'].astype(str)
    df['scrape_date'] = df['scrape_date'].astype(str)
    numerical_columns = df.select_dtypes(include=['number']).columns
    # Fill missing values with the mean of all rows
    df[numerical_columns] = df[numerical_columns].transform(lambda x: x.fillna(x.mean()))
    
    #print("Missing values after filling:")
    #print(df[numerical_columns].isnull().sum())

    return df

if __name__ == '__main__':
    filled_data = fill_missing_values(preprocess_data())
    output_dir = '/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/'
    os.makedirs(output_dir, exist_ok=True)
    filled_data.to_csv(os.path.join(output_dir, 'data_filled.csv'), index=False)

    print('Preprocessed and filled CSV file has been created successfully.')

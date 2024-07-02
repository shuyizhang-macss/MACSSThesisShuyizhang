import pandas as pd
import glob
import os

def process_user_info_files(day):
    user_info_files = glob.glob(f'/Users/zhangshuyi/Desktop/airbnb_scrape/2024-06-{day:02d}/2024-06-{day:02d}-*/user_info_*.csv')
    
    for file in user_info_files:
        try:
            user_info_df = pd.read_csv(file)
            
            # Remove 'guest_name' column
            if 'guest_name' in user_info_df.columns:
                user_info_df.drop(columns=['guest_name'], inplace=True)
            
            # Group by 'room_id' and calculate the mean of 'num_review' and 'num_years'
            aggregated_df = user_info_df.groupby('room_id').agg({
                'num_review': 'mean',
                'num_years': 'mean'
            }).reset_index()
            
            part = file.split('/')[-2].split('-')[-1]  # Extract part number from the directory name
            file_name = os.path.basename(file).replace('user_info_', 'user_info_avg_')
            output_dir = os.path.dirname(file)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, file_name)
            
            aggregated_df.to_csv(output_file, index=False)
            
            print(f'Processed and saved: {output_file}')
        
        except pd.errors.EmptyDataError:
            print(f'Skipping empty file: {file}')
        except Exception as e:
            print(f'Error processing file {file}: {e}')


def merge_on_date(day,part):
    user_info_files = glob.glob(f'/Users/zhangshuyi/Desktop/airbnb_scrape/2024-06-{day:02d}/2024-06-{day:02d}-{part}/user_info_avg*.csv')
    #print(user_info_files)
    room_info_files = glob.glob(f'/Users/zhangshuyi/Desktop/airbnb_scrape/2024-06-{day:02d}/2024-06-{day:02d}-{part}/room_info_*.csv')

    def read_csv_files(files):
        dfs = []
        for file in files:
            try:
                df = pd.read_csv(file)
                if not df.empty:
                    dfs.append(df)
            except pd.errors.EmptyDataError:
                print(f'Skipping empty file: {file}')
        return dfs
    
    user_info_df_list = read_csv_files(user_info_files)
    #user_info_df_list = [pd.read_csv(file) for file in user_info_files]
    user_info_df = pd.concat(user_info_df_list, ignore_index=True)

    room_info_df_list = read_csv_files(room_info_files)
    #room_info_df_list = [pd.read_csv(file) for file in room_info_files]
    room_info_df = pd.concat(room_info_df_list, ignore_index=True)

    merged_df = pd.merge(room_info_df, user_info_df, on='room_id', how='outer')
    merged_df['scrape_date'] = f'2024-06-{day:02d}'

    merged_df.to_csv(f'/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/2024-06-{day:02d}-{part}.csv', index=False)

def merge_all_files():
    csv_files = glob.glob('/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/2024-06-*.csv')

    all_dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                all_dfs.append(df)
        except pd.errors.EmptyDataError:
            print(f'Skipping empty file: {file}')
    
    if not all_dfs:
        print('No valid CSV files found to merge.')
        return

    combined_df = pd.concat(all_dfs, ignore_index=True)
    output_dir = '/Users/zhangshuyi/Desktop/airbnb_scrape/Merged_data/'
    os.makedirs(output_dir, exist_ok=True)
    combined_df.to_csv(os.path.join(output_dir, 'combined_data.csv'), index=False)


def aggregate_rows(df):
    # Group by 'room_id', 'start_date', and 'scrape_date'
    # Group by 'room_id', 'start_date', and 'scrape_date'
    grouped_df = df.groupby(['room_id', 'start_date', 'scrape_date']).agg({
        'num_review': 'mean',   
        'num_years': 'mean',    
        'daily_price': 'mean',  
        'room_type': 'first',  
        'price': 'first',    
        'location': 'first', 
        'host_id': 'first',    
    }).reset_index()
    return grouped_df

if __name__ == '__main__':
#    for day in range(26,29):
#        process_user_info_files(day)
    
    for day in range(26,29):
        for part in range(1,3):
            merge_on_date(day,part)
    merge_all_files()
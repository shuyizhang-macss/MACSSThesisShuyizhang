import pandas as pd

# Load the original CSV file
df = pd.read_csv('/Users/zhangshuyi/Desktop/airbnb_scrape/airbnb_ids_new.csv')

# Calculate the size of each split
split_size = len(df) // 2

# Split and save the files
for i in range(2):
    start = i * split_size
    end = None if i == 1 else (i + 1) * split_size
    split_df = df[start:end]
    result = split_df.to_csv(f'airbnb_ids_new_{i + 1}.csv', index=False)

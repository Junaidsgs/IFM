import argparse
import pandas as pd

def fill_missing_dates(input_file, output_file, date_column_name, start_date=None, end_date=None):
    # 1. Load the data (assuming it's a CSV file)
    # If using Excel, use pd.read_excel(input_file) instead
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)

    # 2. Convert the specifying date column to actual datetime objects
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    # 3. Set the date column as the index so we can manipulate the timeline
    df.set_index(date_column_name, inplace=True)

    # 4. Generate a complete, continuous date range from the earliest to the latest date
    # freq='D' specifies Daily frequency. 
    s_date = pd.to_datetime(start_date) if start_date else df.index.min()
    e_date = pd.to_datetime(end_date) if end_date else df.index.max()
    full_date_range = pd.date_range(start=s_date, end=e_date, freq='D')

    # 5. Reindex the dataframe. This injects the new dates with NaN values.
    df_filled = df.reindex(full_date_range)
    
    # Fill missing values: 0 for numeric columns, forward-fill for others (like Package Name)
    for col in df_filled.columns:
        if pd.api.types.is_numeric_dtype(df_filled[col]):
            df_filled[col] = df_filled[col].fillna(0)
        else:
            df_filled[col] = df_filled[col].ffill()

    # 6. Reset the index to turn the dates back into a normal column
    df_filled.reset_index(inplace=True)
    
    # After resetting, the date column is named 'index' by default, rename it back
    df_filled.rename(columns={'index': date_column_name}, inplace=True)

    # 7. Save the fixed data to a new file
    # If using Excel, use df_filled.to_excel(output_file, index=False)
    df_filled.to_csv(output_file, index=False)
    print(f"Success! Missing dates filled with 0. Saved as: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill missing dates in a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("-o", "--output_file", default="output_fixed.csv", help="Path to the output CSV file")
    parser.add_argument("-d", "--date_column", default="Date", help="Name of the date column (default: Date)")
    parser.add_argument("-s", "--start_date", help="Start date (e.g., 2019-09-01). Defaults to earliest date in data.")
    parser.add_argument("-e", "--end_date", help="End date (e.g., 2019-09-30). Defaults to latest date in data.")
    
    args = parser.parse_args()
    
    fill_missing_dates(
        input_file=args.input_file, 
        output_file=args.output_file, 
        date_column_name=args.date_column,
        start_date=args.start_date,
        end_date=args.end_date
    )


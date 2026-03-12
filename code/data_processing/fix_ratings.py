import argparse
import pandas as pd

def fix_na_and_dates(input_file, output_file, date_column_name, start_date=None, end_date=None):
    print(f"Loading data from {input_file}...")
    # Load data. Pandas naturally interprets 'NaN', 'NA' as missing values.
    # explicit na_values just to be extremely safe.
    df = pd.read_csv(input_file, na_values=["NA"])

    # 1. Fix NA values by taking the value from the next cell to the right
    # Iterate through columns up to the second to last one
    for i in range(len(df.columns) - 1):
        df.iloc[:, i] = df.iloc[:, i].fillna(df.iloc[:, i+1])

    # 2. Handle missing dates
    if date_column_name in df.columns:
        df[date_column_name] = pd.to_datetime(df[date_column_name])
        df.set_index(date_column_name, inplace=True)
        
        # Sort index before reindexing to avoid errors and ensure order
        df.sort_index(inplace=True)
        
        s_date = pd.to_datetime(start_date) if start_date else df.index.min()
        e_date = pd.to_datetime(end_date) if end_date else df.index.max()
        
        full_date_range = pd.date_range(start=s_date, end=e_date, freq='D')
        
        df_filled = df.reindex(full_date_range)
        
        # Fill missing dates injected by reindex
        # We forward fill strings (like package name).
        # We will also forward fill the Total Average Rating as that does not reset to 0 usually,
        # but the request previously was fill missing dates with 0s. I will do 0 for numeric to be consistent.
        for col in df_filled.columns:
            if pd.api.types.is_numeric_dtype(df_filled[col]):
                df_filled[col] = df_filled[col].fillna(0)
            else:
                df_filled[col] = df_filled[col].ffill()
                
        df_filled.reset_index(inplace=True)
        df_filled.rename(columns={'index': date_column_name}, inplace=True)
    else:
        print(f"Warning: Date column '{date_column_name}' not found. Skipping date padding.")
        df_filled = df
        
    df_filled.to_csv(output_file, index=False)
    print(f"Success! Fixed NAs and missing dates. Saved as: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix NA values and missing dates in a CSV.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("-o", "--output_file", default="ratings_fixed.csv", help="Path to output CSV")
    parser.add_argument("-d", "--date_column", default="Date", help="Name of date column (default: Date)")
    parser.add_argument("-s", "--start_date", help="Start date (e.g., 2019-09-01). Defaults to earliest.")
    parser.add_argument("-e", "--end_date", help="End date (e.g., 2019-10-31). Defaults to latest.")
    
    args = parser.parse_args()
    
    fix_na_and_dates(
        input_file=args.input_file, 
        output_file=args.output_file, 
        date_column_name=args.date_column,
        start_date=args.start_date,
        end_date=args.end_date
    )

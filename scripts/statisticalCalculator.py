import pandas as pd
import numpy as np
import os

def calculate_stats(df, column):
    stats = {
        f'{column}_mean': df[column].mean(),
        f'{column}_median': df[column].median(),
        f'{column}_mode': df[column].mode().iloc[0] if not df[column].mode().empty else np.nan,
        f'{column}_min': df[column].min(),
        f'{column}_max': df[column].max(),
        f'{column}_Q1': df[column].quantile(0.25),
        f'{column}_Q3': df[column].quantile(0.75),
        f'{column}_var': df[column].var(),
        f'{column}_stdev': df[column].std()
    }
    return pd.Series(stats)

# Specify the columns to analyze
columns_to_analyze = [
    'Acceleration', 'Deceleration', 'Lane Offset', 'Consider Overtake', 
    'Overtake', 'Steer Trq', 'Steer Accel', 'Steer Veloc', 'Speed', 
    'Lateral Acceleration'
]

# Directory containing your CSV files
directory = 'path/to/your/csv/files'

# Process each CSV file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Calculate statistics for each specified column
        for column in columns_to_analyze:
            if column in df.columns:
                stats = calculate_stats(df, column)
                
                # Add new columns with stats
                for stat_name, stat_value in stats.items():
                    df[stat_name] = stat_value
        
        # Save the updated DataFrame back to a CSV file
        output_filename = f'processed_{filename}'
        output_path = os.path.join(directory, output_filename)
        df.to_csv(output_path, index=False)
        
        print(f"Processed file saved: {output_filename}")

print("All files have been processed.")
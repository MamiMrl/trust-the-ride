import os
import pandas as pd

def calculate_interactions(df, columns, X):
    interactions = 0
    last_values = {col: None for col in columns}
    changingState = False
    non_changing_count = 0

    for index, row in df.iterrows():
        isChanged = False
        for col in columns:
            if last_values[col] is not None and row[col] != last_values[col]:
                isChanged = True
            last_values[col] = row[col]
        if isChanged:
            changingState = True
        else:
            non_changing_count += 1
            if changingState and non_changing_count >= X:
                interactions += 1
                changingState = False
        #print(f"Index: {index}, non_changing_count: {non_changing_count}Changing State: {changingState}")

    return interactions

def process_csv_files(directory, columns, X):
    total_interactions = 0

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            interactions = calculate_interactions(df, columns, X)
            print(f"File: {filename} - Total Interactions: {interactions}")
            total_interactions += interactions

    print(f"Overall Total Interactions: {total_interactions}")

# Define the folder path and columns to consider
folder_path = r"D:\OneDrive - Kadir Has University\Masaüstü\Calculate-Interaction"
columns_to_include = ["Acceleration", "Deceleration", "Lane Offset", "Steer Trq", "Steer Accel", "Steer Veloc", "Speed", "Lateral Acceleration"]
X = 2  # Define the arbitrary X times for change detection

# Process the CSV files in the specified directory
process_csv_files(folder_path, columns_to_include, X)
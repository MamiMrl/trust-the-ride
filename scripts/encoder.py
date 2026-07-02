import pandas as pd
import glob
import os
import shutil
import tempfile

# Define a function to determine the personality trait based on the filename
def determine_trait(filename):
    if "HiOp_Lo_No" in filename:
        return "High Openness - Low Neuroticism"
    elif "HiOp_LoNo" in filename:
        return "High Openness - Low Neuroticism"
    elif "HiNo_LoOp" in filename:
        return "High Neuroticism - Low Openness"
    else:
        return "Unknown Value"

# Define the path to your CSV files (current directory)
csv_files = glob.glob("*.csv")

# Process each CSV file
for file in csv_files:
    try:
        # Read the CSV file
        df = pd.read_csv(file, delimiter=',')  # Ensure correct delimiter
        
        # Determine the personality trait
        personality_trait = determine_trait(file)
        
        # Add the new column
        df["Personality Trait"] = personality_trait
        
        # Write to a temporary file first
        with tempfile.NamedTemporaryFile('w', delete=False, newline='', suffix='.csv') as tmp_file:
            df.to_csv(tmp_file.name, index=False)
        
        # Replace the original file with the updated file
        shutil.move(tmp_file.name, file)

        print(f"Successfully updated {file}")

    except PermissionError as e:
        print(f"Permission denied: {file}. Error: {e}")

print("All CSV files have been processed.")

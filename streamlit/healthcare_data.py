# healthcare_data.py
import pandas as pd
import os

def load_healthcare_data():
    """Load healthcare data from a CSV file if it exists; otherwise, create and save a sample dataset."""
    DATASET_FILE = "healthcare_data.csv"
    if os.path.exists(DATASET_FILE):
        df = pd.read_csv(DATASET_FILE)
    else:
        data = {
            "PatientID": [1,2,3,4,5,6,7,8,9,10],
            "Age": [45,50,39,60,55,40,65,70,30,50],
            "BMI": [28.5,30.2,24.8,32.0,29.5,27.0,31.0,33.5,22.5,28.0],
            "BloodPressure": [130,135,120,140,132,125,145,150,115,130],
            "Cholesterol": [220,240,200,260,230,210,250,270,190,220],
            "HeartDisease": ["Yes", "No", "No", "Yes", "Yes", "No", "Yes", "Yes", "No", "No"]
        }
        df = pd.DataFrame(data)
        # Save the sample data to CSV for future runs
        df.to_csv(DATASET_FILE, index=False)
    return df
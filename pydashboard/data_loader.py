import os
import pandas as pd

DATASET_FILE = "healthcare_data.csv"

def load_healthcare_data():
    if os.path.exists(DATASET_FILE):
        return pd.read_csv(DATASET_FILE)
    else:
        # Fallback sample dataset
        data = {
            'PatientID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Age': [45, 50, 39, 60, 55, 40, 65, 70, 30, 50],
            'BMI': [28.5, 30.2, 24.8, 32.0, 29.5, 27.0, 31.0, 33.5, 22.5, 28.0],
            'BloodPressure': [130, 135, 120, 140, 132, 125, 145, 150, 115, 130],
            'Cholesterol': [220, 240, 200, 260, 230, 210, 250, 270, 190, 220],
            'HeartDisease': ['Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No']
        }
        return pd.DataFrame(data)

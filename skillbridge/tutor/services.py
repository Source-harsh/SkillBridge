import joblib
import pandas as pd
import numpy as np

# Load the pre-trained LightGBM model
MODEL_PATH = r"C:\Users\Swapnil\OneDrive\Desktop\coding c++\lightgbm_model.pkl"  # Update the path as necessary
model = joblib.load(MODEL_PATH)

def rank_mentors(input_data):
    """
    Function to predict mentor ranking using the LightGBM model.
    
    :param input_data: Dictionary containing features for the prediction.
    :return: Model prediction.
    """
    # Define the expected features
    features = [
        'mentee_skill_level', 'mentor_skill_level', 'teaching_style_match',
        'mentor_rating', 'engagement_score', 'availability_overlap', 'match_score'
    ]
    
    # Create a DataFrame for the input
    input_df = pd.DataFrame([input_data], columns=features)
    
    # Ensure all columns are numeric and handle missing values
    input_df = input_df.fillna(0).astype(np.float64)
    
    # Make prediction
    probabilities = model.predict_proba(input_df)[:, 1]  # Probability of being selected
    return probabilities[0]  # Return the predicted probability

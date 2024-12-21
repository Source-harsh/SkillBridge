from django.shortcuts import render, get_object_or_404
from .models import Mentor
import joblib
import pandas as pd
from django.http import JsonResponse, HttpResponse
import numpy as np

# Load the trained LightGBM model
model = joblib.load(r'C:\Users\Swapnil\OneDrive\Desktop\coding c++\lightgbm_model.pkl')

# Define features required by the model
FEATURES = [
    'mentee_skill_level', 'mentor_skill_level', 'teaching_style_match',
    'mentor_rating', 'engagement_score', 'availability_overlap', 'match_score'
]

# Skill level mapping
SKILL_LEVEL_MAPPING = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

from datetime import datetime, timedelta

def parse_time(time_str):
    """Convert time string like '5PM' or '10AM' to datetime object"""
    try:
        return datetime.strptime(time_str.strip(), '%I%p')
    except ValueError:
        try:
            return datetime.strptime(time_str.strip(), '%I:%M%p')
        except ValueError:
            return None

def calculate_overlap(mentor_time, user_time):
    """Calculate overlap between mentor and user time slots"""
    try:
        # Parse mentor time range
        mentor_start, mentor_end = mentor_time.split('-')
        mentor_start = parse_time(mentor_start.strip())
        mentor_end = parse_time(mentor_end.strip())
        
        # Parse user time range
        user_start, user_end = user_time.split('-')
        user_start = parse_time(user_start.strip())
        user_end = parse_time(user_end.strip())
        
        if not all([mentor_start, mentor_end, user_start, user_end]):
            return 0
        
        # Convert to minutes since midnight for easier calculation
        mentor_start_mins = mentor_start.hour * 60 + mentor_start.minute
        mentor_end_mins = mentor_end.hour * 60 + mentor_end.minute
        user_start_mins = user_start.hour * 60 + user_start.minute
        user_end_mins = user_end.hour * 60 + user_end.minute
        
        # Calculate overlap
        overlap_start = max(mentor_start_mins, user_start_mins)
        overlap_end = min(mentor_end_mins, user_end_mins)
        
        if overlap_end <= overlap_start:
            return 0
            
        overlap_duration = overlap_end - overlap_start
        total_user_duration = user_end_mins - user_start_mins
        
        # Return overlap percentage
        return (overlap_duration / total_user_duration) * 100
    except:
        return 0

def mentor_list(request):
    # Get all mentors from database
    mentors = Mentor.objects.all()
    mentor_df = pd.DataFrame(list(mentors.values()))
    
    if mentor_df.empty:
        return render(request, 'tutor/mentor_lists.html', {'mentors': []})
    
    # Get search parameters
    mentee_skill = request.GET.get('mentee_skill', '')
    expertise = request.GET.get('expertise', '')
    availability = request.GET.get('availability', '')
    teaching_mode = request.GET.get('teaching_mode', '')
    
    print(f"Search parameters - Skill: {mentee_skill}, Expertise: {expertise}, Availability: {availability}, Mode: {teaching_mode}")

    # Apply filters
    if expertise:
        mentor_df = mentor_df[mentor_df['expertise'].str.contains(expertise, case=False, na=False)]
    if teaching_mode:
        mentor_df = mentor_df[mentor_df['teaching_mode'].str.contains(teaching_mode, case=False, na=False)]
    
    # Calculate availability overlap for each mentor
    if availability:
        mentor_df['availability_overlap'] = mentor_df['available_time'].apply(
            lambda x: calculate_overlap(x, availability)
        )
    else:
        mentor_df['availability_overlap'] = 80  # Default value if no time preference

    # Prepare features for the model
    feature_df = pd.DataFrame()
    
    # Map mentee skill level
    mentee_skill_num = SKILL_LEVEL_MAPPING.get(mentee_skill, 1)
    feature_df['mentee_skill_level'] = pd.Series([mentee_skill_num] * len(mentor_df))
    
    # Map mentor features
    feature_df['mentor_skill_level'] = mentor_df['skill_level']
    feature_df['teaching_style_match'] = 1
    feature_df['mentor_rating'] = mentor_df['rating']
    feature_df['engagement_score'] = 85
    feature_df['availability_overlap'] = mentor_df['availability_overlap']
    feature_df['match_score'] = mentor_df['availability_overlap'] / 100  # Scale overlap to 0-1

    # Print feature values for debugging
    print("\nFeature values for first few mentors:")
    print(feature_df.head())

    # Predict scores using the model
    try:
        mentor_df['predicted_score'] = model.predict_proba(feature_df[FEATURES])[:, 1]
        # Adjust predicted score based on availability overlap
        mentor_df['predicted_score'] = mentor_df['predicted_score'] * (1 + mentor_df['availability_overlap'] / 200)
        mentor_df['predicted_score'] = mentor_df['predicted_score'].round(3)
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        mentor_df['predicted_score'] = 0.5

    # Sort mentors by predicted score and update ranks
    mentor_df = mentor_df.sort_values(by=['predicted_score', 'rating'], ascending=[False, False])
    mentor_df['rank'] = range(1, len(mentor_df) + 1)

    # Print results for debugging
    print("\nTop 5 ranked mentors:")
    print(mentor_df[['name', 'available_time', 'availability_overlap', 'predicted_score', 'rank']].head())

    return render(request, 'tutor/mentor_lists.html', 
                 {'mentors': mentor_df.to_dict('records')})


def mentor_profile(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    return render(request, 'tutor/mentor_profile.html', {'mentor': mentor})

def home(request):
    return HttpResponse("Welcome to the Mentor Matching Home Page!")

def predict_ranking(request):
    """
    API endpoint to predict mentor ranking based on user input.
    """
    if request.method == 'POST':
        # Parse JSON input
        data = request.POST
        try:
            # Extract relevant features from the input
            input_data = {
                'mentee_skill_level': float(data.get('mentee_skill_level', 0)),
                'mentor_skill_level': float(data.get('mentor_skill_level', 0)),
                'teaching_style_match': float(data.get('teaching_style_match', 0)),
                'mentor_rating': float(data.get('mentor_rating', 0)),
                'engagement_score': float(data.get('engagement_score', 0)),
                'availability_overlap': float(data.get('availability_overlap', 0)),
                'match_score': float(data.get('match_score', 0)),
            }

            # Get prediction
            probability = model.predict_proba(pd.DataFrame([input_data])[features])[:, 1]
            return JsonResponse({'success': True, 'probability': probability[0]})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

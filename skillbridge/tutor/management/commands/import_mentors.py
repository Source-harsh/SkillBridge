# import_mentors.py
import csv
from django.core.management.base import BaseCommand
from tutor.models import Mentor

class Command(BaseCommand):
    help = 'Import mentors from a CSV file into the database'

    def handle(self, *args, **kwargs):
        # Path to your CSV file
        file_path = r'C:\Users\Swapnil\OneDrive\Desktop\coding c++\teachers.csv'  # Replace with the actual path to your CSV file

        # Open and read the CSV file
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            
            # Loop through each row in the CSV and create Mentor objects
            for row in reader:
                name = row['name']
                expertise = row['expertise']
                skill_level = row['skill_level']
                available_time = row['available_time']
                teaching_mode = row['teaching_mode']
                rating = row['rating']
                email = row['email']
                
                # Create a new mentor in the database
                Mentor.objects.create(
                    name=name,
                    expertise=expertise,
                    skill_level=skill_level,
                    available_time=available_time,
                    teaching_mode=teaching_mode,
                    rating=rating,
                    email=email
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported mentors from CSV'))

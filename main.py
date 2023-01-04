from resume_builder import *
import json

# Open the JSON file
with open('data.json', 'r') as f:
    # Load the data from the file
    data = json.load(f)

# Create an object from the data
obj = Resume(**data)
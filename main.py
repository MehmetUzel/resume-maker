from resume_builder import *
import json

# Open the JSON file
with open('mehmet.json', 'r') as f:
    # Load the data from the file
    data = json.load(f)

# Create an object from the data
obj = Resume(**data)

print(obj.total_years_of_experience())

#obj.new_generate_pdf('18skill.pdf')

generate_pdf(obj, '20skill.pdf')
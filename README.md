# resume-maker
Python package to build your resume

```bash
pip install resume-maker
```

Sample Usage
```python
from resume_maker import *
import json

# Open the JSON file
with open('data.json', 'r') as f:
    # Load the data from the file
    data = json.load(f)

# Create an object from the data
obj = Resume(**data)

# Create a resume from the object
obj.get_pdf('resume.pdf')
```

Sample JSON

```json
{
    "person": {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "title": "Software Engineer",
        "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum.",
        "linkedin": "https://www.linkedin.com/in/john-doe/",
        "github": "https://github.com/johndoe"
    },
    "experiences": [
        {
            "company": "Acme Corp",
            "title": "Software Engineer",
            "start": "2021-05-01",
            "end": "2020-12-31",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "projects": [
                {
                    "name": "Project A",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                },
                {
                    "name": "Project B",
                    "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                }
            ]
        },
        {
            "company": "New Corp",
            "title": "Software Engineer",
            "start": "2017-05-01",
            "end": "2019-12-31",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "projects": [
                {
                    "name": "Project A",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                },
                {
                    "name": "Project B",
                    "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                }
            ]
        }
    ],
    "educations": [
        {
            "name": "Universtiy of Example",
            "start": "2016-09-01",
            "end": "2020-06-30",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        },
        {
            "name": "Bootcamp of Example",
            "start": "2021-09-01",
            "end": "2021-12-30",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        }
    ],
    "skills": [
        {
            "name": "Python"
        },
        {
            "name": "Django"
        },
        {
            "name": "JavaScript"
        },
        {
            "name": "React"
        },
        {
            "name": "Agile"
        },
        {
            "name": "Scrum"
        },
        {
            "name": "Java"
        },
        {
            "name": "C#"
        },
        {
            "name": "Unity"
        },
        {
            "name": "Flutter"
        },
        {
            "name": "Dart"
        }
    ],
    "languages": [
        {
            "name": "English",
            "level": "Fluent"
        },
        {
            "name": "Spanish",
            "level": "Intermediate"
        }
    ],
    "projects": [
        {
            "name": "Project C",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        },
        {
            "name": "Project D",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        },
        {
            "name": "Project E",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        },
        {
            "name": "Project F",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        },
        {
            "name": "Project G",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ullamcorper odio vitae tincidunt tincidunt. Proin non sollicitudin libero. Praesent felis nulla, faucibus sit amet porta in, convallis eu nulla. Suspendisse mattis ante quam, in dignissim nulla semper in. Sed quis nulla ligula. Quisque dapibus, lectus vel euismod sagittis, arcu purus laoreet massa, at semper diam massa eget diam. Nunc molestie quam sed dolor sodales, nec tempor libero vestibulum. Fusce bibendum turpis hendrerit felis posuere, vitae feugiat lectus euismod. Integer vitae lacinia sem. Fusce semper ipsum. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }
    ]
}
```
from pydantic import BaseModel, HttpUrl
from typing import List
from enum import Enum
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

"""
FONTSIZE = 10

def draw_long_string(c, x, y, text, width):
    words = text.split()
    current_x = x
    current_y = y
    c.setFont('Helvetica', FONTSIZE)
    for word in words:
        if current_x + c.stringWidth(word) > x + width:
            current_x = x
            current_y -= 0.20*inch
        c.drawString(current_x, current_y, word)
        current_x += c.stringWidth(word) + c.stringWidth(" ")
    return current_y

def draw_skills(c, x, y, text, width):
    current_x = x
    current_y = y
    c.setFont('Helvetica', FONTSIZE)
    for word in text:
        if current_x + c.stringWidth(word.name) > x + width:
            current_x = x
            current_y -= 0.20*inch
        c.drawString(current_x, current_y, f"{word.name},")
        current_x += c.stringWidth(word.name) + c.stringWidth("  ")
    return current_y

def draw_title_string(c, x, y, title):
    c.setFillColorRGB(0.5,0.5,0.5) #choose your font colour
    c.setFont("Helvetica", 20)
    c.drawString(x, y, title)
    c.setFont('Helvetica', FONTSIZE)
    c.setFillColorRGB(0,0,0) #choose your font colour

def draw_experience_title(c, x, y, text, date):
    c.setFont("Helvetica", 13)
    c.drawString(x, y, text)
    #newx = x + c.stringWidth(text)
    x += c.stringWidth(text)
    c.setFont('Helvetica', FONTSIZE)
    c.drawString(x, y, date)

"""

class Proficiency(str, Enum):
    b='Beginner'
    i='Intermediate'
    f='Fluent'


class Person(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    title: str
    about: str
    linkedin: HttpUrl
    github: HttpUrl

    def get_full_name(self):
        return f"{self.name} {self.surname}"
        

class Education(BaseModel):
    name: str
    start: str
    end: str
    description: str


class Skill(BaseModel):
    name: str


class Language(BaseModel):
    name: str
    level: Proficiency

    class Config:  
        use_enum_values = True


class Project(BaseModel):
    name: str
    description: str


class Experience(BaseModel):
    company: str
    title: str
    start: str
    end: str
    description: str
    projects: List[Project]


class Resume(BaseModel):
    person: Person
    experiences: List[Experience]
    educations: List[Education]
    skills: List[Skill]
    languages: List[Language]
    projects: List[Project]

    def total_years_of_experience(self) -> float:
        total_years = 0.0
        for experience in self.experiences:
            start_date = datetime.strptime(experience.start, '%Y-%m-%d')
            if experience.end == "Active":
                end_date = datetime.today()
            else:
                end_date = datetime.strptime(experience.end, '%Y-%m-%d')
            total_years += (end_date - start_date).days / 365.25
        return round(total_years, 1)

    # def new_generate_pdf(self, filename):
    #     c = Canvas(filename)
    #     y = 11.25*inch  # start drawing at this y coordinate
    #     profile_off = 0.3*inch
    #     experience_off = 3.75*inch
    #     project_off = 0.3*inch

    #     # ! Dont remove credits below
    #     c.setFont("Helvetica", 7)
    #     c.drawString(0.25*inch, y+0.1*inch, "Built with resume builder python package by Mehmet UZEL")
    #     c.setFont("Helvetica", FONTSIZE)
    #     y -= 0.25*inch

    #     # Draw the name and contact information
    #     c.setFont("Helvetica", 14)
    #     c.drawString(profile_off, y, self.person.get_full_name())
    #     y -= 0.25*inch
    #     c.setFont("Helvetica", 13)
    #     c.drawString(profile_off, y, self.person.title)
    #     y -= 0.25*inch
    #     c.setFont("Helvetica", FONTSIZE)
    #     c.drawString(profile_off, y, self.person.phone)
    #     y -= 0.25*inch
    #     c.drawString(profile_off, y, self.person.email)
    #     y -= 0.2*inch
    #     c.setFont("Helvetica", 8)
    #     c.drawString(profile_off, y, self.person.linkedin)
    #     y -= 0.2*inch
    #     c.drawString(profile_off, y, self.person.github)
    #     y -= 0.5*inch
    #     c.setFont("Helvetica", FONTSIZE)


    #     # Draw the skills
    #     draw_title_string(c, profile_off, y, 'Skills')
    #     y -= 0.25*inch
    #     y = draw_skills(c, profile_off, y, self.skills, 2.75*inch)
    #     y -= 0.25*inch
    #     y -= 0.25*inch


    #     # Draw the About
    #     draw_title_string(c, profile_off, y, 'About')
    #     y -= 0.25*inch
    #     y = draw_long_string(c, profile_off, y, self.person.about, 2.75*inch)
    #     y -= 0.5*inch


    #     # Draw the education
    #     draw_title_string(c, profile_off, y, 'Education')
    #     y -= 0.25*inch
    #     for education in self.educations:
    #         c.drawString(profile_off, y, f'{education.name} ({education.start} - {education.end})')
    #         y -= 0.25*inch
    #         c.setFont("Helvetica", 8.5)
    #         c.drawString(profile_off + 0.1*inch, y, f'{education.description}')
    #         c.setFont("Helvetica", FONTSIZE)
    #         y -= 0.25*inch
    #     y -= 0.25*inch

    #     # Draw the languages
    #     draw_title_string(c, profile_off, y, 'Languages')
    #     y -= 0.25*inch
    #     for language in self.languages:
    #         c.drawString(profile_off, y, f'{language.name} ({language.level})')
    #         y -= 0.25*inch
    #     y -= 0.25*inch


    #     y = 11.25*inch
    #     # Draw the experiences
    #     draw_title_string(c, experience_off, y, 'Experience')
    #     y -= 0.25*inch
    #     c.drawString(experience_off, y, f'Total Years of Experience : {self.total_years_of_experience()} years')
    #     y -= 0.25*inch
    #     for experience in self.experiences:
    #         draw_experience_title(c,experience_off,y,f'{experience.company} - {experience.title}', f'({experience.start} - {experience.end})')
    #         y -= 0.25*inch
    #         y = draw_long_string(c, experience_off+0.25*inch, y, experience.description, 4*inch)
    #         y -= 0.25*inch
    #         for project in experience.projects:
    #             c.drawString(experience_off+0.25*inch, y, f'{project.name}')
    #             y -= 0.25*inch
    #             y = draw_long_string(c, experience_off+0.25*inch, y, project.description, 4*inch)
    #             y -= 0.25*inch
    #     y -= 0.25*inch

    #     c.showPage()

    #     y = 11*inch
    #     # Draw the projects
    #     draw_title_string(c, project_off, y, 'Personal Projects')
    #     y -= 0.5*inch
    #     for project in self.projects:
    #         c.setFont("Helvetica", 13)
    #         c.drawString(project_off, y, f'{project.name}')
    #         c.setFont("Helvetica", FONTSIZE)
    #         y -= 0.25*inch
    #         y = draw_long_string(c, project_off+0.25*inch, y, project.description, 7.5*inch)
    #         y -= 0.5*inch
    #     y -= 0.25*inch

        

    #     c.save()
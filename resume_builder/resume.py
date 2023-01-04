from pydantic import BaseModel, HttpUrl
from typing import List
from enum import Enum
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

def draw_long_string(canvas, x, y, text, width):
    """Draw a long string on the given canvas, breaking it into multiple lines as needed to fit within the given width."""
    words = text.split()
    current_x = x
    current_y = y
    canvas.setFont('Helvetica', 12)
    for word in words:
        if canvas.stringWidth(word) > width:
            max_chars = width // canvas.stringWidth('A')
            chunks = [word[i:i+max_chars] for i in range(0, len(word), max_chars)]
            for chunk in chunks:
                canvas.drawString(current_x, current_y, chunk)
                current_y -= 0.25*inch
        else:
            canvas.drawString(current_x, current_y, word)
            current_x += canvas.stringWidth(word)
            if current_x + canvas.stringWidth(word) > x + width:
                current_x = x
                current_y -= 0.25*inch
    return current_y


class Seniority(str, Enum):
    j='Junior'
    m='Mid'
    s='Senior'

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
    seniority: Seniority

    class Config:  
        use_enum_values = True
        

class Language(BaseModel):
    name: str
    level: Proficiency

    class Config:  
        use_enum_values = True


class Project(BaseModel):
    name: str
    start: str
    end: str
    skills: List[Skill]
    description: str


class Experience(BaseModel):
    company: str
    start: str
    end: str
    description: str
    projects: List[Project]
    skills: List[Skill]


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
            end_date = datetime.strptime(experience.end, '%Y-%m-%d')
            total_years += (end_date - start_date).days / 365.25
        return round(total_years, 1)

    def skill_count(self) -> dict:
        skill_count = {}
        for experience in self.experiences:
            for skill in experience.skills:
                if skill.name in skill_count:
                    skill_count[skill.name] += 1
                else:
                    skill_count[skill.name] = 1
            for project in experience.projects:
                for skill in project.skills:
                    if skill.name in skill_count:
                        skill_count[skill.name] += 1
                    else:
                        skill_count[skill.name] = 1
        for project in self.projects:
            for skill in project.skills:
                if skill.name in skill_count:
                    skill_count[skill.name] += 1
                else:
                    skill_count[skill.name] = 1
        return skill_count

    def skill_graph(self):
        graph = nx.Graph()
        for experience in self.experiences:
            for skill in experience.skills:
                graph.add_node(skill.name)
            for project in experience.projects:
                for skill in project.skills:
                    graph.add_node(skill.name)
                    graph.add_edge(skill.name, project.name)
        for project in self.projects:
            for skill in project.skills:
                graph.add_node(skill.name)
                graph.add_edge(skill.name, project.name)

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.show()

    def cent_skill_graph(self):
        graph = nx.Graph()
        for experience in self.experiences:
            for skill in experience.skills:
                graph.add_edge(skill.name, experience.company)
            for project in experience.projects:
                for skill in project.skills:
                    graph.add_edge(skill.name, project.name)
        for project in self.projects:
            for skill in project.skills:
                graph.add_edge(skill.name, project.name)

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.show()

    def new_generate_pdf(self, filename):
            canvas = Canvas(filename, pagesize=letter)
            y = 10*inch  # start drawing at this y coordinate
            profile_off = 0.5*inch
            experience_off = 3.75*inch

            # ! Dont remove credits below
            canvas.drawString(0.75*inch, 10.5*inch, "Built with resume builder python package by Mehmet UZEL")
            y -= 0.25*inch

            # Draw the name and contact information
            canvas.drawString(profile_off, y, self.person.get_full_name())
            y -= 0.25*inch
            canvas.drawString(profile_off, y, self.person.title)
            y -= 0.25*inch
            canvas.drawString(profile_off, y, self.person.email)
            y -= 0.25*inch
            canvas.drawString(profile_off, y, self.person.phone)
            y -= 0.25*inch
            canvas.drawString(profile_off, y, self.person.linkedin)
            y -= 0.25*inch
            canvas.drawString(profile_off, y, self.person.github)
            y -= 0.5*inch

            # Draw the skills
            canvas.drawString(profile_off, y, 'Skills')
            y -= 0.25*inch
            for skill in self.skills:
                canvas.drawString(profile_off, y, f'{skill.name} ({skill.seniority})')
                y -= 0.25*inch
            y -= 0.25*inch
            # Draw the languages
            canvas.drawString(profile_off, y, 'Languages')
            y -= 0.25*inch
            for language in self.languages:
                canvas.drawString(profile_off, y, f'{language.name} ({language.level})')
                y -= 0.25*inch
            y -= 0.25*inch
            # Draw the languages
            canvas.drawString(profile_off, y, 'About')
            y -= 0.25*inch
            y = draw_long_string(canvas, profile_off, y, self.person.about, 2.75*inch)

            y = 9.75*inch
            # Draw the experiences
            canvas.drawString(experience_off, y, 'Experience')
            y -= 0.25*inch
            canvas.drawString(experience_off, y, f'Total Years of Experience : {self.total_years_of_experience()}')
            y -= 0.25*inch
            for experience in self.experiences:
                canvas.drawString(experience_off, y, f'{experience.company} ({experience.start} - {experience.end})')
                y -= 0.25*inch
                y = draw_long_string(canvas, experience_off+0.5*inch, y, experience.description, 4*inch)
                y -= 0.25*inch
                for project in experience.projects:
                    canvas.drawString(experience_off+0.5*inch, y, f'{project.name} ({project.start} - {project.end})')
                    y -= 0.25*inch
                    y = draw_long_string(canvas, experience_off+0.5*inch, y, project.description, 4*inch)
                    y -= 0.25*inch
                y -= 0.25*inch
            y -= 0.25*inch

            

            canvas.save()
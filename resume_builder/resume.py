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
    # Split the string into words
    words = text.split()
    # Keep track of the current position on the canvas
    current_x = x
    current_y = y
    # Set the font and font size
    canvas.setFont('Helvetica', 12)
    # Iterate over the words in the string
    for word in words:
        # Check if the current word will fit within the current line
        if canvas.stringWidth(word) > width:
            # The word is too long to fit within the current line, so we need to break it into smaller chunks
            # Find the maximum number of characters that can fit within the current line
            max_chars = width // canvas.stringWidth('A')
            # Split the word into smaller chunks that will fit within the current line
            chunks = [word[i:i+max_chars] for i in range(0, len(word), max_chars)]
            # Draw the chunks on separate lines
            for chunk in chunks:
                canvas.drawString(current_x, current_y, chunk)
                current_y -= 0.25*inch
        else:
            # The word fits within the current line, so we can draw it
            canvas.drawString(current_x, current_y, word)
            # Increment the x position by the width of the word
            current_x += canvas.stringWidth(word)
            # Check if the next word will fit within the current line
            if current_x + canvas.stringWidth(words[i+1]) > x + width:
                # The next word won't fit within the current line, so we need to move to the next line
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

            # Draw the name and contact information
            canvas.drawString(1*inch, y, self.person.get_full_name())
            y -= 0.25*inch
            canvas.drawString(1*inch, y, self.person.title)
            y -= 0.25*inch
            canvas.drawString(1*inch, y, self.person.email)
            y -= 0.25*inch
            canvas.drawString(1*inch, y, self.person.phone)
            y -= 0.25*inch
            canvas.drawString(1*inch, y, self.person.linkedin)
            y -= 0.25*inch
            canvas.drawString(1*inch, y, self.person.github)
            y -= 0.5*inch

            # Draw the experiences
            canvas.drawString(1*inch, y, 'Experience')
            y -= 0.25*inch
            canvas.drawString(1*inch, y, f'Total Years of Experience : {self.total_years_of_experience()}')
            y -= 0.25*inch
            for experience in self.experiences:
                canvas.drawString(1*inch, y, f'{experience.company} ({experience.start} - {experience.end})')
                y -= 0.25*inch
                for project in experience.projects:
                    canvas.drawString(1.5*inch, y, f'{project.name} ({project.start} - {project.end})')
                    y -= 0.25*inch
                    y = draw_long_string(canvas, 1.5*inch, y, project.description, 4*inch)
                    y -= 0.25*inch
                y -= 0.25*inch
            y -= 0.5*inch

            # Draw the skills
            canvas.drawString(1*inch, y, 'Skills')
            y -= 0.25*inch
            for skill in self.skills:
                canvas.drawString(1*inch, y, f'{skill.name} ({skill.seniority})')
                y -= 0.25*inch

            # Draw the languages
            canvas.drawString(1*inch, y, 'Languages')
            y -= 0.25*inch
            for language in self.languages:
                canvas.drawString(1*inch, y, f'{language.name} ({language.level})')
                y -= 0.25*inch

            canvas.save()
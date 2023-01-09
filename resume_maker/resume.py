from pydantic import BaseModel, HttpUrl
from typing import List
from enum import Enum
from datetime import datetime
from resume_maker.pdf_converter import generate_pdf


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
    """
    end can be a date or "active"
    """
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
            if experience.end.lower() == "active":
                end_date = datetime.today()
            else:
                end_date = datetime.strptime(experience.end, '%Y-%m-%d')
            total_years += (end_date - start_date).days / 365.25
        return round(total_years, 1)

    def get_pdf(self, filename):
        generate_pdf(self, filename)
from pydantic import BaseModel, HttpUrl
from datetime import date
from enum import Enum

class Seniority(str, Enum):
    j='Junior'
    m='Mid'
    s='Senior'

class Proficiency(str, Enum):
    b='Beginner'
    i='Intermediate'
    f='Fluent'

class Resume(BaseModel):
    person: Person
    experiences = list[Experience]
    educations = list[Education]
    skills = list[Skill]
    languages = list[Language]
    projects = list[Project]
        

class Person(BaseModel):
    name = str
    surname = str
    email = str
    phone = str
    linkedin = HttpUrl
    github = HttpUrl
        

class Experience(BaseModel):
    company = str
    start = date
    end = date
    projects = list[Project]
    skills = list[Skill]
        

class Education(BaseModel):
    name = str
    start = date
    end = date
    description = str
        

class Skill(BaseModel):
    name = str
    seniority = Seniority

    class Config:  
        use_enum_values = True
        

class Language(BaseModel):
    name = str
    level = Proficiency

    class Config:  
        use_enum_values = True


class Project(BaseModel):
    name = str
    start = date
    end = date
    skills = list[Skill]
    description = str
        



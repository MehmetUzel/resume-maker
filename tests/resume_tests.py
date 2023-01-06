import unittest
from resume_builder import *

class TestPerson(unittest.TestCase):
    def test_get_full_name(self):
        person = Person(name='John', surname='Doe', email='john@example.com', phone='123-456-7890', title='Software Engineer', about='Motivated Engineer, who likes camping', linkedin='http://linkedin.com/in/johndoe', github='http://github.com/johndoe')
        self.assertEqual(person.get_full_name(), 'John Doe')

class TestEducation(unittest.TestCase):
    def test_education_name(self):
        education = Education(name='Bachelor of Science', start='2016-09-01', end='2020-05-01', description='This is a description of my education.')
        self.assertEqual(education.name, 'Bachelor of Science')

class TestSkill(unittest.TestCase):
    def test_skill_name(self):
        skill = Skill(name='Python')
        self.assertEqual(skill.name, 'Python')

class TestLanguage(unittest.TestCase):
    def test_language_name(self):
        language = Language(name='English', level='Fluent')
        self.assertEqual(language.name, 'English')
        self.assertEqual(language.level, 'Fluent')

class TestProject(unittest.TestCase):
    def test_project_name(self):
        project = Project(name='My Project', description='This is a description of my project.')
        self.assertEqual(project.name, 'My Project')

class TestExperience(unittest.TestCase):
    def test_experience_company(self):
        project1 = Project(name='Project 1', description='This is a description of my project.')
        project2 = Project(name='Project 2', description='This is a description of my project.')
        experience = Experience(company='Acme Inc.', title='Software Engineer', start='2020-01-01', end='2020-12-31', description='This is a description of my experience.', projects=[project1, project2])
        self.assertEqual(experience.company, 'Acme Inc.')

class TestResume(unittest.TestCase):
    def test_total_years_of_experience(self):
        person = Person(name='John', surname='Doe', email='john@example.com', phone='123-456-7890', title='Software Engineer', about='Motivated Engineer, who likes camping', linkedin='http://linkedin.com/in/johndoe', github='http://github.com/johndoe')
        skill1 = Skill(name='Python')
        skill2 = Skill(name='Java')
        language1 = Language(name='English', level='Fluent')
        language2 = Language(name='Spanish', level='Intermediate')
        project1 = Project(name='Project 1', description='This is a description of my project.')
        project2 = Project(name='Project 2', description='This is a description of my project.')
        education1 = Education(name='Bachelor of Science', start='2016-09-01', end='2020-05-01', description='This is a description of my education.')
        education2 = Education(name='Master of Science', start='2020-09-01', end='2022-05-01', description='This is a description of my education.')
        experience1 = Experience(company='Acme Inc.', title='Software Engineer', start='2020-01-01', end='2020-12-31', description='This is a description of my experience.', projects=[project1, project2])
        experience2 = Experience(company='XYZ Corp.', title='Software Engineer', start='2021-01-01', end='2021-12-31', description='This is a description of my experience.', projects=[project1])
        resume = Resume(person=person, experiences=[experience1, experience2], educations=[education1, education2], skills=[skill1, skill2], languages=[language1, language2], projects=[project1, project2])
        self.assertEqual(resume.total_years_of_experience(), 2.0)

if __name__ == '__main__':
    unittest.main()
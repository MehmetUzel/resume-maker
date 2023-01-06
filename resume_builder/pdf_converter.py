from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

FONTSIZE = 10

def draw_long_string(c, x, y, text, width):
    """Draw a long string on the given c, breaking it into multiple lines as needed to fit within the given width."""
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
    """Draw a long string on the given c, breaking it into multiple lines as needed to fit within the given width."""
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

def draw_credits(c, y):
    # ! Dont remove credits below
    c.setFont("Helvetica", 7)
    c.drawString(0.25*inch, y+0.1*inch, "Built with resume builder python package by Mehmet UZEL")
    c.setFont("Helvetica", FONTSIZE)
    return y - 0.25*inch

def draw_profile(c, profile_off, y, resume):
    c.setFont("Helvetica", 14)
    c.drawString(profile_off, y, resume.person.get_full_name())
    y -= 0.25*inch
    c.setFont("Helvetica", 13)
    c.drawString(profile_off, y, resume.person.title)
    y -= 0.25*inch
    c.setFont("Helvetica", FONTSIZE)
    c.drawString(profile_off, y, resume.person.phone)
    y -= 0.25*inch
    c.drawString(profile_off, y, resume.person.email)
    y -= 0.2*inch
    c.setFont("Helvetica", 8)
    c.drawString(profile_off, y, resume.person.linkedin)
    y -= 0.2*inch
    c.drawString(profile_off, y, resume.person.github)
    y -= 0.5*inch
    c.setFont("Helvetica", FONTSIZE)
    return y

def draw_skills_section(c, profile_off, y, resume):
    draw_title_string(c, profile_off, y, 'Skills')
    y -= 0.25*inch
    y = draw_skills(c, profile_off, y, resume.skills, 2.75*inch)
    return y - 0.5*inch

def draw_about_section(c, profile_off, y, resume):
    draw_title_string(c, profile_off, y, 'About')
    y -= 0.25*inch
    y = draw_long_string(c, profile_off, y, resume.person.about, 2.75*inch)
    return y - 0.5*inch

def draw_education_section(c, profile_off, y, resume):
    draw_title_string(c, profile_off, y, 'Education')
    y -= 0.25*inch
    for education in resume.educations:
        c.drawString(profile_off, y, f'{education.name} ({education.start} - {education.end})')
        y -= 0.25*inch
        c.setFont("Helvetica", 8.5)
        c.drawString(profile_off + 0.1*inch, y, f'{education.description}')
        c.setFont("Helvetica", FONTSIZE)
        y -= 0.25*inch
    return y - 0.25*inch

def draw_language_section(c, profile_off, y, resume):
    draw_title_string(c, profile_off, y, 'Languages')
    y -= 0.25*inch
    for language in resume.languages:
        c.drawString(profile_off, y, f'{language.name} ({language.level})')
        y -= 0.25*inch
    return y - 0.25*inch

def draw_experience_section(c, experience_off, y, resume):
    draw_title_string(c, experience_off, y, 'Experience')
    y -= 0.25*inch
    c.drawString(experience_off, y, f'Total Years of Experience : {resume.total_years_of_experience()} years')
    y -= 0.25*inch
    for experience in resume.experiences:
        draw_experience_title(c,experience_off,y,f'{experience.company} - {experience.title}', f'({experience.start} - {experience.end})')
        y -= 0.25*inch
        y = draw_long_string(c, experience_off+0.25*inch, y, experience.description, 4*inch)
        y -= 0.25*inch
        for project in experience.projects:
            c.drawString(experience_off+0.25*inch, y, f'{project.name}')
            y -= 0.25*inch
            y = draw_long_string(c, experience_off+0.25*inch, y, project.description, 4*inch)
            y -= 0.25*inch
    return y - 0.25*inch

def draw_projects_section(c, project_off, y, resume):
    y -= 0.25*inch
    draw_title_string(c, project_off, y, 'Personal Projects')
    y -= 0.5*inch
    for project in resume.projects:
        c.setFont("Helvetica", 13)
        c.drawString(project_off, y, f'{project.name}')
        c.setFont("Helvetica", FONTSIZE)
        y -= 0.25*inch
        y = draw_long_string(c, project_off+0.25*inch, y, project.description, 7.5*inch)
        y -= 0.5*inch
    return y - 0.25*inch


def generate_pdf(resume, filename):
    c = Canvas(filename)
    INITIAL_Y = 11.25*inch
    y = INITIAL_Y  # start drawing at this y coordinate
    profile_off = 0.3*inch
    experience_off = 3.75*inch
    project_off = 0.3*inch

    # ! Dont remove credits below
    y = draw_credits(c,y)

    # Draw the name and contact information
    y = draw_profile(c, profile_off, y, resume)


    # Draw the skills
    y = draw_skills_section(c, profile_off, y, resume)


    # Draw the About
    y = draw_about_section(c, profile_off, y, resume)


    # Draw the education
    y = draw_education_section(c, profile_off, y, resume)

    # Draw the languages
    y = draw_language_section(c, profile_off, y, resume)
    

    y = INITIAL_Y
    # Draw the experiences
    y = draw_experience_section(c, experience_off, y, resume)

    c.showPage()

    y = INITIAL_Y
    # Draw the projects
    y = draw_projects_section(c, project_off, y, resume)

    c.save()
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# Font settings
FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_SIZE_NAME = 18
FONT_SIZE_TITLE = 14
FONT_SIZE_SECTION = 13
FONT_SIZE_SUBSECTION = 11
FONT_SIZE_BODY = 9.5
FONT_SIZE_SMALL = 8
FONT_SIZE_CREDITS = 7

# Colors
COLOR_PRIMARY = HexColor('#1a1a1a')
COLOR_SECONDARY = HexColor('#4a4a4a')
COLOR_ACCENT = HexColor('#2c5282')
COLOR_LIGHT = HexColor('#718096')
COLOR_DIVIDER = HexColor('#cbd5e0')


def draw_horizontal_line(c, x, y, width, color=COLOR_DIVIDER):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(x, y, x + width, y)
    c.setStrokeColor(COLOR_PRIMARY)


def draw_long_string(c, x, y, text, width, fontsize=FONT_SIZE_BODY, font=FONT, line_spacing=0.18):
    words = text.split()
    current_x = x
    current_y = y
    c.setFont(font, fontsize)
    for word in words:
        if current_x + c.stringWidth(word, font, fontsize) > x + width:
            current_x = x
            current_y -= line_spacing * inch
        c.drawString(current_x, current_y, word)
        current_x += c.stringWidth(word, font, fontsize) + c.stringWidth(" ", font, fontsize)
    return current_y


def draw_skills(c, x, y, skills, width):
    current_x = x
    current_y = y
    c.setFont(FONT, FONT_SIZE_BODY)
    for i, skill in enumerate(skills):
        separator = "," if i < len(skills) - 1 else ""
        text = f"{skill.name}{separator}"
        if current_x + c.stringWidth(text, FONT, FONT_SIZE_BODY) > x + width:
            current_x = x
            current_y -= 0.18 * inch
        c.drawString(current_x, current_y, text)
        current_x += c.stringWidth(text, FONT, FONT_SIZE_BODY) + c.stringWidth(" ", FONT, FONT_SIZE_BODY)
    return current_y


def draw_section_header(c, x, y, title, width=None):
    c.setFillColor(COLOR_ACCENT)
    c.setFont(FONT_BOLD, FONT_SIZE_SECTION)
    c.drawString(x, y, title.upper())
    y -= 0.08 * inch
    if width:
        draw_horizontal_line(c, x, y, width, COLOR_ACCENT)
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return y - 0.18 * inch


def draw_experience_title(c, x, y, company, title, date):
    c.setFont(FONT_BOLD, FONT_SIZE_SUBSECTION)
    c.setFillColor(COLOR_PRIMARY)
    c.drawString(x, y, f"{company} - {title}")
    c.setFont(FONT, FONT_SIZE_SMALL)
    c.setFillColor(COLOR_LIGHT)
    c.drawString(x, y - 0.16 * inch, date)
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return y - 0.35 * inch


def draw_credits(c, y):
    c.setFont(FONT, FONT_SIZE_CREDITS)
    c.setFillColor(COLOR_LIGHT)
    c.drawRightString(8.1 * inch, y + 0.1 * inch, "Built with resume-maker python package by Mehmet UZEL")
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return y - 0.15 * inch


def draw_profile(c, x, y, resume):
    # Name
    c.setFont(FONT_BOLD, FONT_SIZE_NAME)
    c.setFillColor(COLOR_PRIMARY)
    c.drawString(x, y, resume.person.get_full_name())
    y -= 0.3 * inch

    # Title
    c.setFont(FONT, FONT_SIZE_TITLE)
    c.setFillColor(COLOR_ACCENT)
    c.drawString(x, y, resume.person.title)
    c.setFillColor(COLOR_PRIMARY)
    y -= 0.35 * inch

    return y


def draw_contact_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Personal Info & Socials', width)

    # Phone & Email
    c.setFont(FONT_BOLD, FONT_SIZE_SMALL)
    c.drawString(x, y, "Phone:")
    c.setFont(FONT, FONT_SIZE_BODY)
    c.drawString(x + 0.45 * inch, y, resume.person.phone)
    y -= 0.2 * inch

    c.setFont(FONT_BOLD, FONT_SIZE_SMALL)
    c.drawString(x, y, "Email:")
    c.setFont(FONT, FONT_SIZE_BODY)
    c.drawString(x + 0.45 * inch, y, resume.person.email)
    y -= 0.2 * inch

    # Social links
    c.setFont(FONT, FONT_SIZE_SMALL)
    c.setFillColor(COLOR_ACCENT)
    c.drawString(x, y, str(resume.person.linkedin))
    y -= 0.18 * inch
    c.drawString(x, y, str(resume.person.github))
    y -= 0.18 * inch
    if resume.person.twitter:
        c.drawString(x, y, str(resume.person.twitter))
        y -= 0.18 * inch
    c.setFillColor(COLOR_PRIMARY)

    return y - 0.25 * inch


def draw_skills_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Skills', width)
    y = draw_skills(c, x, y, resume.skills, width)
    return y - 0.35 * inch


def draw_about_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'About', width)
    y = draw_long_string(c, x, y, resume.person.about, width)
    return y - 0.35 * inch


def draw_education_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Education', width)
    for education in resume.educations:
        c.setFont(FONT_BOLD, FONT_SIZE_BODY)
        c.drawString(x, y, education.name)
        c.setFont(FONT, FONT_SIZE_SMALL)
        c.setFillColor(COLOR_LIGHT)
        c.drawString(x, y - 0.15 * inch, f"{education.start} - {education.end}")
        c.setFillColor(COLOR_PRIMARY)
        y -= 0.3 * inch
        y = draw_long_string(c, x + 0.1 * inch, y, education.description, width - 0.1 * inch, FONT_SIZE_SMALL)
        c.setFont(FONT, FONT_SIZE_BODY)
        y -= 0.25 * inch
    return y - 0.1 * inch


def draw_language_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Languages', width)
    for language in resume.languages:
        c.setFont(FONT_BOLD, FONT_SIZE_BODY)
        c.drawString(x, y, language.name)
        c.setFont(FONT, FONT_SIZE_BODY)
        c.setFillColor(COLOR_LIGHT)
        c.drawString(x + c.stringWidth(language.name, FONT_BOLD, FONT_SIZE_BODY) + 5, y, f"({language.level})")
        c.setFillColor(COLOR_PRIMARY)
        y -= 0.2 * inch
    return y - 0.15 * inch


def draw_experience_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Experience', width)

    c.setFont(FONT, FONT_SIZE_BODY)
    c.setFillColor(COLOR_SECONDARY)
    c.drawString(x, y, f"Total: {resume.total_years_of_experience()} years")
    c.setFillColor(COLOR_PRIMARY)
    y -= 0.3 * inch

    for experience in resume.experiences:
        end_display = experience.end if experience.end else "Present"
        y = draw_experience_title(c, x, y, experience.company, experience.title, f"{experience.start} - {end_display}")
        y = draw_long_string(c, x + 0.15 * inch, y, experience.description, width - 0.15 * inch)
        y -= 0.3 * inch
        for project in experience.projects:
            c.setFont(FONT_BOLD, FONT_SIZE_BODY)
            c.drawString(x + 0.15 * inch, y, project.name)
            y -= 0.18 * inch
            y = draw_long_string(c, x + 0.25 * inch, y, project.description, width - 0.25 * inch)
            y -= 0.2 * inch
    return y


def draw_projects_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, 'Personal Projects', width)
    y -= 0.1 * inch
    for project in resume.projects:
        c.setFont(FONT_BOLD, FONT_SIZE_SUBSECTION)
        c.setFillColor(COLOR_PRIMARY)
        c.drawString(x, y, project.name)
        c.setFont(FONT, FONT_SIZE_BODY)
        y -= 0.22 * inch
        y = draw_long_string(c, x + 0.15 * inch, y, project.description, width - 0.15 * inch)
        y -= 0.35 * inch
    return y


def generate_pdf(resume, filename):
    c = Canvas(filename)
    INITIAL_Y = 11.25 * inch
    LEFT_COL_X = 0.3 * inch
    LEFT_COL_WIDTH = 2.9 * inch
    RIGHT_COL_X = 3.6 * inch
    RIGHT_COL_WIDTH = 4.5 * inch
    FULL_WIDTH = 7.8 * inch

    y = INITIAL_Y

    # Credits
    y = draw_credits(c, y)

    # Profile header (full width)
    y = draw_profile(c, LEFT_COL_X, y, resume)

    # Left column sections
    left_y = y
    left_y = draw_contact_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_skills_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_about_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_education_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_language_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)

    # Right column - Experience
    right_y = y
    right_y = draw_experience_section(c, RIGHT_COL_X, right_y, resume, RIGHT_COL_WIDTH)

    c.showPage()

    # Page 2 - Projects (full width)
    y = INITIAL_Y
    y = draw_projects_section(c, LEFT_COL_X, y, resume, FULL_WIDTH)

    c.save()

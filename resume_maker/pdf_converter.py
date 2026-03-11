import re

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from pathlib import Path

# Font settings
FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_SIZE_NAME = 18
FONT_SIZE_TITLE = 14
FONT_SIZE_SECTION = 13
FONT_SIZE_SUBSECTION = 11
FONT_SIZE_BODY = 9.5
FONT_SIZE_SMALL = 8
FONT_SIZE_TINY = 7.4

SPACE_XXS = 0.08 * inch
SPACE_XS = 0.14 * inch
SPACE_SM = 0.18 * inch
SPACE_MD = 0.24 * inch
SPACE_LG = 0.3 * inch

LEADING_BODY = 0.18
LEADING_SMALL = 0.17

EXPERIENCE_AFTER_TITLE = 0.35 * inch
EXPERIENCE_AFTER_SUMMARY = 0.28 * inch
EXPERIENCE_PROJECT_TITLE_GAP = 0.18 * inch
EXPERIENCE_AFTER_PROJECT = 0.28 * inch
EXPERIENCE_BETWEEN_ITEMS = 0.08 * inch

# Colors
COLOR_PRIMARY = HexColor('#1a1a1a')
COLOR_SECONDARY = HexColor('#4a4a4a')
COLOR_ACCENT = HexColor('#2c5282')
COLOR_LIGHT = HexColor('#718096')
COLOR_DIVIDER = HexColor('#cbd5e0')

LABELS = {
    'en': {
        'personal_info_socials': 'Personal Info & Socials',
        'location': 'Location:',
        'phone': 'Phone:',
        'email': 'Email:',
        'skills': 'Skills',
        'about': 'About',
        'education': 'Education',
        'languages': 'Languages',
        'experience': 'Experience',
        'total_years': 'Total: {years} years',
        'present': 'Present',
        'personal_projects': 'Personal Projects',
        'Beginner': 'Beginner',
        'Intermediate': 'Intermediate',
        'Fluent': 'Fluent',
    },
    'tr': {
        'personal_info_socials': 'Kişisel Bilgiler',
        'location': 'Konum:',
        'phone': 'Telefon:',
        'email': 'E-posta:',
        'skills': 'Yetenekler',
        'about': 'Hakkımda',
        'education': 'Eğitim',
        'languages': 'Diller',
        'experience': 'Deneyim',
        'total_years': 'Toplam: {years} yıl',
        'present': 'Devam ediyor',
        'personal_projects': 'Kişisel Projeler',
        'Beginner': 'Temel',
        'Intermediate': 'Orta',
        'Fluent': 'Akıcı',
    },
}

TR_UPPER_MAP = str.maketrans({
    'i': 'İ',
    'ı': 'I',
})


def configure_fonts():
    global FONT, FONT_BOLD

    regular_candidates = [
        Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf'),
        Path('/System/Library/Fonts/Supplemental/Arial.ttf'),
    ]
    bold_candidates = [
        Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ]

    regular_font = next((path for path in regular_candidates if path.exists()), None)
    bold_font = next((path for path in bold_candidates if path.exists()), None)

    if not regular_font:
        return

    pdfmetrics.registerFont(TTFont('ResumeSans', str(regular_font)))
    FONT = 'ResumeSans'

    if bold_font:
        pdfmetrics.registerFont(TTFont('ResumeSans-Bold', str(bold_font)))
        FONT_BOLD = 'ResumeSans-Bold'
    else:
        FONT_BOLD = FONT


configure_fonts()

MOBILE_SKILLS = {
    'Flutter',
    'Dart',
    'SwiftUI',
    'Firebase',
    'Kotlin',
    'Android',
    'iOS',
    'Mobile App Development',
    'Google Play Publishing',
    'Mobil Uygulama Geliştirme',
    'Google Play Yayınlama',
}

AI_SKILLS = {
    'AI Agents',
    'Agentic Workflows',
    'Prompt Engineering',
    'LLM Integrations',
    'RAG',
    'Tool Calling',
    'MCP',
    'AI Evals',
    'RLHF',
    'Yapay Zeka Ajanları',
    'Ajanik İş Akışları',
    'İstem Mühendisliği',
    'LLM Entegrasyonları',
    'Araç Çağırma',
    'AI Değerlendirmeleri',
}

SKILL_GROUPS = [
    ('Mobile', MOBILE_SKILLS),
    ('AI', AI_SKILLS),
    ('Backend', {'.NET Core', 'C#', 'SQL Server', 'WebAPI', 'MVC', 'Python', 'Java'}),
    ('Web', {'HTML', 'CSS', 'React', 'SEO'}),
    ('CMS & Tools', {'WordPress', 'Elementor', 'Git', 'Figma'}),
]


def get_locale(resume):
    return getattr(resume, 'locale', 'en') or 'en'


def t(resume, key, **kwargs):
    locale = get_locale(resume)
    template = LABELS.get(locale, LABELS['en']).get(key, LABELS['en'].get(key, key))
    return template.format(**kwargs) if kwargs else template


def localized_upper(text, locale):
    if locale == 'tr':
        return text.translate(TR_UPPER_MAP).upper()
    return text.upper()


def draw_horizontal_line(c, x, y, width, color=COLOR_DIVIDER):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(x, y, x + width, y)
    c.setStrokeColor(COLOR_PRIMARY)


def draw_long_string(c, x, y, text, width, fontsize=FONT_SIZE_BODY, font=FONT, line_spacing=0.18):
    lines = split_text_to_lines(text, width, fontsize, font)
    return draw_wrapped_lines(c, x, y, lines, fontsize, font, line_spacing)


def split_text_to_lines(text, width, fontsize=FONT_SIZE_BODY, font=FONT):
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = words[0]
    for word in words[1:]:
        candidate = f"{current_line} {word}"
        if pdfmetrics.stringWidth(candidate, font, fontsize) <= width:
            current_line = candidate
            continue
        lines.append(current_line)
        current_line = word
    lines.append(current_line)
    return lines


def split_token_for_width(token, width, fontsize=FONT_SIZE_BODY, font=FONT):
    if pdfmetrics.stringWidth(token, font, fontsize) <= width:
        return [token]

    parts = re.split(r'([/\-])', token)
    chunks = []
    current = ""

    for part in parts:
        if not part:
            continue
        candidate = f"{current}{part}"
        if current and pdfmetrics.stringWidth(candidate, font, fontsize) > width:
            chunks.append(current)
            current = part
            continue
        current = candidate

    if current:
        chunks.append(current)

    normalized = []
    for chunk in chunks:
        if pdfmetrics.stringWidth(chunk, font, fontsize) <= width:
            normalized.append(chunk)
            continue
        piece = ""
        for char in chunk:
            candidate = f"{piece}{char}"
            if piece and pdfmetrics.stringWidth(candidate, font, fontsize) > width:
                normalized.append(piece)
                piece = char
            else:
                piece = candidate
        if piece:
            normalized.append(piece)

    return normalized


def build_wrapped_tokens(items, width, fontsize=FONT_SIZE_BODY, font=FONT):
    lines = []
    current_line = []
    current_width = 0
    space_width = pdfmetrics.stringWidth(" ", font, fontsize)

    for item in items:
        token = item["text"]
        token_parts = split_token_for_width(token, width, fontsize, font)
        for part_index, part in enumerate(token_parts):
            part_width = pdfmetrics.stringWidth(part, font, fontsize)
            needs_space = bool(current_line)
            candidate_width = current_width + (space_width if needs_space else 0) + part_width
            if current_line and candidate_width > width:
                lines.append(current_line)
                current_line = []
                current_width = 0
                needs_space = False

            if needs_space:
                current_width += space_width
            current_line.append({
                "text": part,
                "accent": item.get("accent", False),
            })
            current_width += part_width

            is_last_part = part_index == len(token_parts) - 1
            if is_last_part and item.get("suffix"):
                suffix = item["suffix"]
                suffix_width = pdfmetrics.stringWidth(suffix, font, fontsize)
                if current_line and current_width + suffix_width > width:
                    lines.append(current_line)
                    current_line = [{
                        "text": suffix.lstrip(),
                        "accent": False,
                    }]
                    current_width = pdfmetrics.stringWidth(suffix.lstrip(), font, fontsize)
                else:
                    current_line.append({
                        "text": suffix,
                        "accent": False,
                    })
                    current_width += suffix_width

    if current_line:
        lines.append(current_line)

    return lines


def draw_wrapped_lines(c, x, y, lines, fontsize=FONT_SIZE_BODY, font=FONT, line_spacing=0.18):
    c.setFont(font, fontsize)
    current_y = y
    for index, line in enumerate(lines):
        c.drawString(x, current_y, line)
        if index < len(lines) - 1:
            current_y -= line_spacing * inch
    return current_y


def draw_clickable_text(c, x, y, text, url, fontsize=FONT_SIZE_SMALL, font=FONT_BOLD, color=COLOR_ACCENT):
    c.setFont(font, fontsize)
    c.setFillColor(color)
    c.drawString(x, y, text)
    text_width = pdfmetrics.stringWidth(text, font, fontsize)
    c.linkURL(str(url), (x, y - 2, x + text_width, y + fontsize), relative=0)
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return text_width


def draw_labeled_value(c, x, y, label, value, label_font=FONT_BOLD, value_font=FONT, label_size=FONT_SIZE_SMALL, value_size=FONT_SIZE_BODY, gap=4):
    c.setFont(label_font, label_size)
    c.drawString(x, y, label)
    label_width = pdfmetrics.stringWidth(label, label_font, label_size)
    c.setFont(value_font, value_size)
    c.drawString(x + label_width + gap, y, value)


def group_skills(skills):
    grouped = []
    used = set()
    skill_names = [skill.name for skill in skills]

    for label, members in SKILL_GROUPS:
        items = [name for name in skill_names if name in members]
        if items:
            grouped.append((label, items))
            used.update(items)

    remaining = [name for name in skill_names if name not in used]
    if remaining:
        grouped.append(('Other', remaining))

    return grouped


def ordered_skills(skills):
    grouped = group_skills(skills)
    ordered = []
    for label, items in grouped:
        is_accent = label in {'Mobile', 'AI'}
        for item in items:
            ordered.append({
                "text": item,
                "accent": is_accent,
            })
    return ordered


def draw_skill_list(c, x, y, skills, width):
    tokens = ordered_skills(skills)
    items = []
    for index, token in enumerate(tokens):
        items.append({
            "text": token["text"],
            "accent": token["accent"],
            "suffix": ", " if index < len(tokens) - 1 else "",
        })

    lines = build_wrapped_tokens(items, width, FONT_SIZE_SMALL, FONT)
    current_y = y
    for line_index, line in enumerate(lines):
        current_x = x
        for token in line:
            color = COLOR_ACCENT if token["accent"] else COLOR_PRIMARY
            c.setFillColor(color)
            c.setFont(FONT_BOLD if token["accent"] else FONT, FONT_SIZE_SMALL)
            c.drawString(current_x, current_y, token["text"])
            current_x += pdfmetrics.stringWidth(token["text"], FONT_BOLD if token["accent"] else FONT, FONT_SIZE_SMALL)
        if line_index < len(lines) - 1:
            current_y -= 0.15 * inch
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return current_y


def draw_section_header(c, x, y, title, width=None, locale='en'):
    c.setFillColor(COLOR_ACCENT)
    c.setFont(FONT_BOLD, FONT_SIZE_SECTION)
    c.drawString(x, y, localized_upper(title, locale))
    y -= SPACE_XXS
    if width:
        draw_horizontal_line(c, x, y, width, COLOR_ACCENT)
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return y - SPACE_MD


def draw_experience_title(c, x, y, company, title, date):
    c.setFont(FONT_BOLD, FONT_SIZE_SUBSECTION)
    c.setFillColor(COLOR_PRIMARY)
    c.drawString(x, y, f"{company} - {title}")
    c.setFont(FONT, FONT_SIZE_SMALL)
    c.setFillColor(COLOR_LIGHT)
    c.drawString(x, y - SPACE_XS, date)
    c.setFillColor(COLOR_PRIMARY)
    c.setFont(FONT, FONT_SIZE_BODY)
    return y - EXPERIENCE_AFTER_TITLE


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
    y = draw_section_header(c, x, y, t(resume, 'personal_info_socials'), width, get_locale(resume))

    # Phone & Email
    if resume.person.location:
        draw_labeled_value(c, x, y, t(resume, 'location'), resume.person.location)
        y -= SPACE_MD

    draw_labeled_value(c, x, y, t(resume, 'phone'), resume.person.phone)
    y -= SPACE_MD

    draw_labeled_value(c, x, y, t(resume, 'email'), resume.person.email)
    y -= SPACE_MD

    # Social links
    c.setFont(FONT, FONT_SIZE_SMALL)
    c.setFillColor(COLOR_ACCENT)
    c.drawString(x, y, str(resume.person.linkedin))
    y -= SPACE_MD
    c.drawString(x, y, str(resume.person.github))
    y -= SPACE_MD
    if resume.person.twitter:
        c.drawString(x, y, str(resume.person.twitter))
        y -= SPACE_MD
    c.setFillColor(COLOR_PRIMARY)

    return y - SPACE_LG


def draw_skills_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'skills'), width, get_locale(resume))
    y = draw_skill_list(c, x, y, resume.skills, width)
    return y - 0.3 * inch


def draw_about_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'about'), width, get_locale(resume))
    y = draw_long_string(c, x, y, resume.person.about, width, FONT_SIZE_SMALL, FONT, LEADING_BODY)
    return y - SPACE_LG


def draw_education_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'education'), width, get_locale(resume))
    for education in resume.educations:
        c.setFont(FONT_BOLD, FONT_SIZE_BODY)
        c.drawString(x, y, education.name)
        c.setFont(FONT, FONT_SIZE_SMALL)
        c.setFillColor(COLOR_LIGHT)
        c.drawString(x, y - SPACE_XS, f"{education.start} - {education.end}")
        c.setFillColor(COLOR_PRIMARY)
        y -= SPACE_LG
        y = draw_long_string(c, x + 0.1 * inch, y, education.description, width - 0.1 * inch, FONT_SIZE_SMALL, FONT, LEADING_SMALL)
        c.setFont(FONT, FONT_SIZE_BODY)
        y -= SPACE_LG
    return y - SPACE_XS


def draw_language_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'languages'), width, get_locale(resume))
    for language in resume.languages:
        c.setFont(FONT_BOLD, FONT_SIZE_BODY)
        c.drawString(x, y, language.name)
        c.setFont(FONT, FONT_SIZE_BODY)
        c.setFillColor(COLOR_LIGHT)
        c.drawString(x + c.stringWidth(language.name, FONT_BOLD, FONT_SIZE_BODY) + 5, y, f"({t(resume, language.level)})")
        c.setFillColor(COLOR_PRIMARY)
        y -= SPACE_MD
    return y - SPACE_LG


def draw_experience_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'experience'), width, get_locale(resume))

    c.setFont(FONT, FONT_SIZE_BODY)
    c.setFillColor(COLOR_SECONDARY)
    c.drawString(x, y, t(resume, 'total_years', years=resume.total_years_of_experience()))
    c.setFillColor(COLOR_PRIMARY)
    y -= SPACE_LG + SPACE_XXS

    for experience in resume.experiences:
        end_display = experience.end if experience.end else t(resume, 'present')
        y = draw_experience_title(c, x, y, experience.company, experience.title, f"{experience.start} - {end_display}")
        y = draw_long_string(c, x + 0.15 * inch, y, experience.description, width - 0.15 * inch, FONT_SIZE_BODY, FONT, LEADING_BODY)
        y -= EXPERIENCE_AFTER_SUMMARY
        for project in experience.projects:
            c.setFont(FONT_BOLD, FONT_SIZE_BODY)
            c.drawString(x + 0.15 * inch, y, project.name)
            if project.link_label and project.link_url:
                link_width = pdfmetrics.stringWidth(project.link_label, FONT_BOLD, FONT_SIZE_SMALL)
                link_x = x + width - link_width
                if link_x > x + 1.6 * inch:
                    draw_clickable_text(c, link_x, y, project.link_label, project.link_url)
                else:
                    y -= SPACE_XS
                    draw_clickable_text(c, x + 0.25 * inch, y, project.link_label, project.link_url)
            y -= EXPERIENCE_PROJECT_TITLE_GAP
            y = draw_long_string(c, x + 0.25 * inch, y, project.description, width - 0.25 * inch, FONT_SIZE_SMALL, FONT, LEADING_SMALL)
            y -= EXPERIENCE_AFTER_PROJECT
        y -= EXPERIENCE_BETWEEN_ITEMS
    return y


def draw_projects_section(c, x, y, resume, width):
    y = draw_section_header(c, x, y, t(resume, 'personal_projects'), width, get_locale(resume))
    y -= SPACE_XXS
    for project in resume.projects:
        c.setFont(FONT_BOLD, FONT_SIZE_BODY)
        c.setFillColor(COLOR_PRIMARY)
        c.drawString(x, y, project.name)
        if project.link_label and project.link_url:
            link_width = pdfmetrics.stringWidth(project.link_label, FONT_BOLD, FONT_SIZE_SMALL)
            if x + width - link_width > x + 0.1 * inch:
                draw_clickable_text(c, x + width - link_width, y, project.link_label, project.link_url)
            else:
                y -= SPACE_XS
                draw_clickable_text(c, x + 0.1 * inch, y, project.link_label, project.link_url)
        c.setFont(FONT, FONT_SIZE_SMALL)
        y -= SPACE_SM
        y = draw_long_string(c, x + 0.1 * inch, y, project.description, width - 0.1 * inch, FONT_SIZE_SMALL, FONT, LEADING_SMALL)
        y -= SPACE_MD
    return y


def estimate_project_height(project, width):
    description_lines = split_text_to_lines(project.description, width - 0.15 * inch, FONT_SIZE_BODY, FONT)
    return (
        0.22 * inch
        + max(len(description_lines) - 1, 0) * 0.18 * inch
        + 0.35 * inch
    )


def draw_project_item(c, x, y, project, width):
    c.setFont(FONT_BOLD, FONT_SIZE_SUBSECTION)
    c.setFillColor(COLOR_PRIMARY)
    c.drawString(x, y, project.name)
    c.setFont(FONT, FONT_SIZE_BODY)
    y -= 0.22 * inch
    y = draw_long_string(c, x + 0.15 * inch, y, project.description, width - 0.15 * inch)
    return y - 0.35 * inch


def draw_projects_across_pages(c, x, y, resume, width, initial_page_bottom, next_page_bottom, page_width):
    remaining = list(resume.projects)
    current_x = x
    current_y = y
    current_width = width
    current_bottom = initial_page_bottom
    show_header = True

    while remaining:
        if show_header:
            current_y = draw_section_header(c, current_x, current_y, 'Personal Projects', current_width, 'en')
            current_y -= 0.1 * inch
            show_header = False

        project = remaining[0]
        required_height = estimate_project_height(project, current_width)
        if current_y - required_height < current_bottom:
            c.showPage()
            current_x = 0.3 * inch
            current_y = 11.25 * inch
            current_width = page_width
            current_bottom = next_page_bottom
            show_header = True
            continue

        current_y = draw_project_item(c, current_x, current_y, project, current_width)
        remaining.pop(0)


def generate_pdf(resume, filename):
    c = Canvas(filename)
    INITIAL_Y = 11.25 * inch
    LEFT_COL_X = 0.3 * inch
    LEFT_COL_WIDTH = 3.0 * inch
    RIGHT_COL_X = 3.7 * inch
    RIGHT_COL_WIDTH = 4.3 * inch
    FULL_WIDTH = 7.8 * inch
    PAGE_BOTTOM = 0.55 * inch

    y = INITIAL_Y

    # Profile header (full width)
    y = draw_profile(c, LEFT_COL_X, y, resume)

    # Left column sections
    left_y = y
    left_y = draw_contact_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_skills_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_about_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_education_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_language_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)
    left_y = draw_projects_section(c, LEFT_COL_X, left_y, resume, LEFT_COL_WIDTH)

    # Right column - Experience
    right_y = y
    right_y = draw_experience_section(c, RIGHT_COL_X, right_y, resume, RIGHT_COL_WIDTH)

    c.save()

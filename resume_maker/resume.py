import calendar
import re
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from resume_maker.pdf_converter import generate_pdf


MONTH_LOOKUP = {
    'jan': 1,
    'january': 1,
    'oca': 1,
    'ocak': 1,
    'feb': 2,
    'february': 2,
    'şub': 2,
    'sub': 2,
    'şubat': 2,
    'subat': 2,
    'mar': 3,
    'march': 3,
    'mar': 3,
    'mart': 3,
    'apr': 4,
    'april': 4,
    'nis': 4,
    'nisan': 4,
    'may': 5,
    'mayıs': 5,
    'mayis': 5,
    'jun': 6,
    'june': 6,
    'haz': 6,
    'haziran': 6,
    'jul': 7,
    'july': 7,
    'tem': 7,
    'temmuz': 7,
    'aug': 8,
    'august': 8,
    'ağu': 8,
    'agu': 8,
    'ağustos': 8,
    'agustos': 8,
    'sep': 9,
    'sept': 9,
    'september': 9,
    'eyl': 9,
    'eylül': 9,
    'eylul': 9,
    'oct': 10,
    'october': 10,
    'eki': 10,
    'ekim': 10,
    'nov': 11,
    'november': 11,
    'kas': 11,
    'kasım': 11,
    'kasim': 11,
    'dec': 12,
    'december': 12,
    'ara': 12,
    'aralık': 12,
    'aralik': 12,
}


class Proficiency(str, Enum):
    b='Beginner'
    i='Intermediate'
    f='Fluent'


class Person(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    location: str = None
    title: str
    about: str
    linkedin: HttpUrl
    github: HttpUrl
    twitter: HttpUrl = None

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
    link_label: Optional[str] = None
    link_url: Optional[HttpUrl] = None


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
    locale: str = "en"
    person: Person
    experiences: List[Experience]
    educations: List[Education]
    skills: List[Skill]
    languages: List[Language]
    projects: List[Project]

    @staticmethod
    def _parse_date(value: str, is_end: bool = False) -> datetime:
        if not value:
            return datetime.today()

        normalized = value.strip()
        if normalized.lower() in {"active", "present", "current"}:
            return datetime.today()

        month_match = re.fullmatch(r"([A-Za-zÇĞİÖŞÜçğıöşü.]+)\s+(\d{4})", normalized)
        if month_match:
            month_token = month_match.group(1).replace(".", "").casefold()
            year = int(month_match.group(2))
            month = MONTH_LOOKUP.get(month_token)
            if month:
                day = calendar.monthrange(year, month)[1] if is_end else 1
                return datetime(year, month, day)

        date_formats = (
            ("%Y-%m-%d", None),
            ("%Y-%m", None),
            ("%b %Y", None),
            ("%B %Y", None),
            ("%Y", None),
        )

        for fmt, _ in date_formats:
            try:
                parsed = datetime.strptime(normalized, fmt)
                if fmt == "%Y":
                    month = 12 if is_end else 1
                    day = 31 if is_end else 1
                    return parsed.replace(month=month, day=day)
                if fmt in {"%Y-%m", "%b %Y", "%B %Y"}:
                    day = calendar.monthrange(parsed.year, parsed.month)[1] if is_end else 1
                    return parsed.replace(day=day)
                return parsed
            except ValueError:
                continue

        raise ValueError(f"Unsupported date format: {value}")

    def total_years_of_experience(self) -> float:
        if not self.experiences:
            return 0.0

        ranges = []
        for experience in self.experiences:
            start_date = self._parse_date(experience.start)
            end_date = self._parse_date(experience.end, is_end=True)
            if end_date < start_date:
                start_date, end_date = end_date, start_date
            ranges.append((start_date, end_date))

        ranges.sort(key=lambda item: item[0])
        merged_ranges = [ranges[0]]

        for start_date, end_date in ranges[1:]:
            last_start, last_end = merged_ranges[-1]
            if start_date <= last_end:
                merged_ranges[-1] = (last_start, max(last_end, end_date))
                continue
            merged_ranges.append((start_date, end_date))

        total_years = 0.0
        for start_date, end_date in merged_ranges:
            total_years += (end_date - start_date).days / 365.25
        return round(total_years, 1)

    def get_pdf(self, filename):
        generate_pdf(self, filename)

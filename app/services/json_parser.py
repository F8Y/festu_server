from bs4 import BeautifulSoup
from datetime import datetime
import re

DATE_RE = re.compile(r"(\d{2}\.\d{2}\.\d{4})\s+([А-Яа-я]+)")
PAIR_NUMBER_RE = re.compile(r"(\d)-я пара")

PAIR_TIME_MAP = {
    1: "8:05-9:35",
    2: "9:50-11:20",
    3: "11:35-13:05",
    4: "13:35-15:05",
    5: "15:15-16:45",
    6: "16:55-18:25"
}

def parse_schedule_to_json(html: str, monday: datetime, sunday: datetime) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    schedule = {
        "week": f"{monday.strftime('%d.%m.%Y')}–{sunday.strftime('%d.%m.%Y')}",
        "days": []
    }

    for h3 in soup.find_all("h3"):
        match = DATE_RE.match(h3.text.strip())
        if not match:
            continue

        date_str, day_name = match.groups()
        table = h3.find_next_sibling("table")
        if not table:
            continue

        day_data = {
            "date": date_str,
            "day": day_name,
            "pairs": []
        }

        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 5:
                continue

            pair_td = tds[0]
            number_time_text = pair_td.get_text(strip=True)
            number = extract_pair_number(number_time_text)
            time = extract_pair_time_by_number(number)

            subject_text = tds[1].get_text(strip=True)
            subject = clean_subject(subject_text)
            comment = extract_comment(subject_text)

            auditorium = tds[2].get_text(strip=True)
            group = tds[3].get_text(strip=True)

            teacher_td = tds[4]
            teacher_name = teacher_td.get_text(strip=True).replace("✉", "").strip()
            email_tag = teacher_td.find("a", href=re.compile("mailto:"))
            teacher_email = email_tag["href"].replace("mailto:", "").strip() if email_tag else None

            pair = {
                "number": number,
                "time": time,
                "subject": subject,
                "auditorium": auditorium,
                "group": group,
                "teacher": {
                    "name": teacher_name,
                    "email": teacher_email
                },
                "comment": comment
            }

            day_data["pairs"].append(pair)

        if day_data["pairs"]:
            schedule["days"].append(day_data)

    return schedule


def extract_pair_number(text: str) -> int | None:
    match = PAIR_NUMBER_RE.search(text)
    return int(match.group(1)) if match else None

def extract_pair_time_by_number(number: int | None) -> str | None:
    if number is None:
        return None
    return PAIR_TIME_MAP.get(number)

def extract_comment(text: str) -> str | None:
    match = re.match(r"\(([^)]+)\)", text)
    return match.group(1) if match else None

def clean_subject(text: str) -> str:
    return re.sub(r"^\([^)]+\)\s*", "", text).strip()
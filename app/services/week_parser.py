from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

DATE_RE = re.compile(r"(\d{2}\.\d{2}\.\d{4})")

def get_week_range(date_str: str) -> tuple[datetime, datetime]:
    selected_date = datetime.strptime(date_str, "%d.%m.%Y")
    monday = selected_date - timedelta(days=selected_date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def extract_week_schedule(html: str, selected_date: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    monday, sunday = get_week_range(selected_date)

    result_parts = []

    for h3 in soup.find_all("h3"):
        match = DATE_RE.search(h3.text)
        if not match:
            continue

        day_date = datetime.strptime(match.group(1), "%d.%m.%Y")

        if monday <= day_date <= sunday:
            table = h3.find_next_sibling("table")
            if table:
                result_parts.append(str(h3))
                result_parts.append(str(table))

    return "\n".join(result_parts) if result_parts else None
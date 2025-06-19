from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import calendar
from datetime import datetime

app = FastAPI()

class DateRequest(BaseModel):
    dates: List[str]

def format_calendar(dates: List[str]) -> str:
    # Преобразуем строки в объекты datetime
    dt_objects = [datetime.strptime(date_str, "%d-%m-%Y") for date_str in dates]
    if not dt_objects:
        return "Нет дат для отображения"

    # Определяем месяц и год по первой дате
    target_month = dt_objects[0].month
    target_year = dt_objects[0].year

    # Получаем все дни месяца
    cal = calendar.Calendar(firstweekday=0)  # Начинается с Понедельника (0 - понедельник)
    month_days = cal.monthdayscalendar(target_year, target_month)

    # Преобразуем даты в set номеров дней
    active_days = {dt.day for dt in dt_objects if dt.month == target_month and dt.year == target_year}

    # Шапка календаря
    header = f"Календарь активностей для {target_year}-{target_month:02d}:\n"
    days_header = "Пн Вт Ср Чт Пт Сб Вс\n"

    body = ""
    for week in month_days:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day in active_days:
                line += "✅ "
            else:
                line += f"{day:2} "
        body += line.rstrip() + "\n"

    return header + days_header + body.strip()

@app.post("/calendar/")
async def generate_calendar(req: DateRequest):
    result = format_calendar(req.dates)
    return {"calendar": result}

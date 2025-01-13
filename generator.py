#!/usr/bin/env python3
"""
US Stock Market Calendar Generator for 2025

This script generates an ICS (iCalendar) file containing the complete US stock market schedule for 2025.
- Regular trading sessions (9:30 AM - 4:00 PM ET)
- Full-day market holidays
- Early closure days (closes at 1:00 PM ET)
- Daylight Saving Time changes

Usage:
    Simply run the script and it will generate 'us_stock_market_calendar_2025.ics' in the current directory.
    The generated file can be imported into most calendar applications (Google Calendar, Outlook, etc.)

Author: 
    Bin Hua <https://binhua.org>
"""

from datetime import datetime, timedelta

def generate_market_calendar():
    # Define full-day market holidays
    full_holidays = [
        (datetime(2025, 1, 1), "New Year's Day"),
        (datetime(2025, 1, 20), "Martin Luther King Jr. Day"),
        (datetime(2025, 2, 17), "Presidents Day"),
        (datetime(2025, 4, 18), "Good Friday"),
        (datetime(2025, 5, 26), "Memorial Day"),
        (datetime(2025, 6, 19), "Juneteenth"),
        (datetime(2025, 7, 4), "Independence Day"),
        (datetime(2025, 9, 1), "Labor Day"),
        (datetime(2025, 11, 27), "Thanksgiving Day"),
        (datetime(2025, 12, 25), "Christmas Day"),
    ]
    
    # Define early closure days (close at 1:00 PM ET)
    early_close_days = [
        (datetime(2025, 7, 3), "Independence Day Eve"),
        (datetime(2025, 11, 28), "Day After Thanksgiving"),
        (datetime(2025, 12, 24), "Christmas Eve"),
    ]
    
    # Generate calendar file content
    calendar = []
    calendar.append("BEGIN:VCALENDAR")
    calendar.append("VERSION:2.0")
    calendar.append("PRODID:-//Anthropic//Stock Market Calendar Generator//EN")
    calendar.append("CALSCALE:GREGORIAN")
    calendar.append("METHOD:PUBLISH")
    calendar.append("X-WR-CALNAME:US Stock Market Schedule 2025")
    calendar.append("X-WR-TIMEZONE:America/New_York")
    
    # Add Daylight Saving Time changes
    calendar.extend([
        "BEGIN:VEVENT",
        "DTSTART:20250309T020000",
        "DTEND:20250309T030000",
        "SUMMARY:Daylight Saving Time Begins",
        "DESCRIPTION:US markets switch to summer trading hours",
        "TRANSP:OPAQUE",
        "END:VEVENT",
        "",
        "BEGIN:VEVENT",
        "DTSTART:20251102T010000",
        "DTEND:20251102T020000",
        "SUMMARY:Daylight Saving Time Ends",
        "DESCRIPTION:US markets switch to winter trading hours",
        "TRANSP:OPAQUE",
        "END:VEVENT"
    ])

    # Add full-day market holidays
    for date, holiday_name in full_holidays:
        calendar.extend([
            "",
            "BEGIN:VEVENT",
            f"DTSTART;VALUE=DATE:{date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(date + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:Market Closed - {holiday_name}",
            "DESCRIPTION:US Stock Market Holiday - Full Day Closure",
            "TRANSP:OPAQUE",
            "END:VEVENT"
        ])

    # Add early closure days
    for date, desc in early_close_days:
        calendar.extend([
            "",
            "BEGIN:VEVENT",
            f"DTSTART:{date.strftime('%Y%m%d')}T093000",
            f"DTEND:{date.strftime('%Y%m%d')}T130000",
            f"SUMMARY:Early Close - {desc}",
            "DESCRIPTION:Early Market Closure - Trading Hours 9:30 AM - 1:00 PM ET",
            "TRANSP:OPAQUE",
            "END:VEVENT"
        ])

    # Generate regular trading days
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
            
        # Check if current date is a holiday or early closure day
        is_holiday = any(current_date.date() == holiday[0].date() for holiday in full_holidays)
        is_early_close = any(current_date.date() == early[0].date() for early in early_close_days)
        
        # Add regular trading hours for normal trading days
        if not is_holiday and not is_early_close:
            calendar.extend([
                "",
                "BEGIN:VEVENT",
                f"DTSTART:{current_date.strftime('%Y%m%d')}T093000",
                f"DTEND:{current_date.strftime('%Y%m%d')}T160000",
                "SUMMARY:Regular Trading Hours",
                "DESCRIPTION:Normal US Stock Market Trading Session (9:30 AM - 4:00 PM ET)",
                "TRANSP:TRANSPARENT",
                "END:VEVENT"
            ])
            
        current_date += timedelta(days=1)
    
    calendar.append("")
    calendar.append("END:VCALENDAR")
    
    return "\n".join(calendar)

# Generate calendar file
calendar_content = generate_market_calendar()

# Write to file
with open('us_stock_market_calendar_2025.ics', 'w', encoding='utf-8') as f:
    f.write(calendar_content)

print("Calendar has been generated successfully!")

"""Module 18 · Dates, times and time zones (the bugs everyone ships once)

Rules that prevent 95% of date bugs:
  1. Store and compute in UTC. Convert to local time only to SHOW it.
  2. Use timezone-AWARE datetimes (with tzinfo). "Naive" ones are ambiguous.
  3. Use zoneinfo for real time zones: it knows daylight saving time (DST).
  4. Exchange dates as ISO 8601 text: 2026-11-08T10:30:00+00:00

Run it:  python 18_data_apis_databases/05_dates_and_timezones.py
         (on Windows you may need: pip install tzdata)
"""
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

BERLIN, KOLKATA, NEW_YORK = ZoneInfo("Europe/Berlin"), ZoneInfo("Asia/Kolkata"), ZoneInfo("America/New_York")

# --- 1. Naive vs aware ------------------------------------------------------------------------
naive = datetime(2026, 11, 8, 10, 30)                 # 10:30... but where?
aware = datetime(2026, 11, 8, 10, 30, tzinfo=UTC)     # 10:30 UTC, unambiguous
print("naive tzinfo:", naive.tzinfo, "| aware:", aware.isoformat())

# --- 2. One moment, shown in three places ---------------------------------------------------------
meeting = datetime(2026, 11, 8, 9, 0, tzinfo=BERLIN)
for zone in (BERLIN, KOLKATA, NEW_YORK):
    print(f"  {str(zone):<16} {meeting.astimezone(zone):%a %H:%M}")

# --- 3. "Now" the right way ----------------------------------------------------------------------
now = datetime.now(UTC)                                # NOT datetime.utcnow() (naive, deprecated)
print("now (UTC):", now.isoformat(timespec="seconds"))

# --- 4. Daylight saving time: adding a "day" across the switch --------------------------------------
before_switch = datetime(2026, 3, 28, 12, 0, tzinfo=BERLIN)   # Germany: clocks jump on 29 March
next_day = before_switch + timedelta(days=1)
hours = (next_day.astimezone(UTC) - before_switch.astimezone(UTC)) / timedelta(hours=1)
print(f"+1 day across DST: {next_day:%Y-%m-%d %H:%M %Z}, only {hours:.0f} real hours passed")

# --- 5. Parse and format ------------------------------------------------------------------------------
parsed = datetime.fromisoformat("2026-11-08T10:30:00+05:30")     # ISO 8601 from an API
print("parsed:", parsed, "->", parsed.astimezone(UTC).isoformat())
print("custom:", datetime.strptime("08.11.2026 10:30", "%d.%m.%Y %H:%M"))   # a German-style input
print("pretty:", f"{meeting:%d %B %Y, %H:%M}")

# --- 6. Date maths -------------------------------------------------------------------------------------
invoice = date(2026, 11, 8)
due = invoice + timedelta(days=30)
print("due:", due, "| days left:", (due - invoice).days, "| weekday:", due.strftime("%A"))

# Comparing naive and aware datetimes raises TypeError: a good thing, it catches the bug.
try:
    naive < aware
except TypeError as e:
    print("caught:", e)

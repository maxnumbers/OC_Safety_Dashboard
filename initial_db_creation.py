import csv
import sqlite3
import sys
from datetime import date, timedelta

import numpy as np
import pandas as pd

# Create sqlite database and cursor
conn = sqlite3.connect("safety.db")


def determine_point_category(point_qty):

    if point_qty < 3:
        rank = "Wood"
    elif point_qty < 6:
        rank = "Bronze"
    elif point_qty < 9:
        rank = "Silver"
    elif point_qty < 12:
        rank = "Gold"
    elif point_qty >= 12:
        rank = "Platinum"
    return rank


def assign_event_points(event):
    points_by_event = {
        "Attend a Staff Meeting": 1,
        "Safety Steering Team Meeting": 1,
        "Attend a Team Safety Meeting": 1,
        "Share off the job safety/Who had your back?": 1,
        "Review JHA before performing a NEW task": 1,
        "Present a safety meeting": 5,
        "Provide Time and/or Funds for Safety Improvements": 2,
        "Participation in a safety inspection": 2,
        "Safety Measures for Work Travel during COVID": 5,
        "Plant Trial Preparation": 10,
        "Safety Mentor": 10,
        "Calculated Activity": 2,
    }

    return points_by_event[event]


def round_and_intc(np_array):
    return np.intc(np.round(np_array))


# load initial data
submissions = pd.read_csv("OC_Safety_Dashboard.csv")
submissions["Event Date"] = pd.to_datetime(submissions["Event Date"])
# drop duplicates at high level to avoid repeating
submissions = submissions.drop_duplicates()

# section out to get employees:leaders,employees, and leaders
employees = submissions[["Name", "Leader Name"]].drop_duplicates()
leaders = pd.DataFrame(submissions["Leader Name"].unique(), columns=["Leader Name"])

# determine points for events, then reattach to submissions
events = list(submissions["Event"])
credit_points = [assign_event_points(event) for event in events]
submissions = submissions.assign(Event_Points=credit_points)

# calculate points of employees
employees_points = [
    submissions[submissions["Name"] == name]["Event_Points"].sum()
    for name in list(employees["Name"])
]
employees = employees.assign(Total_Points=employees_points)

# assign point categories once points are summed
employees_categories = [
    determine_point_category(points) for points in list(employees["Total_Points"])
]
employees = employees.assign(Point_Category=employees_categories)
employees = employees.sort_values("Total_Points", ascending=False)
employees_by_leader = [
    employees[employees["Leader Name"] == leader] for leader in leaders["Leader Name"]
]
employee_qty_by_leader = [
    employees[employees["Leader Name"] == leader].Name.count()
    for leader in leaders["Leader Name"]
]
employee_qty_by_leader = np.array(employee_qty_by_leader)
leaders = leaders.assign(Qty_Emlpoyees=employee_qty_by_leader)

# determine % bronze or higher: org & teams
bronze_plus_employees = employees[employees["Point_Category"] != "Wood"]
qty_bronze_plus = len(bronze_plus_employees)
total_employees = len(employees)
bronze_plus_qty_by_leader = [
    bronze_plus_employees[bronze_plus_employees["Leader Name"] == leader].Name.count()
    for leader in leaders["Leader Name"]
]
bronze_plus_qty_by_leader = np.array(bronze_plus_qty_by_leader)
percent_bronze_plus_by_leader = round_and_intc(
    bronze_plus_qty_by_leader / employee_qty_by_leader * 100
)
leaders = leaders.assign(Percent_Bronze=percent_bronze_plus_by_leader)

# determine % attendance of staff meetings: org & team
## get all staff meetings
all_staff_meetings = submissions[submissions["Event"] == "Attend a Staff Meeting"]
## filter staff meetings to last 45 days
date_max = pd.to_datetime(date.today())
date_min = pd.to_datetime(date.today() - timedelta(45))
date_filtered_staff_meetings = all_staff_meetings[
    (all_staff_meetings["Event Date"] >= date_min)
    & (all_staff_meetings["Event Date"] < date_max)
]

# at least one "Staff Meeting" in last 31 days
total_staff_meeting_attendee_qty = len(date_filtered_staff_meetings.Name.unique())
total_staff_meeting_percent_attendance = int(
    round(total_staff_meeting_attendee_qty / total_employees * 100, 0)
)
staff_meetings_by_leader = [
    date_filtered_staff_meetings[
        date_filtered_staff_meetings["Leader Name"] == leader
    ].Name.unique()
    for leader in leaders["Leader Name"]
]
staff_meeting_qty_by_leader = []
for team in staff_meetings_by_leader:
    staff_meeting_qty_by_leader.append(len(team))
staff_meeting_qty_by_leader = np.array(staff_meeting_qty_by_leader)
percent_staff_meeting_attendance_by_leader = round_and_intc(
    staff_meeting_qty_by_leader / employee_qty_by_leader * 100
)
leaders = leaders.assign(
    Staff_Meeting_Percent_30Days=percent_staff_meeting_attendance_by_leader
)
leaders = leaders.assign(Qty_Staff_Meetings_30Days=staff_meeting_qty_by_leader)

print(submissions.head(), submissions.describe())
print(leaders.head(), leaders.describe())
print(employees.head(), employees.describe())


submissions.to_sql("submissions", conn, if_exists="replace")
leaders.to_sql("leaders", conn, if_exists="replace")
employees.to_sql("employees", conn, if_exists="replace")

conn.close()

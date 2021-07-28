import streamlit as st
import numpy as np
import pandas as pd
from google.oauth2 import service_account
from gsheetsdb import connect

field_data = {
    "employees": [
        "",
        "Brandon Williams",
        "Tim Turner",
        "Bryan Albani",
        "Beccah Albright",
        "Steve Badger",
        "Ken Basista",
    ],
    "months": [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "leaders": [
        "",
        "Houpt",
        "Keely",
        "Mendez-Andino",
        "Ravenscroft",
        "Uhl",
    ],
    "events": {
        "Staff Meeting": 1,
        "Safety Team Meeting": 1,
        "Share off the job safety/Who had your back?": 1,
        "Review JHA before new task": 1,
        "Present a safety meeting": 5,
        "Provide time and/or funds for safety improvements": 2,
        "Participation in a safety inspection": 2,
        "Safety measures for work travel during COVID": 5,
        "Plant Trial Preperation": 10,
        "Safety Mentor": 10,
        "Calculated Activity": 2,
    },
}

calculated_fields = {
    "timeframe": {
        "text": [
            "A day or less",
            "A few days a week",
            "Less than 6 months",
            "More than 6 months",
        ],
        "help_text": "**First Aid**: no recovery required before returning to job (Bruising, small cuts, no loss time, doesn't require attention by medical doctor | **Reversible Injury**: Normally reversible; likely will return to same job after recovery from incident: broken bones, severe lasceration, short hospitalization, short term disability, lost time (multi-day), fingertip amputation (not thumb) | **Permanent Injury**: Normally non-reversible; likely will not return to same job after recovery from incident: fatality, limb amputation, long term disability, chronic illness",
    },
    "hazard_reduction": {
        "text": ["Slightly Reduced", "Modestly Reduced", "Elminated"],
        "help_text": "**Slightly Reduced**: PPE and Administrative controlled- Worker still responsible for compliance | **Modestly Reduced**: Engineering controlled - worker is prevented from contacting hazard | **Eliminated**: Substitution or elimination of hazard",
    },
    "completion_difficulty": {
        "text": ["Easy", "Average", "Difficult"],
        "help_text": "**Easy**: Most work can be done from the comfort of the desk chair A few forms need filled out or written Little to no collaboration is needed | **Average**: Collaboration is needed. The creation of new procedures or processes | **Difficult**: Blood, sweat, and tears are needed to complete. The implementation of brand new ideas. Challenging the status quo",
    },
}

st.title("OC Safety Form")

fields = (
    # store employee
    employee := st.selectbox("Name:", field_data["employees"]),
    leader := st.selectbox("Leader Name:", field_data["leaders"]),
    month := st.selectbox("Event Month:", field_data["months"]),
    event := st.selectbox("Event Attended:", field_data["events"].keys()),
)

if event == "Calculated Activity":
    st.write("Additional information is needed")
    calculated_fields = (
        timeframe := st.selectbox(
            "How much time to address this issue?",
            calculated_fields["timeframe"]["text"],
            help=calculated_fields["timeframe"]["help_text"],
        ),
        hazard_reduction := st.selectbox(
            "How much has the hazard been reduced?",
            calculated_fields["hazard_reduction"]["text"],
            help=calculated_fields["hazard_reduction"]["help_text"],
        ),
        completion_difficulty := st.selectbox(
            "Difficulty to complete?",
            calculated_fields["completion_difficulty"]["text"],
            help=calculated_fields["completion_difficulty"]["help_text"],
        ),
    )

    # all are filled in
st.button("Submit")

import sqlite3

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
conn = sqlite3.connect("safety.db")
leaders = pd.read_sql("SELECT * from leaders", conn, index_col="index")
employees = pd.read_sql("SELECT* from employees", conn, index_col="index")


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
    "severity": {
        "text": [
            "First Aid",
            "Reversible Injury",
            "Permanent Injury",
        ],
        "help_text": "**First Aid:** no recovery required before returning to job: Bruising, small cuts, no loss time, doesn't require attention by medical doctor | **Reversible Injury:** Normally reversible; likely will return to same job after recovery from incident: broken bones, severe lasceration, short hospitalization, short term disability, lost time (multi-day), fingertip amputation (not thumb) | **Permanent Injury:** Normally non-reversible; likely will not return to same job after recovery from incident: fatality, limb amputation, long term disability, chronic illness",
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

with st.beta_expander("Submit Safety Form"):
    st.title("OC Safety Form")

    fields = (
        employee := st.selectbox("Name:", employees["Name"]),
        leader := st.selectbox("Leader Name:", leaders["Leader Name"]),
        event := st.selectbox("Event Attended:", points_by_event.keys()),
    )

    if event == "Calculated Activity":
        st.write("Additional information is needed")
        calculated_fields = (
            timeframe := st.selectbox(
                "How much time to address this issue?",
                calculated_fields["timeframe"]["text"],
                help=calculated_fields["timeframe"]["help_text"],
            ),
            severity := st.selectbox(
                "How severe was the resulting injury?",
                calculated_fields["severity"]["text"],
                help=calculated_fields["severity"]["help_text"],
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

st.dataframe(employees["Name", "Total_Points", "Point_Category"])

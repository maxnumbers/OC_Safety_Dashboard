import sqlite3
import os
import numpy as np
import pandas as pd

try:
    import plotly.express as px
except:
    os.system('cmd /c "pip install plotly"')
    import plotly.express as px
import streamlit as st

# Load data
conn = sqlite3.connect("safety.db")
leaders = pd.read_sql("SELECT * from leaders", conn, index_col="index")
employees = pd.read_sql("SELECT* from employees", conn, index_col="index")


st.title("Safety Metric Dashboard")

st.header("Leaderboard")
st.dataframe(employees[["Name", "Total_Points", "Point_Category"]])


st.header("Team Ranks Pie Chart")
leader = st.selectbox("Select a Team Lead", leaders[["Leader Name"]])
pie_chart = px.pie(
    employees[employees["Leader Name"] == leader],
    values="Total_Points",
    names="Point_Category",
)
st.plotly_chart(pie_chart)


st.header("Team Staff Meeting Attendance")
bar_graph = px.bar(leaders, x="Leader Name", y="Staff_Meeting_Percent_30Days")
bar_graph.add_shape(  # add a horizontal "target" line
    type="line",
    line_color="salmon",
    line_width=3,
    opacity=1,
    line_dash="dot",
    x0=-1,
    x1=4,
    y0=75,
    y1=75,
)
st.plotly_chart(bar_graph)

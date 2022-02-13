# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 21:57:01 2022

@author: chags
"""

import streamlit as st
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from math import pi
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import sqlite3
conn = sqlite3.connect('czfitness.db')
c = conn.cursor()
    

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS max_data(date_submitted DATE, Q1 TEXT, Q2 INTEGER, Q3 TEXT, Q4 INTEGER, Q5 INTEGER)')

def add_feedback(date_submitted, Q1, Q2, Q3, Q4, Q5):
    c.execute('INSERT INTO max_data (date_submitted,Q1, Q2, Q3, Q4, Q5) VALUES (?,?,?,?,?,?)',(date_submitted,Q1, Q2, Q3, Q4, Q5))
    conn.commit()

def main():

    bs_goal = 325
    bench_goal = 230
    dead_goal = 325
    st.title("Data Dashboard")
 

    st.sidebar.header("Cole Fitness Tracking")
    df = pd.read_sql("SELECT * FROM max_data", con = conn)
    df1 = df.rename(columns={'date_submitted':'index'}).set_index('index')
    df['Entries'] = df['Q3'].index.count()
    st.line_chart(df['Entries'], use_container_width=True)
    st.bar_chart(df1["Q3"], use_container_width=True)    

    
    with st.expander("Add Lift Data"):
        st.title("Max Lift Entry")

        d = st.date_input("Today's date",None, None, None, None)
    
        question_1 = st.selectbox('Select Lift',('','Pull Ups', 'Push Ups', 'Sit Ups', 'Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts'))
        st.write('You selected:', question_1)
    
        question_2 = st.slider('Select Weight', 0, 400)
        st.write('You selected:', question_2) 
    
        question_3 = st.selectbox('Select Reps',('', '1 rep max', '2 rep max', '3 rep max', '4 rep max', '5 rep max'))
        st.write('You selected:', question_3)
    
        question_4 = st.slider("Enter Body Weight", 0, 300)
        st.write('You selected:', question_4)
    
        question_5 = st.slider("Score How You Are Feeling Today", 0, 100)
        st.write('You selected:', question_5)
    

        if st.button("Submit New Max"):
            create_table()
            add_feedback(d, question_1, question_2, question_3, question_4, question_5)
            st.success("New Max Entered")
            st.balloons()

    rows = c.execute("SELECT date_submitted, Q1, Q2, Q3, Q4, Q5 FROM max_data").fetchall()




    
    lifts = st.selectbox("Show Lift Progress", ('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts'))


    if lifts:
        lift_df = df[df["Q1"].str.contains(lifts)]
        lift_df = lift_df.rename(columns={'date_submitted':'index'}).set_index('index')
        lift_1rm = lift_df[lift_df["Q3"].str.contains('1 rep max')]
        lift_2rm = lift_df[lift_df["Q3"].str.contains('2 rep max')]
        lift_3rm = lift_df[lift_df["Q3"].str.contains('3 rep max')]
        lift_4rm = lift_df[lift_df["Q3"].str.contains('4 rep max')]
        lift_5rm = lift_df[lift_df["Q3"].str.contains('5 rep max')]


        #st.line_chart(bsq1rm["Q2"])
        st.text("1 Rep Max")
        st.bar_chart(lift_1rm["Q2"])
        st.text("2 Rep Max")
        st.bar_chart(lift_2rm["Q2"])
        st.text("3 Rep Max")
        st.bar_chart(lift_3rm["Q2"])
        st.text("4 Rep Max")
        st.bar_chart(lift_4rm["Q2"])
        st.text("5 Rep Max")
        st.bar_chart(lift_5rm["Q2"])

    




       
    
    
    #st.sidebar.header("Entries")


    st.sidebar.dataframe(df)
    


    

        


if __name__ == '__main__':
    main()

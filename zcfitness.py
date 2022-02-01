# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 21:57:01 2022

@author: chags
"""

import streamlit as st

import numpy as np
import pandas as pd

import sqlite3
conn = sqlite3.connect('czfitness.db')
c = conn.cursor()
    

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS max_data(date_submitted DATE, Q1 TEXT, Q2 INTEGER, Q3 TEXT, Q4 INTEGER, Q5 INTEGER)')

def add_feedback(date_submitted, Q1, Q2, Q3, Q4, Q5):
    c.execute('INSERT INTO max_data (date_submitted,Q1, Q2, Q3, Q4, Q5) VALUES (?,?,?,?,?,?)',(date_submitted,Q1, Q2, Q3, Q4, Q5))
    conn.commit()

def main():

    st.sidebar.title("Max Lift Entry")

    d = st.sidebar.date_input("Today's date",None, None, None, None)
    
    question_1 = st.sidebar.selectbox('Select Lift',('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press'))
    st.sidebar.write('You selected:', question_1)
    
    question_2 = st.sidebar.slider('Select Weight', 0, 400)
    st.sidebar.write('You selected:', question_2) 
    
    question_3 = st.sidebar.selectbox('Select Reps',('', '1 rep max', '2 rep max', '3 rep max', '4 rep max', '5 rep max'))
    st.sidebar.write('You selected:', question_3)
    
    question_4 = st.sidebar.slider("Enter Body Weight", 0, 300)
    st.sidebar.write('You selected:', question_4)
    
    question_5 = st.sidebar.slider("Score How You Are Feeling Today", 0, 100)
    st.sidebar.write('You selected:', question_5)
    

    if st.sidebar.button("Submit New Max"):
        create_table()
        add_feedback(d, question_1, question_2, question_3, question_4, question_5)
        st.sidebar.success("New Max Entered")
    df = pd.read_sql("SELECT * FROM max_data", con = conn)
    rows = c.execute("SELECT date_submitted, Q1, Q2, Q3, Q4, Q5 FROM max_data").fetchall()
    st.sidebar.text("Data Entries")
    st.sidebar.dataframe(df)
    st.title("Data Dashboard")
    lifts = st.selectbox("Show Lift Progress", ('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press'))


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

    

    df1 = df.rename(columns={'date_submitted':'index'}).set_index('index')
    st.header("Entries")
    st.bar_chart(df1["Q3"], use_container_width=True)
    st.header("Body Weight")
    st.line_chart(df1["Q4"], use_container_width=True)
    st.header("Feeling")
    st.area_chart(df1["Q5"], use_container_width=True)
    

        


if __name__ == '__main__':
    main()
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
conn = sqlite3.connect('fit.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS max_data(date_submitted DATE, Lift TEXT, Weight INTEGER, Reps TEXT, BW INTEGER)')
    


def add_feedback(Date, Lift, Weight, Reps, BW):
    c.execute('INSERT INTO max_data (date_submitted, Lift, Weight, Reps, BW) VALUES (?,?,?,?,?)',(Date, Lift, Weight, Reps, BW))
    conn.commit()

def main():
    #c.execute('CREATE TABLE IF NOT EXISTS max_data(Date DATE, Lift TEXT, Weight INTEGER, Reps TEXT, BW INTEGER)')
    df = pd.read_sql("SELECT * FROM max_data", con = conn)
    #df["date_submitted"] = "10/26/1995"
    df1 = df.rename(columns={'date_submitted':'index'}).set_index('index')

    
    st.header("Data Entry")
    with st.expander("Add Lift Data"):
        st.title("Max Lift Entry")
        d = st.date_input("Today's date",None, None, None, None)
        
        question_1 = st.selectbox('Select Lift',('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'))
        st.write('You selected:', question_1)
        
        if question_1 is not '': 
            question_2 = st.number_input('Select Weight')
            st.write('You selected:', question_2) 
          
    
            question_3 = st.selectbox('Select Reps',('', '1 rep max', '2 rep max', '3 rep max', '4 rep max', '5 rep max'))
            st.write('You selected:', question_3)
    
        question_4 = st.number_input("Enter Body Weight")
        st.write('You selected:', question_4)
    
    

        if st.button("Submit New Max"):
            #create_table()
            add_feedback(d, question_1, question_2, question_3, question_4)
            st.success("New Max Entered")
            st.balloons()

            rows = c.execute("SELECT date_submitted, Lift, Weight, Reps, BW FROM max_data").fetchall()
    

        
      
 

    st.sidebar.header("Fitness Tracker 🏋️‍♀️")
    st.sidebar.image("https://sites.temple.edu/moodandcognitionlab/files/2021/05/zoe-277x300.jpeg")
    st.sidebar.text("Wake Up Beauty It's Time To Beast!")
    st.sidebar.table(df1)
    #bw_df = df1[df1["BW"] > 1]
    #st.sidebar.area_chart(bw_df)


 


    st.header("View Progress")
    st.bar_chart(df1["Weight"], use_container_width=True) 
    st.bar_chart(df1["Reps"], use_container_width=True) 
    st.bar_chart(df1["BW"], use_container_width=True) 

    st.header("View Lifts")
    lifts = st.selectbox("Show Lift Progress", ('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'))


    if lifts:
        lift_df = df1[df1["Lift"].str.contains(lifts)]
        #lift_df = lift_df.rename(columns={'date_submitted':'index'}).set_index('index')
        lift_1rm = lift_df[lift_df["Reps"].str.contains('1 rep max')]
        lift_2rm = lift_df[lift_df["Reps"].str.contains('2 rep max')]
        lift_3rm = lift_df[lift_df["Reps"].str.contains('3 rep max')]
        lift_4rm = lift_df[lift_df["Reps"].str.contains('4 rep max')]
        lift_5rm = lift_df[lift_df["Reps"].str.contains('5 rep max')]


        #st.line_chart(bsq1rm["2"])
        st.text("1 Rep Max")
        st.bar_chart(lift_1rm["Weight"])
        st.text("2 Rep Max")
        st.bar_chart(lift_2rm["Weight"])
        st.text("3 Rep Max")
        st.bar_chart(lift_3rm["Weight"])
        st.text("4 Rep Max")
        st.bar_chart(lift_4rm["Weight"])
        st.text("5 Rep Max")
        st.bar_chart(lift_5rm["Weight"])
        


if __name__ == '__main__':
    main()

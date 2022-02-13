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

    bs_goal = 325
    bench_goal = 230
    dead_goal = 325
    st.title("Data Dashboard")
 

    st.sidebar.header("Cole Fitness Tracking")
    df = pd.read_sql("SELECT * FROM max_data", con = conn)
    df1 = df.rename(columns={'date_submitted':'index'}).set_index('index')
    

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label = "Body Weight", value = int(df["Q4"].iloc[-1]), delta = (int(df["Q4"].iloc[-1]) - int(df["Q4"].iloc[-2])))

    with col2:
        st.metric(label = "Overal Wellness Score", value = int(df["Q5"].iloc[-1]), delta = (int(df["Q5"].iloc[-1]) - int(df["Q5"].iloc[-2])))
    
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

    




        

    bs_num = df[df["Q1"].str.contains("Back Squats")]
    bs_num = max(bs_num["Q2"])
    bp_num = df[df["Q1"].str.contains("Bench Press")]
    bp_num = max(bp_num["Q2"])
    dead_num = df[df["Q1"].str.contains("Deadlifts")]
    dead_num = max(dead_num["Q2"])
    print(bs_num)
    bs_cur = (bs_num/bs_goal) * 100
    bench_cur = (bp_num/bench_goal) * 100
    dead_cur = (dead_num/dead_goal)* 100
    print(dead_cur)
    #st.sidebar.header("Goals")
    fig, ax = plt.subplots(figsize=(6, 6))

    ax = plt.subplot(projection='polar')
    data = [bs_cur, bench_cur, dead_cur]
    #data = [10, 50, 100]
    startangle = 90
    colors = ['#4393E5', '#43BAE5', '#7AE6EA']
    xs = [(i * pi *2)/ 100 for i in data]
    ys = [-0.2, 1, 2.2]
    left = (startangle * pi *2)/ 360 #this is to control where the bar starts
    # plot bars and points at the end to make them round
    for i, x in enumerate(xs):
        ax.barh(ys[i], x, left=left, height=1, color=colors[i])
        ax.scatter(x+left, ys[i], s=350, color=colors[i], zorder=2)
        ax.scatter(left, ys[i], s=350, color=colors[i], zorder=2)
    
    plt.ylim(-4, 4)
    # legend
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Back Squat', markerfacecolor='#4393E5', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Bench Press', markerfacecolor='#43BAE5', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Deadlift', markerfacecolor='#7AE6EA', markersize=10)]
    ax.legend(handles=legend_elements, loc='center', frameon=False)
    # clear ticks, grids, spines
    plt.xticks([])
    plt.yticks([])
    ax.spines.clear()
    plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 1.0, 0.0, 0),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 1.0, 0),  # blue  with alpha = 20%
    })
    st.sidebar.pyplot(fig=fig)
    
    
    #st.sidebar.header("Entries")
    st.sidebar.bar_chart(df1["Q3"], use_container_width=True)

    st.sidebar.dataframe(df)
    


    

        


if __name__ == '__main__':
    main()

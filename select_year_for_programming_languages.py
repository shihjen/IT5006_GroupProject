import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# load the datasets


language = pd.read_csv('language.csv')
    
st.title('Usage of Programming Languages In Different Job Role')

# function to get the dataframe for year
@st.cache_data
def filter_year(data,year):
    year_df = data[data['Year']==year]
    return year_df

#@st.cache_data
def filter_data(data, year, job):
    if job == 'All Job':
        df = data[data['Year']==year]
    else:
        df = data[(data['Year']==year)&(data['Job_Role']==job)]
    return df

# function to get the list of programming languages 
@st.cache_data
def get_language(df):
    survey_language = df.columns.tolist()[2:]
    return survey_language

# function to get a list of jobs
@st.cache_data
def get_job(df):
    survey_job = df.Job_Role.unique().tolist()
    survey_job.insert(0,'All Job')
    return survey_job

job_list = get_job(language)

col1, col2 = st.columns(2)
year = col1.select_slider('Select year to view:', options=[2020, 2021, 2022])
selected_job = col2.selectbox('Select job role: ', options=job_list)


 


filtered_data = filter_data(language,year,selected_job)
programming_language = get_language(filtered_data)



@st.cache_data
def plot(data,pl):
    figure, axes = plt.subplots(figsize=(12, 10))
    for lang in pl:
        counts = data[lang].value_counts()
        axes.bar(counts.index, counts.values / len(data), label=lang)

    plt.title('Common Programming Languages Used on Regular Basis')
    plt.xlabel('Programming Language')
    plt.ylabel('Proportion')
    axes.grid(True)
    axes.legend()
    st.write(figure)


plot(filtered_data,programming_language)








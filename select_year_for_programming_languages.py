import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# load the datasets

@st.cache_data
def get_data(file_path):
    data = pd.read_csv(file_path, low_memory=False)
    return data

survey_2020 = get_data('../data/kaggle_survey_2020_responses.csv')
survey_2021 = get_data('../data/kaggle_survey_2021_responses.csv')
survey_2022 = get_data('../data/kaggle_survey_2022_responses.csv')

# the first column contains information how long the survey was completed by different participants
# drop the first column of all 3 datasets 
survey_2020.drop(survey_2020.columns[0], axis=1, inplace=True)
survey_2021.drop(survey_2021.columns[0], axis=1, inplace=True)
survey_2022.drop(survey_2022.columns[0], axis=1, inplace=True)

# rename the columns contain `salary` and `job role` data for all 3 datasets
survey_2020.rename(columns={'Q24':'Salary', 'Q5':'Job_Role', 'Q3':'ResidenceCountry'}, inplace=True)
survey_2021.rename(columns={'Q25':'Salary', 'Q5': 'Job_Role', 'Q3':'ResidenceCountry'}, inplace=True)
survey_2022.rename(columns={'Q29':'Salary', 'Q23': 'Job_Role', 'Q4':'ResidenceCountry'}, inplace=True)

# rename the columns for different programming language familarity
survey_2020.rename(columns={
                            'Q7_Part_1':'Python',
                            'Q7_Part_2':'R',
                            'Q7_Part_3':'SQL',
                            'Q7_Part_4':'C',
                            'Q7_Part_5':'C++',
                            'Q7_Part_6':'Java',
                            'Q7_Part_7':'Javascript',
                            'Q7_Part_8':'Julia',
                            'Q7_Part_9':'Swift',
                            'Q7_Part_10':'Bash',
                            'Q7_Part_11':'MATLAB',
                            'Q7_Part_12':'None',
                            'Q7_OTHER':'Other'
}, inplace=True)

survey_2021.rename(columns={
                            'Q7_Part_1':'Python',
                            'Q7_Part_2':'R',
                            'Q7_Part_3':'SQL',
                            'Q7_Part_4':'C',
                            'Q7_Part_5':'C++',
                            'Q7_Part_6':'Java',
                            'Q7_Part_7':'Javascript',
                            'Q7_Part_8':'Julia',
                            'Q7_Part_9':'Swift',
                            'Q7_Part_10':'Bash',
                            'Q7_Part_11':'MATLAB',
                            'Q7_Part_12':'None',
                            'Q7_OTHER':'Other'
}, inplace=True)

survey_2022.rename(columns={
                            'Q12_1':'Python',
                            'Q12_2':'R',
                            'Q12_3':'SQL',
                            'Q12_4':'C',
                            'Q12_5':'C#',
                            'Q12_6':'C++',
                            'Q12_7':'Java',
                            'Q12_8':'Javascript',
                            'Q12_9':'Bash',
                            'Q12_10':'PHP',
                            'Q12_11':'MATLAB',
                            'Q12_12': 'Julia',
                            'Q12_13':'Go',
                            'Q12_14':'None',
                           'Q12_15':'Other'
}, inplace=True)

# insert a year column into each dataframe
survey_2020['Year'] = pd.to_datetime('2020', format='%Y').year
survey_2021['Year'] = pd.to_datetime('2021', format='%Y').year
survey_2022['Year'] = pd.to_datetime('2022', format='%Y').year

# create subset of dataframes for analysis programming language used
language_2020 = survey_2020[['Year','Job_Role','Python','R','SQL','C','C++','Java','Javascript','Julia','Swift','Bash','MATLAB','None','Other']].iloc[1:,:]
language_2021 = survey_2021[['Year','Job_Role','Python','R','SQL','C','C++','Java','Javascript','Julia','Swift','Bash','MATLAB','None','Other']].iloc[1:,:]
language_2022 = survey_2022[['Year','Job_Role','Python','R','SQL','C','C#','C++','Java','Javascript','Bash','PHP','MATLAB','Julia','Go','None', 'Other']].iloc[1:,:]

# concatenate the dataframes
@st.cache_data
def concat_df():
    concat_df = pd.concat([language_2020, language_2021, language_2022])
    return concat_df

language = concat_df()
    
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








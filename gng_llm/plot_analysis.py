import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import random 


st.title('GSES and SUS Data Analysis')

# Function to conduct analysis
def analyze_data(df):
    '''Perform statistical analysis on the data'''

    # Conduct paired t-test
    t_stat, p_val = stats.ttest_rel(df['Post_GSES'], df['Pre_GSES'])

    # Calculate mean and standard deviation for GSES scores and SUS scores
    means = df[['Pre_GSES', 'Post_GSES', 'SUS']].mean()
    std_devs = df[['Pre_GSES', 'Post_GSES', 'SUS']].std()

    return t_stat, p_val, means, std_devs

# Functions to create plots
def plot_gses_scores(df):
    '''Create boxplot for GSES scores'''
    fig, ax = plt.subplots()
    sns.boxplot(data=df[['Pre_GSES', 'Post_GSES']], ax=ax)
    sns.despine()  # remove top and right axes spines
    return fig

def plot_sus_scores(df):
    '''Create distribution plot for SUS scores'''
    fig, ax = plt.subplots()
    sns.histplot(df['SUS'], bins=10, ax=ax, kde=True)  # use histplot (distplot is deprecated)
    sns.despine()  # remove top and right axes spines
    return fig

# UI for data input
num_subjects = st.number_input('Enter number of subjects', min_value=1, value=10, step=1)

data = {
    'Subject': ['Subject '+str(i) for i in range(1, num_subjects+1)],
    'Pre_GSES': [st.number_input('Pre GSES for Subject '+str(i), min_value=10, max_value=50, value=random.randint(15, 25)) for i in range(1, num_subjects+1)],
    'Post_GSES': [st.number_input('Post GSES for Subject '+str(i), min_value=10, max_value=50, value=random.randint(30, 45)) for i in range(1, num_subjects+1)],
    'SUS': [st.number_input('SUS for Subject '+str(i), min_value=0, max_value=100, value=random.randint(70, 85)) for i in range(1, num_subjects+1)]
}

df = pd.DataFrame(data)

if st.button('Analyze and Plot'):
    t_stat, p_val, means, std_devs = analyze_data(df)

    # Display analysis results
    st.write(f"Paired T-test Results:")
    st.write(f"t-statistic: {t_stat}")
    st.write(f"p-value: {p_val}")

    st.write("Means:")
    st.write(f"Pre_GSES: {means['Pre_GSES']}")
    st.write(f"Post_GSES: {means['Post_GSES']}")
    st.write(f"SUS: {means['SUS']}")

    st.write("Standard Deviations:")
    st.write(std_devs.to_string())

    # Display plots
    st.write("GSES Scores: Before and After Interaction")
    st.pyplot(plot_gses_scores(df))

    st.write("SUS Scores Distribution")
    st.pyplot(plot_sus_scores(df))
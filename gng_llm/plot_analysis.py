import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

st.title('GSES and SUS Data Analysis')

# Function to conduct analysis and plot
def analyze_and_plot(df):
    # Conduct paired t-test
    t_stat, p_val = stats.ttest_rel(df['Post_GSES'], df['Pre_GSES'])

    st.write(f"Paired T-test Results:")
    st.write(f"t-statistic: {t_stat}")
    st.write(f"p-value: {p_val}")

    # SUS scores analysis
    mean_SUS = df['SUS'].mean()
    std_SUS = df['SUS'].std()

    st.write(f"SUS Score Mean: {mean_SUS}")
    st.write(f"SUS Score Std Dev: {std_SUS}")

    # Data Visualization
    st.write("GSES Scores: Before and After Interaction")
    fig, ax = plt.subplots()
    sns.boxplot(data=df[['Pre_GSES', 'Post_GSES']])
    st.pyplot(fig)

    st.write("SUS Scores Distribution")
    fig, ax = plt.subplots()
    sns.distplot(df['SUS'], bins=10)
    st.pyplot(fig)

# UI for data input
num_subjects = st.number_input('Enter number of subjects', min_value=1, value=10, step=1)

data = {
    'Subject': ['Subject '+str(i) for i in range(1, num_subjects+1)],
    'Pre_GSES': [st.number_input('Pre GSES for Subject '+str(i), min_value=10, max_value=40, value=20) for i in range(1, num_subjects+1)],
    'Post_GSES': [st.number_input('Post GSES for Subject '+str(i), min_value=10, max_value=50, value=30) for i in range(1, num_subjects+1)],
    'SUS': [st.number_input('SUS for Subject '+str(i), min_value=0, max_value=100, value=70) for i in range(1, num_subjects+1)]
}

df = pd.DataFrame(data)

if st.button('Analyze and Plot'):
    analyze_and_plot(df)

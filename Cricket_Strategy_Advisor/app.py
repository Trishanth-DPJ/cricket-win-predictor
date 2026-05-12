import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from strategy_advisor import get_prescriptive_advice

st.set_page_config(page_title="Cricket Win Predictor & Strategy Advisor", layout="wide", page_icon="🏏")

# Load model and data
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl')
    return joblib.load(model_path)

@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'ipl_data.csv')
    return pd.read_csv(data_path)

@st.cache_data
def load_evaluation():
    results_path = os.path.join(os.path.dirname(__file__), 'models', 'evaluation_results.json')
    with open(results_path, 'r') as f:
        return json.load(f)

model = load_model()
df = load_data()
eval_results = load_evaluation()

teams = sorted(df['batting_team'].unique())
cities = sorted(df['city'].unique())

# Custom CSS for Premium Look
st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .card { background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #333; }
    .adv-title { color: #f39c12; font-weight: bold; font-size: 20px; }
    .bat-adv { color: #2ecc71; margin-top: 5px; }
    .bowl-adv { color: #e74c3c; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("🏏 Cricket Match Win Predictor & Strategy Advisor")
st.markdown("*Predictive & Prescriptive Analytics Mini-Project*")

tab1, tab2, tab3 = st.tabs(["🚀 Live Match Predictor", "📊 Exploratory Data Analysis", "⚙️ Model Evaluation"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Match Context")
        batting_team = st.selectbox("Batting Team", teams, index=0)
        bowling_team = st.selectbox("Bowling Team", teams, index=1)
        city = st.selectbox("City", cities)
        
        target_score = st.number_input("Target Score", min_value=50, max_value=300, value=180)
        current_score = st.number_input("Current Score", min_value=0, max_value=300, value=80)
        overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=19.5, value=10.0, step=0.1)
        wickets_fallen = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=2)
        
    with col2:
        st.subheader("Additional Stats")
        toss_winner = st.selectbox("Toss Winner", [batting_team, bowling_team])
        toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])
        recent_performance = st.number_input("Runs in Last 5 Overs", min_value=0, max_value=100, value=40)
        
        # Calculate derived metrics
        balls_bowled = int(overs_completed) * 6 + int((overs_completed % 1) * 10)
        balls_left = 120 - balls_bowled
        runs_left = target_score - current_score
        wickets_left = 10 - wickets_fallen
        crr = current_score / (balls_bowled / 6) if balls_bowled > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
        powerplay = 1 if overs_completed < 6 else 0
        
        st.metric("Required Run Rate (RRR)", round(rrr, 2))
        st.metric("Current Run Rate (CRR)", round(crr, 2))

    if st.button("Predict & Advise", type="primary", use_container_width=True):
        if batting_team == bowling_team:
            st.error("Batting and Bowling teams must be different!")
        else:
            # Create input dataframe
            input_df = pd.DataFrame({
                'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'city': [city],
                'target_score': [target_score],
                'current_score': [current_score],
                'balls_left': [balls_left],
                'wickets_left': [wickets_left],
                'crr': [crr],
                'rrr': [rrr],
                'toss_winner': [toss_winner],
                'toss_decision': [toss_decision],
                'powerplay': [powerplay],
                'recent_performance': [recent_performance]
            })
            
            # Predict
            prob = model.predict_proba(input_df)[0]
            win_prob = round(prob[1] * 100, 2)
            loss_prob = round(prob[0] * 100, 2)
            
            st.markdown("---")
            st.subheader("🤖 Predictive Analytics (Win Probability)")
            c1, c2 = st.columns(2)
            c1.metric(f"{batting_team}", f"{win_prob}%")
            c2.metric(f"{bowling_team}", f"{loss_prob}%")
            
            st.progress(win_prob / 100)
            
            st.markdown("---")
            st.subheader("🧠 Prescriptive Analytics (Strategy Advisor)")
            
            advice = get_prescriptive_advice(win_prob, wickets_left, balls_left, rrr, crr)
            
            ac1, ac2 = st.columns(2)
            with ac1:
                st.markdown('<div class="card"><div class="adv-title">🏏 Batting Strategy</div>', unsafe_allow_html=True)
                for a in advice['batting_advice']:
                    st.markdown(f'<div class="bat-adv">- {a}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with ac2:
                st.markdown('<div class="card"><div class="adv-title">🎯 Bowling Strategy</div>', unsafe_allow_html=True)
                for a in advice['bowling_advice']:
                    st.markdown(f'<div class="bowl-adv">- {a}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Exploratory Data Analysis")
    st.write("Visualizations derived from the synthetic IPL dataset.")
    
    st.subheader("Win Distribution by Toss Decision")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.countplot(data=df, x='toss_decision', hue='result', ax=ax, palette='viridis')
    ax.set_title("Match Result based on Toss Decision")
    ax.set_xticklabels(['Bat First', 'Field First'])
    ax.legend(['Loss', 'Win'])
    # Fix for st.pyplot warning
    st.pyplot(fig)
    
    st.subheader("Correlation Heatmap")
    num_df = df.select_dtypes(include=[np.number])
    fig2, ax2 = plt.subplots(figsize=(10,6))
    sns.heatmap(num_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax2)
    st.pyplot(fig2)

with tab3:
    st.header("Machine Learning Model Evaluation")
    st.write("Comparison of different predictive models tested on the dataset.")
    
    metrics_df = pd.DataFrame(eval_results).T[['Accuracy', 'Precision', 'Recall', 'F1-Score']]
    st.dataframe(metrics_df.style.highlight_max(axis=0, color='darkgreen'))
    
    st.subheader("Algorithm Accuracy Comparison")
    st.bar_chart(metrics_df['Accuracy'])

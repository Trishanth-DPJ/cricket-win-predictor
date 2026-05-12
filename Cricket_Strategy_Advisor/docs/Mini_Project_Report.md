# MINI PROJECT REPORT

**Project Title:** Cricket Match Win Predictor and Strategy Advisor
**Domain:** Predictive and Prescriptive Analytics

---

## 1. ABSTRACT
In the modern era of sports, data-driven decision-making has become paramount. This project presents a "Cricket Match Win Predictor and Strategy Advisor" that leverages both predictive and prescriptive analytics. Using historical match conditions, the system predicts the real-time winning probability of the batting team. Furthermore, rather than just providing a probability, the system utilizes prescriptive rule-based logic to advise team captains and coaches on immediate strategic shifts (e.g., batting aggressively, changing bowling lines, or rotating strike).

## 2. INTRODUCTION
### Predictive Analytics
Predictive analytics involves using historical data and machine learning algorithms to predict future outcomes. In this project, it is used to calculate the win probability of a team based on current match conditions like required run rate and wickets left.

### Prescriptive Analytics
Prescriptive analytics goes beyond predicting outcomes by suggesting actions you can take to affect those outcomes. In this project, it suggests tactical strategies based on the predicted probability and match context.

### Importance in Sports Analytics
In fast-paced games like T20 cricket (e.g., IPL), momentum changes rapidly. Coaches and captains need real-time, objective data to make critical decisions, removing emotional bias.

## 3. PROBLEM STATEMENT
Cricket teams often struggle to make optimal real-time decisions under pressure due to the cognitive overload of assessing multiple match variables simultaneously. There is a need for a dynamic, data-driven match strategy system that not only predicts the match outcome dynamically but also prescribes immediate tactical actions to optimize the chances of winning.

## 4. OBJECTIVES
1. To develop a Machine Learning model capable of predicting the win probability of an IPL cricket match based on real-time features.
2. To build a Prescriptive Analytics engine that provides strategic recommendations based on match context.
3. To design an interactive, user-friendly dashboard for real-time match tracking and visualization.

## 5. DATASET DETAILS
The dataset used mimics Kaggle's historical IPL datasets. Features include:
- **Categorical:** Batting team, Bowling team, Venue (City), Toss winner, Toss decision.
- **Numerical:** Target score, Current score, Balls left, Wickets left, Current Run Rate (CRR), Required Run Rate (RRR), Powerplay status, Recent performance.
- **Target Variable:** Result (1 for batting team win, 0 for loss).

## 6. METHODOLOGY & DATA PREPROCESSING
- **Handling Missing Values:** Handled inherently during synthetic generation and pipeline processing.
- **Encoding:** `OneHotEncoder` was used for categorical variables like Teams and City to prevent ordinal relationships from being implied.
- **Feature Scaling:** `StandardScaler` was used for numerical columns to ensure distance-based algorithms (like KNN) perform optimally.
- **Train-Test Split:** Data was split 80/20 for training and testing.

## 7. MACHINE LEARNING MODELS
We implemented and compared 5 models:
1. **Logistic Regression:** A linear model predicting probabilities via a sigmoid function. Advantage: Fast, interpretable. Disadvantage: Assumes linear relationship.
2. **Decision Tree:** Splits data into branches based on feature conditions. Advantage: Highly interpretable. Disadvantage: Prone to overfitting.
3. **Random Forest:** An ensemble of decision trees. Advantage: High accuracy, handles non-linearities well. Disadvantage: Slower to predict.
4. **K-Nearest Neighbor (KNN):** Classifies based on the proximity of data points. Advantage: Simple instance-based learning. Disadvantage: Slow inference on large datasets.
5. **Neural Network (MLP):** Multi-layer perceptron. Advantage: Learns complex patterns. Disadvantage: Black-box model, requires more data.

## 8. MODEL EVALUATION
Models were evaluated based on:
- **Accuracy:** Overall correctness.
- **Precision:** Exactness (minimizing false positives).
- **Recall:** Completeness (minimizing false negatives).
- **F1-Score:** Harmonic mean of precision and recall.

*Conclusion:* Logistic Regression and Random Forest performed exceptionally well (Accuracy > 93%). Logistic Regression was chosen as the final model for its speed and calibrated probabilities, which are essential for the prescriptive module.

## 9. PRESCRIPTIVE ANALYTICS MODULE
The core innovation of this project is the prescriptive strategy generator. Rule-based logic analyzes the context:
- **If win probability is < 40%:** Advise aggressive shots and strike rotation.
- **If wickets are falling (Wickets < 5, Overs left > 5):** Advise defensive play and stabilizing innings.
- **If RRR > 10:** Advise attacking weak bowlers and changing bowling side.
- **If Death Overs (Balls left < 30):** Advise strictly using yorkers and defensive field setups.

## 10. SYSTEM ARCHITECTURE
```
[Historical IPL Data] -> [Data Preprocessing Pipeline] -> [ML Model Training]
                                                                |
                                                                v
[Real-Time Inputs] -> [Predictive Model] -> (Win Probability) -> [Prescriptive Engine]
                                                                |
                                                                v
                                                       [Streamlit Dashboard UI]
```

## 11. FUTURE ENHANCEMENTS
- **Live API Integration:** Connecting to APIs like CricAPI for real-time automated data feeds.
- **Deep Learning Improvements:** Using LSTMs to analyze ball-by-ball sequential data.
- **Player-specific Strategy Engine:** Providing advice based on the specific batsman on strike vs the bowler.

## 12. CONCLUSION
This project successfully demonstrates the synergy between Predictive and Prescriptive Analytics in sports. The resulting application not only acts as a fun predictor for fans but serves as a viable conceptual prototype for data-driven coaching staffs in professional leagues.

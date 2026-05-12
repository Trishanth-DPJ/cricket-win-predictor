# VIVA QUESTIONS & ANSWERS

**1. What is the difference between Predictive and Prescriptive Analytics in your project?**
**Answer:** Predictive Analytics tells us *what will happen*—in this case, it predicts the winning probability of the batting team using historical data and ML models. Prescriptive Analytics tells us *what to do about it*—it provides actionable strategies (like changing bowling lines or taking aggressive shots) based on that prediction and the current match context.

**2. Why did you choose Logistic Regression/Random Forest for your final model?**
**Answer:** While Random Forest handles non-linear data well and gives high accuracy, Logistic Regression is much faster, highly interpretable, and provides very well-calibrated probability scores, which are essential for driving our prescriptive rule-based engine. (Both models achieved high accuracy in our tests).

**3. What is Data Preprocessing, and how did you handle categorical variables?**
**Answer:** Data preprocessing is cleaning and transforming raw data into an understandable format for ML models. We handled categorical variables like team names and cities using `OneHotEncoder`. This converts categories into binary columns (1s and 0s), preventing the model from assuming any numerical ranking between teams.

**4. How is the Current Run Rate (CRR) and Required Run Rate (RRR) calculated?**
**Answer:** 
- `CRR = (Current Score / Balls Bowled) * 6`
- `RRR = (Runs Left to Target / Balls Left) * 6`
These are dynamic features that change every ball and strongly correlate with the match outcome.

**5. What is a Confusion Matrix?**
**Answer:** A confusion matrix is an evaluation metric that summarizes the performance of a classification algorithm. It shows True Positives, True Negatives, False Positives, and False Negatives, helping us understand exactly where the model is making errors.

**6. Explain how your Prescriptive Analytics engine works.**
**Answer:** The prescriptive engine is rule-based. It takes the output of the predictive model (win probability) and contextual data (like wickets fallen and balls left). For example, if wickets left are < 4 but many overs remain, it triggers a "DEFENSIVE" rule, advising the team to stabilize the innings rather than play risky shots.

**7. Why did you use Streamlit for the frontend?**
**Answer:** Streamlit is a rapid-prototyping Python framework designed specifically for Machine Learning and Data Science applications. It allows us to easily integrate Python ML models (`.pkl` files) directly with web UI components without needing complex backend frameworks like Django or Flask.

**8. What challenges did you face during this project?**
**Answer:** The main challenge was defining the logic for the Prescriptive Analytics module. While prediction relies strictly on math, prescription requires translating human cricket knowledge and heuristics into logical IF-THEN rules based on numerical thresholds.

**9. How can you improve this model in the future?**
**Answer:** We could improve it by integrating a live CricAPI feed to pull real-time match data without manual input. We could also shift from traditional ML models to Deep Learning architectures like LSTMs that analyze sequential ball-by-ball patterns.

**10. What is Feature Scaling and why did you use StandardScaler?**
**Answer:** Feature scaling brings all numerical variables to a standard range. We used `StandardScaler` to ensure features with large ranges (like Target Score) do not dominate features with small ranges (like Wickets). It normalizes the data to have a mean of 0 and standard deviation of 1.

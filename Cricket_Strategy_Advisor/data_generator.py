import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_ipl_data(num_samples=10000):
    np.random.seed(42)
    random.seed(42)

    teams = [
        'Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 
        'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Rajasthan Royals', 
        'Delhi Capitals', 'Punjab Kings', 'Gujarat Titans', 'Lucknow Super Giants'
    ]
    
    cities = ['Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Jaipur', 'Delhi', 'Chandigarh', 'Ahmedabad', 'Lucknow']

    data = []

    for _ in range(num_samples):
        batting_team, bowling_team = random.sample(teams, 2)
        city = random.choice(cities)
        
        # Simulating a run chase (2nd innings)
        target_score = np.random.randint(140, 230)
        
        # Match situation
        overs_completed = round(np.random.uniform(5, 19.5), 1) # Overs from 5.0 to 19.5
        balls_bowled = int(overs_completed * 6)
        balls_left = 120 - balls_bowled
        
        # Wickets fallen (more likely to fall later in the innings)
        wickets_fallen = np.random.randint(0, min(10, int(overs_completed / 1.5) + 1))
        wickets_left = 10 - wickets_fallen
        
        # Current score
        current_score = int((target_score / 20) * overs_completed * np.random.uniform(0.7, 1.2))
        current_score = min(current_score, target_score - 1) # Haven't won yet
        
        runs_left = target_score - current_score
        
        crr = round((current_score * 6) / max(1, balls_bowled), 2)
        rrr = round((runs_left * 6) / max(1, balls_left), 2)
        
        # Additional features requested by user
        toss_winner = random.choice([batting_team, bowling_team])
        toss_decision = random.choice(['bat', 'field'])
        powerplay = 1 if overs_completed < 6 else 0
        recent_performance = min(current_score, np.random.randint(25, 65)) # Runs in last 5 overs
        
        # Determine the winner based on a crude heuristic to make the model learnable
        win_probability_score = (wickets_left * 10) + (crr * 5) - (rrr * 5)
        
        if win_probability_score > 30:
            result = 1 # Batting team wins
        elif win_probability_score < -10:
            result = 0 # Batting team loses
        else:
            result = np.random.choice([0, 1])
            
        data.append([
            batting_team, bowling_team, city, target_score, current_score, balls_left, 
            wickets_left, crr, rrr, toss_winner, toss_decision, powerplay, recent_performance, result
        ])

    columns = [
        'batting_team', 'bowling_team', 'city', 'target_score', 'current_score', 'balls_left', 
        'wickets_left', 'crr', 'rrr', 'toss_winner', 'toss_decision', 'powerplay', 'recent_performance', 'result'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    # Save the dataset
    output_path = os.path.join(os.path.dirname(__file__), 'data', 'ipl_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Synthetic dataset generated successfully at {output_path} with {num_samples} records.")

if __name__ == "__main__":
    generate_synthetic_ipl_data(15000)

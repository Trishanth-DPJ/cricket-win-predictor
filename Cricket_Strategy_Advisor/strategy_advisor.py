def get_prescriptive_advice(win_probability, wickets_left, balls_left, rrr, crr):
    """
    Generates prescriptive analytics recommendations based on match context.
    """
    batting_advice = []
    bowling_advice = []
    
    # 1. Low Win Probability Strategies
    if win_probability < 40:
        batting_advice.append("CRITICAL: Low win probability. Need to increase strike rotation immediately.")
        batting_advice.append("CRITICAL: Play aggressive shots and take calculated risks.")
        batting_advice.append("TACTIC: Consider sending in power hitters up the order.")
        
        bowling_advice.append("TACTIC: Maintain pressure, keep attacking lines to force errors.")
        bowling_advice.append("TACTIC: Attack weak batsmen with close-in fielders.")
    
    # 2. Wickets Falling / Low Wickets
    if wickets_left <= 4 and balls_left > 30:
        batting_advice.append("DEFENSIVE: Too many wickets lost. Play defensively to stabilize the innings.")
        batting_advice.append("DEFENSIVE: Focus on singles and doubles, avoid aerial shots.")
        
        bowling_advice.append("ATTACKING: Opposition is vulnerable. Bring in strike bowlers to finish the tail.")
    
    # 3. High Required Run Rate
    if rrr > 10:
        batting_advice.append("AGGRESSIVE: RRR is very high (>10). Need at least one boundary per over.")
        
        bowling_advice.append("DEFENSIVE: RRR is high. Bowl wide yorkers and set a deep boundary field.")
        if crr > 9:
            bowling_advice.append("TACTIC: Economy rate is high. Bring in a spinner to take pace off the ball or change bowling side.")
            
    # 4. Death Overs
    if balls_left <= 30:
        batting_advice.append("DEATH OVERS: Maximize scoring. Go for big hits on every loose delivery.")
        
        bowling_advice.append("DEATH OVERS: Strictly use yorkers, slower bouncers, and wide defensive lines.")
        bowling_advice.append("DEATH OVERS: Deploy a defensive field setup with sweepers on the boundary.")
        
    # Default positive states
    if win_probability >= 70:
        batting_advice.append("COMFORTABLE: High win probability. Avoid unnecessary risks, rotate strike.")
        bowling_advice.append("URGENT: Need immediate breakthroughs. Introduce mystery spinners or aggressive field settings.")
        
    if not batting_advice:
        batting_advice.append("Maintain current momentum. Play according to the merit of the ball.")
    if not bowling_advice:
        bowling_advice.append("Stick to the planned bowling lines and lengths. Build dot ball pressure.")
        
    return {
        "batting_advice": batting_advice,
        "bowling_advice": bowling_advice
    }

"""
1. The Funnel Math Engine (core/math_engine.py)
This script isolates exactly where candidates are dropping off across different software hiring stages.
"""


import pandas as pd

def calculate_funnel_bias(df: pd.DataFrame) -> dict:
    # Basic structural check
    if 'demographic' not in df.columns or 'last_stage_reached' not in df.columns:
        return {"error": "Missing required columns: 'demographic' or 'last_stage_reached'"}
    
    # 1. Gather baseline totals per subgroup
    total_counts = df['demographic'].value_counts().to_dict()
    
    # 2. Count candidates who survived past the automated AI screen stage
    passed_screen = df[df['last_stage_reached'] != 'Rejected at Screen']
    screen_passed_counts = passed_screen['demographic'].value_counts().to_dict()
    
    # 3. Count candidates who reached the final Hired milestone
    hired_counts = df[df['last_stage_reached'] == 'Hired']['demographic'].value_counts().to_dict()
    
    analysis = {}
    for group in total_counts.keys():
        total = total_counts[group]
        screened = screen_passed_counts.get(group, 0)
        hired = hired_counts.get(group, 0)
        
        # Calculate rates
        screening_rate = round(screened / total, 4) if total > 0 else 0.0
        hire_rate = round(hired / total, 4) if total > 0 else 0.0
        
        analysis[group] = {
            "total_applicants": total,
            "passed_screening": screened,
            "screening_pass_rate": screening_rate,
            "final_hired": hired,
            "overall_hire_rate": hire_rate
        }
        
    return analysis

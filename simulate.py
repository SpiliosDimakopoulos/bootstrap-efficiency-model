import numpy as np
import pandas as pd

def simulate_startups(n=1000, scenario="bootstrapped", seed=42):
    """
    Simulate startup data for analysis.
    
    Parameters:
    n: Number of startups to simulate
    scenario: Either "bootstrapped" or "funded"
    seed: Random seed for reproducibility
    
    Returns:
    DataFrame with simulated startup data
    """
    try:
        if n <= 0:
            raise ValueError("Number of startups must be positive")
        
        if scenario not in ["bootstrapped", "funded"]:
            raise ValueError("Scenario must be 'bootstrapped' or 'funded'")
        
        np.random.seed(seed)

        if scenario == "bootstrapped":
            CAC = np.random.uniform(500, 1500, n)
            OE = np.random.uniform(2000, 8000, n)
        else:  # funded
            CAC = np.random.uniform(200, 1000, n)
            OE = np.random.uniform(5000, 15000, n)

        R = np.random.uniform(10000, 50000, n)
        LTV = np.random.uniform(1000, 5000, n)
        D = np.random.uniform(0, 0.5, n)
        M = np.random.uniform(0, 1, n)  # Market size
        F = np.random.uniform(0, 1, n)  # Founder quality

        # Calculate efficiency with safety checks
        E = (R * LTV) / (CAC * OE) * (1 + D)
        
        # Check for any infinite or NaN values
        if np.isinf(E).any() or np.isnan(E).any():
            print("Warning: Some efficiency values are infinite or NaN")
            E = np.nan_to_num(E, nan=0.0, posinf=1000, neginf=0.0)

        df = pd.DataFrame({
            "R": R, "LTV": LTV, "CAC": CAC, "OE": OE,
            "D": D, "M": M, "F": F, "E": E
        })
        
        print(f"Successfully simulated {n} {scenario} startups")
        return df
        
    except Exception as e:
        print(f"Error in simulate_startups: {e}")
        raise

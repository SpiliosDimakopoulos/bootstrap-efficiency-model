import numpy as np
import statsmodels.api as sm
import warnings

def compute_success_probability(df, alpha0=-2, alpha1=3, alpha2=1, alpha3=1.5):
    """
    Compute success probability using logistic function.
    
    Parameters:
    df: DataFrame with columns E, M, F
    alpha0-3: Logistic regression coefficients
    
    Returns:
    DataFrame with added P_success column
    """
    try:
        # Check if required columns exist
        required_cols = ["E", "M", "F"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for infinite or NaN values
        if df[required_cols].isnull().any().any():
            raise ValueError("Data contains NaN values")
        
        if np.isinf(df[required_cols]).any().any():
            raise ValueError("Data contains infinite values")
        
        linear = alpha0 + alpha1 * df["E"] + alpha2 * df["M"] + alpha3 * df["F"]
        df["P_success"] = 1 / (1 + np.exp(-linear))
        
        # Clip to avoid perfect 0 or 1
        df["P_success"] = np.clip(df["P_success"], 1e-5, 1-1e-5)
        
        return df
    except Exception as e:
        print(f"Error in compute_success_probability: {e}")
        raise

def sensitivity_analysis(df, steps=5):
    """
    Perform sensitivity analysis on efficiency factor E.
    
    Parameters:
    df: DataFrame with column E
    steps: Number of sensitivity steps
    
    Returns:
    List of average adjusted E values
    """
    try:
        if "E" not in df.columns:
            raise ValueError("Column 'E' not found in DataFrame")
        
        results = []
        for d_factor in np.linspace(0, 1, steps):
            df_temp = df.copy()
            df_temp["E_adj"] = df_temp["E"] * (1 + d_factor)
            results.append(df_temp["E_adj"].mean())
        return results
    except Exception as e:
        print(f"Error in sensitivity_analysis: {e}")
        return []

def regression_check(df):
    """
    Perform logistic regression analysis.
    
    Parameters:
    df: DataFrame with columns E, M, F, P_success
    
    Returns:
    Fitted logistic regression model
    """
    try:
        required_cols = ["E", "M", "F", "P_success"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for data quality issues
        if df[required_cols].isnull().any().any():
            raise ValueError("Data contains NaN values")
        
        if len(df) < 10:
            raise ValueError("Insufficient data for regression (need at least 10 observations)")
        
        X = df[["E", "M", "F"]]
        y = df["P_success"]
        
        # Add constant term
        X = sm.add_constant(X)
        
        # Suppress convergence warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = sm.Logit(y, X).fit(disp=0)
        
        return model
    except Exception as e:
        print(f"Error in regression_check: {e}")
        raise

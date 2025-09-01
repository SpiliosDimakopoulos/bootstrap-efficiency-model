import os
from simulate import simulate_startups
from analysis import compute_success_probability, sensitivity_analysis, regression_check
from plots import plot_efficiency_distribution, plot_success_distribution
import numpy as np

def main():
    # Get the current script directory and create paths relative to it
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "..", "results")
    figures_dir = os.path.join(script_dir, "..", "paper", "figures")
    
    # Ensure folders exist
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # Simulate bootstrapped & funded
    df_boot = simulate_startups(2000, "bootstrapped")
    df_fund = simulate_startups(2000, "funded")

    # Compute success probability
    df_boot = compute_success_probability(df_boot)
    df_fund = compute_success_probability(df_fund)

    # Plots
    plot_efficiency_distribution(df_boot, filename="eff_boot.png")
    plot_efficiency_distribution(df_fund, filename="eff_fund.png")
    plot_success_distribution(df_boot, filename="prob_boot.png")
    plot_success_distribution(df_fund, filename="prob_fund.png")

    # Sensitivity analysis
    sens = sensitivity_analysis(df_boot)
    with open(os.path.join(results_dir, "summary.txt"), "w") as f:
        f.write("Average efficiencies under sensitivity steps:\n")
        f.write(str(sens))

    # Clip P_success just in case for regression
    df_boot["P_success"] = np.clip(df_boot["P_success"], 1e-5, 1-1e-5)

    # Regression with error handling
    try:
        model = regression_check(df_boot)
        with open(os.path.join(results_dir, "regression_output.txt"), "w") as f:
            f.write(str(model.summary()))
        print("Regression analysis completed successfully")
    except Exception as e:
        print(f"Regression analysis failed: {e}")
        with open(os.path.join(results_dir, "regression_error.txt"), "w") as f:
            f.write(f"Regression analysis failed with error: {e}")
    
    print("Analysis completed. Check the results/ and paper/figures/ directories.")

if __name__ == "__main__":
    main()

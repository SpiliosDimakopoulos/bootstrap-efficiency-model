import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid display issues
import matplotlib.pyplot as plt
import os

def plot_efficiency_distribution(df, E_critical=1, filename="efficiency_dist.png"):
    try:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paper", "figures")
        os.makedirs(output_dir, exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.hist(df["E"], bins=30, alpha=0.7, edgecolor='black')
        plt.axvline(E_critical, color='red', linestyle='--', label="E_critical", linewidth=2)
        plt.title("Efficiency Distribution", fontsize=14, fontweight='bold')
        plt.xlabel("Efficiency (E)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Efficiency plot saved: {filename}")
    except Exception as e:
        print(f"Error creating efficiency plot: {e}")

def plot_success_distribution(df, filename="prob_dist.png"):
    try:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paper", "figures")
        os.makedirs(output_dir, exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.hist(df["P_success"], bins=30, alpha=0.7, edgecolor='black')
        plt.title("Success Probability Distribution", fontsize=14, fontweight='bold')
        plt.xlabel("Success Probability (P_success)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Success probability plot saved: {filename}")
    except Exception as e:
        print(f"Error creating success probability plot: {e}")

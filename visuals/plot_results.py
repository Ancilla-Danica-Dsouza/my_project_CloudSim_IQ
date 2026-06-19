import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

sns.set_theme(style="darkgrid")
COLORS = {
    "blue"  : "#4C9BE8",
    "coral" : "#E8714C",
    "green" : "#4CE87A",
    "purple": "#9B4CE8",
    "gold"  : "#E8C44C"
}


def plot_iot_demand(df):
    """Graph 1: IoT device workload over 30 days."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7))

    # Top: raw demand
    ax1.plot(df["hour"], df["demand"],
             color=COLORS["blue"], linewidth=0.7, alpha=0.8)
    ax1.fill_between(df["hour"], df["demand"],
                     alpha=0.2, color=COLORS["blue"])

    # Mark holidays
    holiday_hours = df[df["is_holiday"] == 1]["hour"]
    for h in holiday_hours:
        ax1.axvline(x=h, color=COLORS["coral"],
                    alpha=0.4, linewidth=1.5, linestyle="--")

    ax1.set_title("IoT Device Demand — 30 Day Simulation",
                  fontsize=14, fontweight="bold")
    ax1.set_ylabel("Requests / Hour")
    holiday_patch = mpatches.Patch(
        color=COLORS["coral"], alpha=0.4, label="Holiday Spike"
    )
    ax1.legend(handles=[holiday_patch])

    # Bottom: active devices
    ax2.plot(df["hour"], df["active_devices"],
             color=COLORS["green"], linewidth=0.8)
    ax2.set_title("Active IoT Devices per Hour")
    ax2.set_xlabel("Simulation Hour")
    ax2.set_ylabel("Active Devices")

    plt.tight_layout()
    plt.savefig("docs/01_iot_demand.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[Plot] Saved: docs/01_iot_demand.png")


def plot_ml_predictions(y_test, preds):
    """Graph 2: ML model predictions vs actual demand."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: time series comparison
    ax = axes[0]
    ax.plot(y_test.values[:120], label="Actual",
            color=COLORS["blue"], linewidth=1.2)
    ax.plot(preds[:120], label="Predicted",
            color=COLORS["coral"], linewidth=1.2, linestyle="--")
    ax.set_title("ML Demand Forecast vs Actual (120 hrs)",
                 fontweight="bold")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Requests")
    ax.legend()

    # Right: scatter plot
    ax2 = axes[1]
    ax2.scatter(y_test.values, preds,
                alpha=0.4, color=COLORS["purple"], s=10)
    lim = max(y_test.max(), preds.max())
    ax2.plot([0, lim], [0, lim], color="white",
             linewidth=1, linestyle="--", label="Perfect prediction")
    ax2.set_title("Actual vs Predicted (Scatter)", fontweight="bold")
    ax2.set_xlabel("Actual Demand")
    ax2.set_ylabel("Predicted Demand")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("docs/02_ml_predictions.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[Plot] Saved: docs/02_ml_predictions.png")


def plot_cobb_douglas_surface():
    """Graph 3: 3D surface of Cobb-Douglas efficiency."""
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    from models.cobb_douglas import efficiency

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    C_range = np.linspace(1, 20, 40)
    M_range = np.linspace(2, 40, 40)
    C_grid, M_grid = np.meshgrid(C_range, M_range)
    E_grid = np.vectorize(efficiency)(C_grid, M_grid)

    surf = ax.plot_surface(C_grid, M_grid, E_grid,
                           cmap="plasma", alpha=0.85)
    fig.colorbar(surf, ax=ax, shrink=0.5, label="Efficiency")
    ax.set_xlabel("CPU Units")
    ax.set_ylabel("RAM (GB)")
    ax.set_zlabel("Requests / Dollar")
    ax.set_title("Cobb-Douglas Efficiency Surface\n"
                 "Q = 1.2 · C^0.6 · M^0.4",
                 fontweight="bold")

    plt.tight_layout()
    plt.savefig("docs/03_cobb_douglas_surface.png",
                dpi=150, bbox_inches="tight")
    plt.show()
    print("[Plot] Saved: docs/03_cobb_douglas_surface.png")


def plot_blockchain_audit(audit_df):
    """Graph 4: Blockchain audit trail visualization."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Cost over time
    axes[0].plot(audit_df["simulation_hour"],
                 audit_df["cost_usd"],
                 color=COLORS["gold"], linewidth=1.5)
    axes[0].set_title("Hourly Cloud Cost (USD)", fontweight="bold")
    axes[0].set_xlabel("Hour")
    axes[0].set_ylabel("Cost (USD)")

    # CPU allocation
    axes[1].bar(audit_df["simulation_hour"],
                audit_df["cpu_allocated"],
                color=COLORS["blue"], alpha=0.7, width=0.8)
    axes[1].set_title("CPU Allocation per Hour", fontweight="bold")
    axes[1].set_xlabel("Hour")
    axes[1].set_ylabel("CPU Units")

    # Prediction error
    axes[2].fill_between(
        audit_df["simulation_hour"],
        audit_df["prediction_error"],
        alpha=0.6, color=COLORS["coral"]
    )
    axes[2].set_title("ML Prediction Error", fontweight="bold")
    axes[2].set_xlabel("Hour")
    axes[2].set_ylabel("Error (requests)")

    plt.tight_layout()
    plt.savefig("docs/04_blockchain_audit.png",
                dpi=150, bbox_inches="tight")
    plt.show()
    print("[Plot] Saved: docs/04_blockchain_audit.png")
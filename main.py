"""
CloudSim IQ — Cloud Resource Allocation Optimizer
==================================================
Pipeline:
  IoT Simulation → ML Forecasting → 
  Cobb-Douglas Optimization → Blockchain Audit
"""

from models.demand_simulator  import simulate_iot_devices
from models.cobb_douglas      import optimal_allocation
from models.ml_predictor      import train
from models.blockchain_logger import AllocationChain
from visuals.plot_results     import (
    plot_iot_demand,
    plot_ml_predictions,
    plot_cobb_douglas_surface,
    plot_blockchain_audit
)

def banner(text):
    print(f"\n{'='*55}")
    print(f"  {text}")
    print(f"{'='*55}")


def main():
    banner("CloudSim IQ — Starting Pipeline")

    # ── STAGE 1: IoT Layer ─────────────────────────────────
    banner("Stage 1 │ IoT Device Simulation")
    df = simulate_iot_devices(n_devices=1000, days=30)
    plot_iot_demand(df)

    # ── STAGE 2: ML Layer ──────────────────────────────────
    banner("Stage 2 │ ML Demand Forecasting")
    model, df_feat, X_test, y_test, preds = train(df)
    plot_ml_predictions(y_test, preds)

    # ── STAGE 3: Math Layer ────────────────────────────────
    banner("Stage 3 │ Cobb-Douglas Optimization")
    plot_cobb_douglas_surface()

    # ── STAGE 4: Blockchain Layer ──────────────────────────
    banner("Stage 4 │ Blockchain Allocation Logging")
    chain = AllocationChain()

    test_hours   = df_feat.loc[X_test.index, "hour"].values
    actual_vals  = y_test.values

    for i in range(min(50, len(preds))):
        alloc = optimal_allocation(preds[i])
        block = chain.add(
            hour       = test_hours[i],
            actual     = actual_vals[i],
            predicted  = preds[i],
            allocation = alloc
        )
        if i < 5:  # print first 5 blocks
            print(f"  {block}")

    # Blockchain security demo
    chain.tamper_demo()

    # Export audit trail
    audit_df = chain.audit_report()
    print(f"\n[Blockchain] {len(chain.chain)-1} blocks logged")
    print(f"[Blockchain] Chain valid: {chain.is_valid()}")
    print(f"[Blockchain] Audit saved to data/blockchain_audit.csv")
    plot_blockchain_audit(audit_df)

    # ── SUMMARY ────────────────────────────────────────────
    banner("Pipeline Complete — Summary")
    print(f"  Total hours simulated : {len(df)}")
    print(f"  IoT devices simulated : 1,000")
    print(f"  ML R² score           : see Stage 2 output")
    print(f"  Blockchain blocks     : {len(chain.chain)}")
    print(f"  Avg hourly cost       : "
          f"${audit_df['cost_usd'].mean():.4f} USD")
    print(f"  Total simulated cost  : "
          f"${audit_df['cost_usd'].sum():.2f} USD")
    print(f"\n  Graphs saved in /docs/")
    print(f"  Data  saved in /data/")


if __name__ == "__main__":
    main()
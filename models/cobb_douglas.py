import numpy as np

# --- Cobb-Douglas Production Function ---
# Q = A * C^alpha * M^beta
# Q     = throughput (requests handled per hour)
# C     = CPU units allocated
# M     = Memory (GB) allocated
# A     = technology efficiency constant
# alpha = CPU elasticity (how much CPU contributes)
# beta  = Memory elasticity (how much RAM contributes)

A     = 1.2    # efficiency constant
ALPHA = 0.6    # CPU contributes 60%
BETA  = 0.4    # RAM contributes 40%

# Cloud pricing (simplified AWS-style)
PRICE_CPU_PER_UNIT = 0.048   # USD per CPU unit per hour
PRICE_RAM_PER_GB   = 0.012   # USD per GB RAM per hour


def throughput(C, M):
    """Compute cloud throughput using Cobb-Douglas."""
    return A * (C ** ALPHA) * (M ** BETA)


def cost(C, M):
    """Compute hourly cloud cost."""
    return (C * PRICE_CPU_PER_UNIT) + (M * PRICE_RAM_PER_GB)


def efficiency(C, M):
    """Requests served per dollar spent."""
    c = cost(C, M)
    return throughput(C, M) / c if c > 0 else 0


def optimal_allocation(predicted_demand):
    """
    Given predicted demand, find the CPU + RAM combo
    that handles the load at lowest cost.
    
    Strategy: scale CPU and RAM proportionally to demand,
    then find the most cost-efficient combination nearby.
    """
    # Base allocation
    base_cpu = max(1, int(predicted_demand / 800))
    base_ram = max(2, int(predicted_demand / 500))

    best_efficiency = 0
    best_cpu = base_cpu
    best_ram = base_ram

    # Search nearby allocations for best efficiency
    for c in range(max(1, base_cpu - 2), base_cpu + 5):
        for m in range(max(2, base_ram - 2), base_ram + 5):
            q = throughput(c, m)
            # Only consider if it can handle the demand
            if q * 100 >= predicted_demand:
                eff = efficiency(c, m)
                if eff > best_efficiency:
                    best_efficiency = eff
                    best_cpu = c
                    best_ram = m

    return {
        "cpu"       : best_cpu,
        "ram"       : best_ram,
        "throughput": round(throughput(best_cpu, best_ram), 2),
        "cost_usd"  : round(cost(best_cpu, best_ram), 4),
        "efficiency": round(best_efficiency, 4)
    }
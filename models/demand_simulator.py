import numpy as np
import pandas as pd

def simulate_iot_devices(n_devices=1000, days=30, seed=42):
    """
    Simulates IoT device traffic hitting a cloud server.
    
    Each device represents a smart endpoint:
    - Smartphones
    - Smart home sensors  
    - Wearables
    - Industrial monitors
    
    Returns hourly request data for 'days' days.
    """
    np.random.seed(seed)
    hours = days * 24
    records = []

    for hour in range(hours):
        hour_of_day = hour % 24
        day_number  = hour // 24
        day_of_week = day_number % 7

        # --- Device activity patterns ---
        # Devices sleep at night (12am-7am): only 20% active
        # Peak hours (9am-11pm): 85% active
        if hour_of_day < 7:
            active_ratio = 0.20
        elif hour_of_day < 9:
            active_ratio = 0.55
        elif hour_of_day < 23:
            active_ratio = 0.85
        else:
            active_ratio = 0.40

        # Weekends have higher activity
        if day_of_week >= 5:
            active_ratio = min(active_ratio * 1.3, 1.0)

        active_devices = int(n_devices * active_ratio)

        # Each active device sends Poisson-distributed requests
        # (Poisson is realistic — you studied this in stats!)
        device_requests = np.random.poisson(
            lam=5, size=active_devices
        ).sum()

        # --- Special events (simulate Black Friday / holiday) ---
        is_holiday = int(day_number in [10, 25])
        if is_holiday:
            device_requests = int(device_requests * 3.5)

        # --- Random server stress events ---
        is_stress = int(np.random.random() < 0.03)  # 3% chance
        if is_stress:
            device_requests = int(device_requests * 2.0)

        records.append({
            "hour"           : hour,
            "day"            : day_number,
            "hour_of_day"    : hour_of_day,
            "day_of_week"    : day_of_week,
            "active_devices" : active_devices,
            "demand"         : device_requests,
            "is_weekend"     : int(day_of_week >= 5),
            "is_holiday"     : is_holiday,
            "is_stress_event": is_stress
        })

    df = pd.DataFrame(records)

    # Save to CSV (your "cloud data lake")
    df.to_csv("data/iot_workload.csv", index=False)
    print(f"[IoT] Generated {hours} hours of data from "
          f"{n_devices} simulated devices")
    print(f"[IoT] Peak demand : {df['demand'].max():,} requests/hr")
    print(f"[IoT] Avg demand  : {df['demand'].mean():,.0f} requests/hr")

    return df
import pandas as pd

def generate_schedule(principal, rate, tenure, emi):
    balance = principal
    monthly_rate = rate / (12 * 100)

    data = []

    for month in range(1, tenure + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance -= principal_paid

        data.append({
            "Month": month,
            "Interest": round(interest, 2),
            "Principal": round(principal_paid, 2),
            "Balance": round(balance, 2)
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # 🔥 Save dataset (Data Engineering step)
    df.to_csv("emi_schedule.csv", index=False)

    return df
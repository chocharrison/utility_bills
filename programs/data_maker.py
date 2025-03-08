import pandas as pd
import numpy as np
import random
from faker import Faker
from sklearn.linear_model import LinearRegression

fake = Faker()
# Function to generate synthetic data
def generate_synthetic_data(n_samples):
    synthetic_data = []

    for i in range(n_samples):
        # Generate unique identifiers
        account_number = random.randint(2000000000, 3000000000)
        bill_number = random.randint(6000000000, 7000000000)

        # Random customer details
        issue_date = pd.Timestamp(f"2017-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}")
        due_date = issue_date + pd.Timedelta(days=random.randint(15, 45))
        customer_name = fake.name()
        address = fake.address().replace("\n", ", ")

        # Financial and charge details
        os_balance = round(random.uniform(0, 100), 2)
        advance_payment = round(random.uniform(-50, 50), 2)
        current_charges = round(random.uniform(50, 500), 2)
        tampering_inst = random.randint(0, 10)
        other_inst = random.randint(0, 5)
        other_charges = round(random.uniform(0, 20), 2)

        # Consumption and fees
        consumption_value = round(random.uniform(50, 1000), 2)
        meter_rent = round(random.uniform(0.5, 10), 2)
        country_fils = round(random.uniform(0.1, 1), 2)
        fuel_price_rate = round(random.uniform(0.1, 1), 2)
        tv_fees = round(random.uniform(0.5, 2), 2)
        garbage_fees = round(random.uniform(1, 20), 2)

        # Meter and period details
        meter_number = random.randint(100000, 999999)
        period = f"2018-{random.randint(1, 12):02d}-01 to 2018-{random.randint(1, 12):02d}-28"
        pres_read = random.randint(10000, 12000)
        prev_read = pres_read - random.randint(300, 700)
        calc_usage = pres_read - prev_read
        disc = round(random.uniform(0, 1), 2)
        mult_factor = round(random.uniform(1, 1.1), 2)
        exported_usage = round(calc_usage * mult_factor, 2)
        net_consumption = round(exported_usage, 2)

        # Outlier details
        is_obb = random.choice(["TRUE", "FALSE"])
        obb_amount = round(random.uniform(0, 50), 2) if is_obb == "TRUE" else ""

        # Previous months' consumption
        prev_month_periods = []
        prev_month_consumptions = []
        base_consumption = random.uniform(400, 700)
        trend_slope = round(random.uniform(-5, 5), 2)  # Generate synthetic trend slope

        for month in range(1, 12):
            month_period = f"2017-{random.randint(1, 12):02d}-01 to 2017-{random.randint(1, 12):02d}-28"
            prev_month_periods.append(month_period)

            # Add randomness to the slope to make it less perfect
            random_variation = np.random.normal(0, 10)  # Normal distribution for realistic variability
            consumption_value = base_consumption + trend_slope * month + random_variation
            prev_month_consumptions.append(round(max(consumption_value, 0), 2))  # Ensure non-negative values

        # Assemble the row
        synthetic_row = {
            "AccountNumber": account_number,
            "BillNumber": bill_number,
            "IssueDate": issue_date,
            "DueDate": due_date,
            "CustomerName": customer_name,
            "Address": address,
            "OSBalance": os_balance,
            "AdvancePayment": advance_payment,
            "CurrentCharges": current_charges,
            "TamperingInst": tampering_inst,
            "OtherInst": other_inst,
            "OtherCharges": other_charges,
            "ConsumptionValue": consumption_value,
            "MeterRent": meter_rent,
            "CountryFils": country_fils,
            "FuelPriceRate": fuel_price_rate,
            "TVFees": tv_fees,
            "GarbageFees": garbage_fees,
            "MeterNumber": meter_number,
            "Period": period,
            "PresRead": pres_read,
            "PrevRead": prev_read,
            "CalcUsage": calc_usage,
            "Disc": disc,
            "MultFactor": mult_factor,
            "ExportedUsage": exported_usage,
            "NetConsumption": net_consumption,
            "IsObb": is_obb,
            "ObbAmount": obb_amount,
            "Language": random.choice(["English", "Arabic"]),
        }

        for month in range(1, 12):
            synthetic_row[f"PrevMonPeriod_{month}"] = prev_month_periods[month - 1]
            synthetic_row[f"PrevMonConsumption_{month}"] = prev_month_consumptions[month - 1]

        synthetic_data.append(synthetic_row)

    outlier_index = random.randint(0, n_samples - 1)
    synthetic_data[outlier_index]["ConsumptionValue"] *= random.uniform(2, 5)  # Make it significantly larger
    
    return pd.DataFrame(synthetic_data)

# Generate and save synthetic data
n_samples = 100  # Number of synthetic rows to generate
synthetic_data = generate_synthetic_data(n_samples)

# Save to CSV
synthetic_data.to_csv("synthetic_data.csv", index=False)
print("Synthetic data generated and saved to 'synthetic_data.csv'.")

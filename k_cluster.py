

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

# Load the data
data_path = "synthetic_data.csv"  # Update path as needed
df = pd.read_csv(data_path)

# Restructure the data: Melt previous months' data into time series format
melted_df = pd.melt(
    df,
    id_vars=["BillNumber"],
    value_vars=[f"PrevMonConsumption_{i}" for i in range(1, 13)],
    var_name="Month",
    value_name="Consumption",
)

# Add a numerical month for sorting and trend analysis
melted_df["MonthNumber"] = melted_df["Month"].str.extract(r"(\d+)").astype(int)
melted_df = melted_df.sort_values(["BillNumber", "MonthNumber"])

# Calculate Z-scores to detect outliers
melted_df["ZScore"] = melted_df.groupby("BillNumber")["Consumption"].transform(zscore)

# Flag outliers (e.g., Z-score > 3 or < -3)
melted_df["Outlier"] = (melted_df["ZScore"].abs() > 3)

# Visualize trends for each BillNumber
sns.set(style="whitegrid")
for bill_number, group in melted_df.groupby("BillNumber"):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=group, x="MonthNumber", y="Consumption", label="Consumption Trend")
    sns.scatterplot(
        data=group[group["Outlier"]], x="MonthNumber", y="Consumption", color="red", label="Outliers"
    )
    plt.title(f"Consumption Trend for BillNumber: {bill_number}")
    plt.xlabel("Month (1 = Most Recent)")
    plt.ylabel("Consumption")
    plt.legend()
    plt.show()

# Save processed outlier data for review
outliers = melted_df[melted_df["Outlier"]]
outliers.to_csv("outliers_detected.csv", index=False)
print("Outliers saved to '/mnt/data/outliers_detected.csv'")

import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

# Load the data
data = pd.read_csv("sample.csv")

# Filter required columns
columns_needed = ['BillNumber', 'IssueDate', 'ConsumptionValue'] + \
                 [f'PrevMonPeriod_{i}' for i in range(1, 12)] + \
                 [f'PrevMonConsumption_{i}' for i in range(1, 12)]

data = data[columns_needed]

# Process IssueDate
data['IssueDate'] = pd.to_datetime(data['IssueDate'])

# Function to extract start date from ranges (e.g., "2018-01-01 to 2018-01-31")
def extract_start_date(date_range):
    if isinstance(date_range, str):
        return date_range.split(" to ")[0]
    return None

# Extract start dates from PrevMonPeriod columns
for i in range(1, 12):
    data[f'PrevMonPeriod_{i}'] = data[f'PrevMonPeriod_{i}'].apply(extract_start_date)
    data[f'PrevMonPeriod_{i}'] = pd.to_datetime(data[f'PrevMonPeriod_{i}'], errors='coerce')

# Combine Historical Periods and Consumption into Time Series for Each User
user_data = []
for i in range(1, 12):
    user_data.append(
        pd.DataFrame({
            'AccountNumber': data['BillNumber'],
            'Date': data[f'PrevMonPeriod_{i}'],
            'Consumption': data[f'PrevMonConsumption_{i}']
        })
    )

# Add Current Period for Each User
current_data = pd.DataFrame({
    'AccountNumber': data['BillNumber'],
    'Date': data['IssueDate'],
    'Consumption': data['ConsumptionValue']
})

# Combine all periods into a single DataFrame
trend_data = pd.concat(user_data, ignore_index=True).dropna()
trend_data = trend_data.sort_values(['AccountNumber', 'Date'])

# Plot trends for each user
plt.figure(figsize=(14, 8))
#sns.set(style="whitegrid")

# Group by AccountNumber and plot each user's trend with a unique color
for account, group in trend_data.groupby('AccountNumber'):
    plt.plot(group['Date'], group['Consumption'], marker='o', label=f'Account {account}')

# Customize the plot
plt.title("Consumption Trends for Each User", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Consumption", fontsize=12)
plt.legend(title="Account Numbers", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(True)
plt.show()

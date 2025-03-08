import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load data
data = pd.read_csv('synthetic_data.csv')

# Feature Engineering
# Calculate moving averages
data['moving_avg_3'] = data[[f'PrevMonConsumption_{i}' for i in range(1, 4)]].mean(axis=1)
data['moving_avg_6'] = data[[f'PrevMonConsumption_{i}' for i in range(1, 7)]].mean(axis=1)

# Calculate trend (slope)
def calculate_slope(row):
    x = np.arange(1, 12)
    y = row[[f'PrevMonConsumption_{i}' for i in range(1, 12)]].values
    reg = LinearRegression().fit(x.reshape(-1, 1), y)
    return reg.coef_[0]

data['trend_slope'] = data.apply(calculate_slope, axis=1)

# Lag features (differences between consecutive months)
for i in range(1, 11):
    data[f'lag_diff_{i}'] = data[f'PrevMonConsumption_{i}'] - data[f'PrevMonConsumption_{i+1}']

# Prepare features and target
features = [f'PrevMonConsumption_{i}' for i in range(1, 12)] + ['moving_avg_3', 'moving_avg_6', 'trend_slope']
features += [f'lag_diff_{i}' for i in range(1, 11)]
X = data[features]
y = data['ConsumptionValue']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train regression model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict current consumption
data['predicted_consumption'] = model.predict(X)

# Calculate residuals
data['residual'] = data['ConsumptionValue'] - data['predicted_consumption']

# Define outliers (e.g., residuals exceeding 2 standard deviations)
threshold = 2 * data['residual'].std()
data['is_outlier'] = data['residual'].abs() > threshold

# Save relevant results
selected_columns = ['BillNumber', 'ConsumptionValue', 'predicted_consumption', 'residual', 'is_outlier']
outliers = data[selected_columns]

outliers.to_csv('outliers.csv', index=False)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

print(f"Outliers saved in 'outliers.csv'")

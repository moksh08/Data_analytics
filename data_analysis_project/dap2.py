import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle

file_path = "C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Select features and target variable
feature_columns = ['duration', 'days_left', 'time_of_day']  # Adjusted features for price prediction
target_column = 'price'  # Change this to your actual target variable for price prediction

# Split the dataset into features and target variable
X = df[feature_columns]
y = df[target_column]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model (for price prediction)
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Print predicted values
print("Predicted Values:")
print(predictions)

# Print regression metrics
print("\nRegression Metrics:")
print(f"Mean Squared Error: {mean_squared_error(y_test, predictions):.2f}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, predictions):.2f}")
print(f"R^2 Score: {r2_score(y_test, predictions):.2f}")

# Save the trained model to a pickle file
with open('flight_price_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

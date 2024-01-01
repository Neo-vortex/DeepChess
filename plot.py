import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def advanced_analyze_data(csv_file):
    # Read the CSV file without header
    data = pd.read_csv(csv_file, header=None, names=['True_Score', 'Predicted_Score'])

    # Descriptive statistics
    statistics = data.describe()

    # Correlation matrix
    correlation_matrix = data.corr()

    # Scatter plot with regression line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='True_Score', y='Predicted_Score', data=data)
    plt.title('Scatter Plot with Regression Line')
    plt.xlabel('True_Score')
    plt.ylabel('Predicted_Score')
    plt.show()

    # Residual analysis
    residuals = data['True_Score'] - data['Predicted_Score']
    
    # Q-Q plot for residuals
    plt.figure(figsize=(10, 6))
    stats.probplot(residuals, plot=plt)
    plt.title('Q-Q Plot for Residuals')
    plt.show()

    # Distribution of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, bins=30, kde=True)
    plt.title('Distribution of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.show()

    # Calculate performance metrics
    mse = np.mean((data['True_Score'] - data['Predicted_Score'])**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(data['True_Score'] - data['Predicted_Score']))
    r_squared = np.corrcoef(data['True_Score'], data['Predicted_Score'])[0, 1]**2

    # Print advanced statistical information
    print("Descriptive Statistics:")
    print(statistics)
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    print(f"\nMean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"R-squared: {r_squared}")

# Example usage
advanced_analyze_data('evaluation_results.csv')
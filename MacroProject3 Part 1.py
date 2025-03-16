import pandas as pd

# Change pandas display options to show all rows and columns
pd.set_option('display.max_rows', None)  # No limit on the number of rows
pd.set_option('display.max_columns', None)  # No limit on the number of columns
pd.set_option('display.width', None)  # Disable line wrapping
pd.set_option('display.max_colwidth', None)  # Show full content of each column

file_path = "C:/Users/koush/OneDrive - University of Cincinnati/R/Macro/Assignment3.csv"

# Sample dataset (replace with actual CSV file)
df = pd.read_csv(file_path)

# Pivot the table so "Measure" values become columns
df_pivot = df.pivot(index=["REF_AREA", "Reference area","TIME_PERIOD"], columns=["Measure"], values="OBS_VALUE")

# Reset index to flatten the table
df_pivot.reset_index(inplace=True)

print(df_pivot)

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Ensure 'Time' is treated as a string
df_pivot["Time"] = df_pivot["TIME_PERIOD"].astype(str)

# Extract year and quarter
df_pivot["Year"] = df_pivot["Time"].str[:4]  # First 4 characters = Year
df_pivot["Quarter"] = df_pivot["Time"].str[5:]  # After the dash = Q1, Q2, etc.

# Mapping quarters to corresponding start months
quarter_to_month = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}

# Replace quarter with the corresponding month
df_pivot["Month"] = df_pivot["Quarter"].map(quarter_to_month)

# Create a new 'Date' column in the format YYYY-MM (first month of the quarter)
df_pivot["Date"] = df_pivot["Year"] + "-" + df_pivot["Month"]

# Convert to datetime format
df_pivot["Date"] = pd.to_datetime(df_pivot["Date"], format="%Y-%m")

# Set time as index
df_pivot.set_index("Date", inplace=True)

# Drop unnecessary columns
df_pivot.drop(columns=["Year", "Quarter", "Month"], inplace=True)

# List of columns to difference
columns_to_diff = [
    "Gross domestic product, nominal value, market prices",
    "Labour force",
    "Private final consumption expenditure, nominal value, appropriation account",
    "Long-term interest rate on government bonds"
    ]

# Group by 'Reference area' (country) and apply differencing for each group
df_diff = df_pivot.groupby('Reference area')[columns_to_diff].diff()

# List of other columns you want to keep (not differenced)
other_columns = [col for col in df_pivot.columns if col not in columns_to_diff]

# Concatenate the differenced columns with the rest of the columns
df_diff = pd.concat([df_pivot[other_columns], df_diff], axis=1)

# Extract the year part from the index (assuming the index is in string format)
df_diff = df_diff[~df_diff.index.year.isin([2025, 2026])]
print(df_diff)

# Group by 'Reference area' (country) and calculate the standard deviation for a specific column
std_by_country = df_diff.groupby('Reference area')[columns_to_diff].std()
print(std_by_country)

# Group by 'Reference area' (country)
grouped_by_country = df_diff.groupby('Reference area')[columns_to_diff]

# Calculate correlations for each country
country_correlations = grouped_by_country.corr()

# Extract the correlation of each variable with GDP (output)
gdp_correlations_by_country = country_correlations['Gross domestic product, nominal value, market prices']

# Print the correlations for each country
pd.set_option('display.max_rows', None)  # Make sure all rows are displayed
pd.set_option('display.max_columns', None)  # Make sure all columns are displayed
print(gdp_correlations_by_country)
# Set the 'TIME_PERIOD' as the index for better time series plotting
df_diff.set_index('TIME_PERIOD', inplace=True)

# Get the unique countries (or regions) in the data
countries = df_diff['Reference area'].unique()

# Loop through each country (or region) and create separate plots for each column
for country in countries:
    # Filter data by country (or region)
    country_data = df_diff[df_diff['Reference area'] == country]
    
    # Loop through each specified column and create a separate plot for the country
    for column in columns_to_diff:
        # Create a new figure for each column of the current country
        plt.figure(figsize=(10, 6))
        plt.plot(country_data.index, country_data[column], label=column, color='b')
        
        # Add title and labels
        plt.title(f'{column} for {country} Over Time', fontsize=16)
        plt.xlabel('TIME_PERIOD', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend()

        # Clean up the x-axis to reduce clutter
        plt.xticks(country_data.index[::4])  # Adjust to show every 4th time period
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        
        # Automatically adjust layout to avoid overlap of labels
        plt.tight_layout()
        plt.show()

file_path2 = "C:/Users/koush/OneDrive - University of Cincinnati/R/Macro/differenced.csv"
# Save the DataFrame as a CSV
df_diff.to_csv(file_path2, index=False)  # index=False to avoid writing row numbers

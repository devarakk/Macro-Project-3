import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as op

file_path = r"C:\Users\docla\OneDrive - University of Cincinnati\Rprojects\Macro Project 3 data.xlsx"
xls = pd.ExcelFile(file_path)

# Load relevant sheets for MSFT, WMT, and IBM
msft_df = pd.read_excel(xls, sheet_name='MSFT')
wmt_df = pd.read_excel(xls, sheet_name='WMT')
ibm_df = pd.read_excel(xls, sheet_name='IBM')

# Function to convert 'datacqtr' to a proper datetime format
def convert_quarter_to_date(df):
    df['year'] = df['datacqtr'].str[:4].astype(int)
    df['quarter'] = df['datacqtr'].str[4:]
    df['date'] = pd.to_datetime(df['year'].astype(str) + df['quarter'].replace(
        {'Q1': '-01-01', 'Q2': '-04-01', 'Q3': '-07-01', 'Q4': '-10-01'}), format='%Y-%m-%d')
    return df

# Apply conversion
msft_df = convert_quarter_to_date(msft_df)
wmt_df = convert_quarter_to_date(wmt_df)
ibm_df = convert_quarter_to_date(ibm_df)

#############

# Define periods
pre_gfc = (msft_df['year'] >= 2004) & (msft_df['year'] <= 2006)
during_gfc = (msft_df['year'] >= 2007) & (msft_df['year'] <= 2009)
post_gfc = (msft_df['year'] >= 2010) & (msft_df['year'] <= 2012)

#################################################################################################################
# Function to compute summary statistics with company names
def compute_summary_stats(df, company_name):
    return pd.DataFrame({
        'Company': [company_name] * 3,  # Add company name to each row
        'Period': ['Pre-GFC', 'During-GFC', 'Post-GFC'],
        'ROA': [df.loc[pre_gfc, 'roa'].mean(), df.loc[during_gfc, 'roa'].mean(), df.loc[post_gfc, 'roa'].mean()],
        'Debt-to-Assets': [df.loc[pre_gfc, 'debt_assets'].mean(), df.loc[during_gfc, 'debt_assets'].mean(), df.loc[post_gfc, 'debt_assets'].mean()],
        'Current Ratio': [df.loc[pre_gfc, 'curr_ratio'].mean(), df.loc[during_gfc, 'curr_ratio'].mean(), df.loc[post_gfc, 'curr_ratio'].mean()],
        'Revenue': [df.loc[pre_gfc, 'revtq'].mean(), df.loc[during_gfc, 'revtq'].mean(), df.loc[post_gfc, 'revtq'].mean()]
    })

# Generate summaries with company names
msft_summary = compute_summary_stats(msft_df, "Microsoft")
wmt_summary = compute_summary_stats(wmt_df, "Walmart")
ibm_summary = compute_summary_stats(ibm_df, "IBM")

# Combine all summaries for a structured table
summary_df = pd.concat([msft_summary, wmt_summary, ibm_summary], ignore_index=True)

# Display the corrected table
from IPython.display import display
display(summary_df)
summary_df.to_excel("firm_gfc.xlsx", index=False)
###############################################################################################################################

# Plot ROA trends
plt.figure(figsize=(10, 5))
plt.plot(msft_df['date'], msft_df['roa'], label='MSFT', marker='o', linestyle='-')
plt.plot(wmt_df['date'], wmt_df['roa'], label='WMT', marker='o', linestyle='-')
plt.plot(ibm_df['date'], ibm_df['roa'], label='IBM', marker='o', linestyle='-')

plt.axvline(pd.to_datetime('2007-01-01'), color='r', linestyle='--', label='GFC Start')
plt.axvline(pd.to_datetime('2009-12-31'), color='g', linestyle='--', label='GFC End')

plt.xlabel('Year')
plt.ylabel('Return on Assets (ROA)')
plt.title('Return on Assets (ROA) Over Time')
plt.legend()
plt.grid(True)
plt.savefig("ROA_plot.png", dpi=300, bbox_inches='tight')
plt.show()

# Plot Debt-to-Assets Ratio trends
plt.figure(figsize=(10, 5))
plt.plot(msft_df['date'], msft_df['debt_assets'], label='MSFT', marker='o', linestyle='-')
plt.plot(wmt_df['date'], wmt_df['debt_assets'], label='WMT', marker='o', linestyle='-')
plt.plot(ibm_df['date'], ibm_df['debt_assets'], label='IBM', marker='o', linestyle='-')

plt.axvline(pd.to_datetime('2007-01-01'), color='r', linestyle='--', label='GFC Start')
plt.axvline(pd.to_datetime('2009-12-31'), color='g', linestyle='--', label='GFC End')

plt.xlabel('Year')
plt.ylabel('Debt-to-Assets Ratio')
plt.title('Debt-to-Assets Ratio Over Time')
plt.legend()
plt.grid(True)
plt.savefig("debttoasset_ratio_plot.png", dpi=300, bbox_inches='tight')
plt.show()

# Plot Current Ratio trends
plt.figure(figsize=(10, 5))
plt.plot(msft_df['date'], msft_df['curr_ratio'], label='MSFT', marker='o', linestyle='-')
plt.plot(wmt_df['date'], wmt_df['curr_ratio'], label='WMT', marker='o', linestyle='-')
plt.plot(ibm_df['date'], ibm_df['curr_ratio'], label='IBM', marker='o', linestyle='-')

plt.axvline(pd.to_datetime('2007-01-01'), color='r', linestyle='--', label='GFC Start')
plt.axvline(pd.to_datetime('2009-12-31'), color='g', linestyle='--', label='GFC End')

plt.xlabel('Year')
plt.ylabel('Current Ratio')
plt.title('Current Ratio Over Time')
plt.legend()
plt.grid(True)
plt.savefig("current_ratio_plot.png", dpi=300, bbox_inches='tight')
plt.show()

#########


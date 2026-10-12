import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
df = pd.read_csv(r"C:\Users\PC\Downloads\Unemployment in India.csv",encoding="cp1252")

# Clean column names
df.columns = df.columns.str.strip()

print("First 5 rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# Find the required columns
date_col = "Date"
rate_col = "Estimated Unemployment Rate (%)"

# Clean data
df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
df[rate_col] = pd.to_numeric(df[rate_col], errors="coerce")

df = df.drop_duplicates()
df = df.dropna(subset=[date_col, rate_col])
df = df[(df[rate_col] >= 0) & (df[rate_col] <= 100)]

# Create output folder
Path("outputs").mkdir(exist_ok=True)

# Basic statistical analysis
print("\nAverage Unemployment Rate:")
print(round(df[rate_col].mean(), 2), "%")

print("\nMaximum Unemployment Rate:")
print(round(df[rate_col].max(), 2), "%")

print("\nMinimum Unemployment Rate:")
print(round(df[rate_col].min(), 2), "%")

# Monthly unemployment trend
df["Month"] = df[date_col].dt.to_period("M")
monthly_data = df.groupby("Month")[rate_col].mean()

plt.figure(figsize=(12, 6))
plt.plot(monthly_data.index.astype(str), monthly_data.values,
         marker="o")
plt.title("Monthly Unemployment Rate Analysis")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/monthly_unemployment_trend.png")
plt.show()

# COVID-19 comparison
before_covid = df[df[date_col] < "2020-03-01"]
during_covid = df[df[date_col] >= "2020-03-01"]

if not before_covid.empty and not during_covid.empty:
    before_rate = before_covid[rate_col].mean()
    during_rate = during_covid[rate_col].mean()

    print("\nAverage Rate Before COVID-19:",
          round(before_rate, 2), "%")
    print("Average Rate From March 2020 Onward:",
          round(during_rate, 2), "%")

    plt.figure(figsize=(7, 5))
    plt.bar(
        ["Before COVID-19", "March 2020 Onward"],
        [before_rate, during_rate]
    )
    plt.title("Unemployment Rate: COVID-19 Comparison")
    plt.ylabel("Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig("outputs/covid_comparison.png")
    plt.show()

# Regional analysis
if "Region" in df.columns:
    region_data = df.groupby("Region")[rate_col].mean()
    region_data = region_data.sort_values(ascending=False).head(10)

    print("\nTop 10 Regions by Average Unemployment:")
    print(region_data)

    region_data.sort_values().plot(kind="barh", figsize=(9, 6))
    plt.title("Top 10 Regions by Average Unemployment")
    plt.xlabel("Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig("outputs/regional_unemployment.png")
    plt.show()

# Save cleaned data
df.to_csv("outputs/cleaned_unemployment.csv", index=False)

print("\nTask 2 completed successfully!")
print("Check the outputs folder for results and graphs.")
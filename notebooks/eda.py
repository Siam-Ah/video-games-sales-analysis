import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Cleaning Data ---

# Load dataset
file_path = "..\\data\\raw\\Video_Game_Sales_as_of_Jan_2017.csv"
df = pd.read_csv(file_path)

# Inspect dataset
print("Shape of dataset:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Convert User_score to same scale as Critic_Score (0-100)
if df['User_Score'].max() <= 10:
    df['User_Score'] = df['User_Score'] * 10

print("\nAfter scaling User_Score:")
print("Critic_Score range:", df['Critic_Score'].min(), "-", df['Critic_Score'].max())
print("User_Score range:", df['User_Score'].min(), "-", df['User_Score'].max())

# Handle missing values
# Fill missing User_Score and Critic_Score with median
df['User_Score'] = df['User_Score'].fillna(df['User_Score'].median())
df['Critic_Score'] = df['Critic_Score'].fillna(df['Critic_Score'].median())

# Fill missing User_Count and Critic_Count with median
df['User_Count'] = df['User_Count'].fillna(df['User_Count'].median())
df['Critic_Count'] = df['Critic_Count'].fillna(df['Critic_Count'].median())

# Fill missing Rating with "Unknown"
df['Rating'] = df['Rating'].fillna("Unknown")

# Drop rows where Year_of_Release is missing
df = df.dropna(subset=['Year_of_Release'])

print("\nMissing values after cleaning:")
print(df.isnull().sum())

df.to_csv("outputs/vgames_cleaned.csv", index=False)
print("Cleaned dataset saved as vgames_cleaned.csv")

# --- Descriptive Statistics ---

# Overall summary for numeric columns
print("\nDescriptive statistics for numeric columns:")
print(df.describe())

# Count unique values in key categorical columns
print("\nNumber of unique Platforms:", df['Platform'].nunique())
print("\nNumber of unique Genres:", df['Genre'].nunique())
print("\nNumber of unique Publishers:", df['Publisher'].nunique())
print("\nNumber of unique Ratings:", df['Rating'].nunique())

# Most common categories
print("\nTop 5 Platforms:")
print(df['Platform'].value_counts().head())

print("\nTop 5 Genres:")
print(df['Genre'].value_counts().head())

print("\nTop 5 Publishers:")
print(df['Publisher'].value_counts().head())

print("\nRating Distribution:")
print(df['Rating'].value_counts().head())

# Regional and global sales summary
print("\nTotal Sales by Region:")
print(df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum())

print("\nAverage Sales by Region:")
print(df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].mean())

# Save descriptive stats to CSV
df.describe().to_csv("Outputs/descriptive_statistics.csv")

# --- Explanatory Visualisations ---
sns.set(style="whitegrid")

# Number of games released per year
plt.figure(figsize=(12, 6))
sns.countplot(x="Year_of_Release", data=df, color="skyblue")
plt.xticks(rotation=90)
plt.title("Number of Games Released per Year")
plt.xlabel("Year")
plt.ylabel("Number of Games")
plt.tight_layout()
plt.show()

# Top 10 Platforms by Global Sales
platform_sales = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=platform_sales.index, y=platform_sales.values, palette="viridis")
plt.title("Top 10 Platforms by Global Sales")
plt.xlabel("Platform")
plt.ylabel("Global Sales (millions)")
plt.show()

# Top 10 Genres by Global Sales
genre_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=genre_sales.index, y=genre_sales.values, palette="plasma")
plt.title("Top 10 Genres by Global Sales")
plt.xlabel("Genre")
plt.ylabel("Global Sales (millions)")
plt.show()

# Regional Sales Comparison
region_sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
plt.figure(figsize=(8, 6))
sns.barplot(x=region_sales.index, y=region_sales.values, palette="Set2")
plt.title("Regional Sales Distribution")
plt.xlabel("Region")
plt.ylabel("Total Sales (millions)")
plt.show()

# Critic vs User Scores
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Critic_Score'], label="Critic Score", fill=True, color="blue")
sns.kdeplot(df['User_Score'], label="User Score", fill=True, color="green")
plt.title("Distribution of Critic vs User Scores")
plt.xlabel("Score (0-100)")
plt.ylabel("Density")
plt.legend()
plt.show()

# Correlation matrix
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix for Numerical Features")
plt.show()

# Critic vs User Scores
plt.figure(figsize=(8, 6))
sns.scatterplot(x="Critic_Score", y="User_Score", data=df, alpha=0.5)
plt.title("Critic Score vs User Score")
plt.xlabel("Critic Score (0-100)")
plt.ylabel("User Score (0-100)")
plt.show()

# Scores vs Global Sales
plt.figure(figsize=(8, 6))
sns.scatterplot(x="Critic_Score", y="Global_Sales", data=df, alpha=0.5, color="blue", label="Critic Score")
sns.scatterplot(x="User_Score", y="Global_Sales", data=df, alpha=0.5, color="green", label="User Score")
plt.title("Sales vs Scores")
plt.xlabel("Score (0-100)")
plt.ylabel("Global Sales (millions)")
plt.legend()
plt.show()

# Genre Sales Over Time
# Group by Year and Genre
genre_trends = df.groupby(["Year_of_Release", "Genre"])["Global_Sales"].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=genre_trends, x="Year_of_Release", y="Global_Sales", hue="Genre")
plt.title("Global Sales Trends by Genre Over Time")
plt.xlabel("Year")
plt.ylabel("Global Sales (millions)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Top Publishers Impact
publisher_sales = df.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=publisher_sales.values, y=publisher_sales.index, palette="magma")
plt.title("Top 10 Publishers by Global Sales")
plt.xlabel("Global Sales (millions)")
plt.ylabel("Publisher")
plt.show()

# Sales Prediction & Score Influence
corr_matrix = df[['Global_Sales', 'Critic_Score', 'User_Score']].corr()
print(corr_matrix['Global_Sales'])

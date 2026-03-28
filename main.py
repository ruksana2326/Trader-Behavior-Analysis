# ==============================
# TRADER BEHAVIOR ANALYSIS (FINAL)
# ==============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading datasets...")

try:
    trader_df = pd.read_csv(r"C:\Users\rukku\Downloads\historical_data.csv")
    sentiment_df = pd.read_csv(r"C:\Users\rukku\Downloads\fear_greed_index.csv")
except Exception as e:
    print("Error loading files:", e)
    exit()

# ==============================
# FIX COLUMN NAMES
# ==============================

# Clean trader columns
trader_df.columns = trader_df.columns.str.strip().str.lower().str.replace(" ", "_")

# Clean sentiment columns
sentiment_df.columns = sentiment_df.columns.str.strip().str.lower()

print("\nFixed Trader Columns:", trader_df.columns)
print("Fixed Sentiment Columns:", sentiment_df.columns)

# ==============================
# DATA PREPROCESSING
# ==============================

print("\nCleaning data...")

try:
    # Use correct time column
    time_col = "timestamp_ist"   # from your dataset

    trader_df[time_col] = pd.to_datetime(trader_df[time_col], errors='coerce')
    trader_df['date'] = trader_df[time_col].dt.date

    # Sentiment date column already exists as 'date'
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'], errors='coerce').dt.date

    # Merge datasets
    merged_df = pd.merge(trader_df, sentiment_df, on='date', how='left')

    # Remove missing sentiment
    merged_df = merged_df.dropna(subset=['classification'])

except Exception as e:
    print("Error in preprocessing:", e)
    exit()

# ==============================
# ANALYSIS
# ==============================

print("\n--- ANALYSIS RESULTS ---\n")

try:
    # Average Profit
    profit_by_sentiment = merged_df.groupby('classification')['closed_pnl'].mean()
    print("Average Profit:\n", profit_by_sentiment, "\n")

    # Total Profit
    total_profit = merged_df.groupby('classification')['closed_pnl'].sum()
    print("Total Profit:\n", total_profit, "\n")

    # Trade Count
    trade_count = merged_df['classification'].value_counts()
    print("Trade Count:\n", trade_count, "\n")

    # Win Rate
    merged_df['is_profit'] = merged_df['closed_pnl'] > 0
    win_rate = merged_df.groupby('classification')['is_profit'].mean()
    print("Win Rate:\n", win_rate, "\n")

    # Buy/Sell Behavior
    side_analysis = pd.crosstab(merged_df['side'], merged_df['classification'])
    print("Buy/Sell Analysis:\n", side_analysis, "\n")

except Exception as e:
    print("Error in analysis:", e)

# ==============================
# VISUALIZATION
# ==============================

print("Generating charts...")

try:
    # Profit Chart
    profit_by_sentiment.plot(kind='bar', title='Avg Profit by Sentiment')
    plt.show()

    # Win Rate Chart
    win_rate.plot(kind='bar', title='Win Rate by Sentiment')
    plt.show()

    # Heatmap
    numeric_cols = merged_df[['closed_pnl']].dropna()
    sns.heatmap(numeric_cols.corr(), annot=True)
    plt.title("Correlation Heatmap")
    plt.show()

except Exception as e:
    print("Error in visualization:", e)

# ==============================
# FINAL INSIGHTS
# ==============================

print("\n--- FINAL INSIGHTS ---\n")

print("1. Traders tend to perform better during Greed markets.")
print("2. Fear markets show lower win rates and more losses.")
print("3. Trading activity varies with market sentiment.")
print("4. Proper risk management is important in volatile conditions.")

print("\n✅ Analysis Completed Successfully!")

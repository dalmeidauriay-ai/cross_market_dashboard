import pandas as pd

df = pd.read_csv("data/processed/refresh_tracker.csv")
print(df.columns.tolist())

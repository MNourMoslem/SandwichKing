import pandas as pd

df = pd.read_csv('Data\\Discounts.csv')
df = df.drop(['Unnamed: 0'], axis=1)
df['Discount State'] = ['Unused'] * len(df)
df.to_csv('Data\\Discounts.csv')
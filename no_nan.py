from pandas import read_csv

data = read_csv("data.csv")
data.dropna(inplace=True)
data.to_csv("data.csv")
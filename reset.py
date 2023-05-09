from pandas import read_csv, DataFrame

data = read_csv("data copy.csv").drop(columns=["Unnamed: 0"])
empty = DataFrame(columns=data.columns)

data.to_csv("data.csv")
empty.to_csv("liked.csv")
empty.to_csv("unliked.csv")

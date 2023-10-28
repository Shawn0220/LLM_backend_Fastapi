import pandas as pd

data = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
df = pd.DataFrame(data)
df.to_csv('tt.csv', index=False)

df.reindex(index=df.index[::-1])

df = df.iloc[::-1]
df = df.iloc[:, ::-1]
df.to_csv('new.csv', index=False)

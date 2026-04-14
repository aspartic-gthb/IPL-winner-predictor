import pandas as pd
import sqlite3

dbf0 = pd.read_parquet("stageddata/deliveries/IPL/chunk_0.parquet")
dbf1 = pd.read_parquet("stageddata/deliveries/IPL/chunk_1.parquet")
dbf2 = pd.read_parquet("stageddata/deliveries/IPL/chunk_2.parquet")

dbf = pd.concat([dbf0, dbf1, dbf2], ignore_index=True)

dmf0 = pd.read_parquet("stageddata/matches/IPL/chunk_0.parquet")
dmf1 = pd.read_parquet("stageddata/matches/IPL/chunk_1.parquet")
dmf2 = pd.read_parquet("stageddata/matches/IPL/chunk_2.parquet")

dmf = pd.concat([dmf0, dmf1, dmf2], ignore_index=True)
dpmf0 = pd.read_parquet("stageddata/peoplematchdata/IPL/chunk_0.parquet")
dpmf1 = pd.read_parquet("stageddata/peoplematchdata/IPL/chunk_1.parquet")
dpmf2 = pd.read_parquet("stageddata/peoplematchdata/IPL/chunk_2.parquet")

dpmf = pd.concat([dpmf0, dpmf1, dpmf2], ignore_index=True)



dfpm = pd.read_parquet("stageddata/playeridmap.parquet")
dft = pd.read_parquet("stageddata/teams.parquet")
dfp = pd.read_parquet("stageddata/players.parquet")

# conn = sqlite3.connect("ipl.db")

def shows(*args):
    for df in args:
        print(df.shape, df.columns, df.sample(n=3))

shows(dbf, dmf, dpmf, dfp, dft)
# conn.commit()
# conn.close()





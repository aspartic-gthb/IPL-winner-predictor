import pandas as pd
import glob


mfs = glob.glob("stageddata/matches/IPL/chunk_*.parquet")
dmf = pd.concat([pd.read_parquet(f) for f in mfs], ignore_index=True)
dft = pd.read_parquet("stageddata/teams.parquet")


tnm = {
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
    # 'Deccan Chargers': 'Sunrisers Hyderabad' # we can
}


dft['team_id_str'] = dft['team_id'].astype(str).str.replace('.0', '', regex=False).str.strip()
i2n = dict(zip(dft['team_id_str'], dft['name']))

def normalize_to_name(series):
    s = series.astype(str).str.replace('.0', '', regex=False).str.strip()

    mnasme = s.map(i2n).fillna(s)
    return mnasme.replace(tnm)

dmf['t1_name'] = normalize_to_name(dmf['team1id'])
dmf['t2_name'] = normalize_to_name(dmf['team2id'])
dmf['w_name'] = normalize_to_name(dmf['winner'])

def gts(df, n):
    t_name = 't1_name' if n == 1 else 't2_name'
    o_name = 't2_name' if n == 1 else 't1_name'
    
    ####### suffixed columns
    t_score, o_score = f'team{n}score', f'team{2 if n==1 else 1}score'
    t_wick, o_wick = f'team{n}wickets', f'team{2 if n==1 else 1}wickets'
    t_ball, o_ball = f'team{n}balls', f'team{2 if n==1 else 1}balls'

    temp = pd.DataFrame()
    temp['name'] = df[t_name]
    
    is_win = (df['w_name'] == df[t_name])
    is_loss = (df['w_name'] == df[o_name])
    is_shared = ((df['isTie'].astype(str) == '1') | (df['isDLS'].astype(str) == '1') | (~is_win & ~is_loss))
    
    temp['is_win'], temp['is_loss'], temp['is_shared'] = is_win.astype(int), is_loss.astype(int), is_shared.astype(int)
    temp['points'] = (temp['is_win'] * 2) + (temp['is_shared'] * 1)
    
    # NRR math
    rs, rc = pd.to_numeric(df[t_score], errors='coerce').fillna(0), pd.to_numeric(df[o_score], errors='coerce').fillna(0)
    tw, ow = pd.to_numeric(df[t_wick], errors='coerce').fillna(0), pd.to_numeric(df[o_wick], errors='coerce').fillna(0)
    tb, ob = pd.to_numeric(df[t_ball], errors='coerce').fillna(0), pd.to_numeric(df[o_ball], errors='coerce').fillna(0)
    
    temp['r_s'], temp['r_c'] = rs, rc
    temp['b_f'], temp['b_b'] = tb.where(tw < 10, 120), ob.where(ow < 10, 120)
    
    return temp


combined = pd.concat([gts(dmf, 1), gts(dmf, 2)])

table = combined.groupby('name').agg(
    Mat=('points', 'count'),
    Won=('is_win', 'sum'),
    Lost=('is_loss', 'sum'),
    Tied_NR=('is_shared', 'sum'),
    Pts=('points', 'sum'),
    RS=('r_s', 'sum'),
    BF=('b_f', 'sum'),
    RC=('r_c', 'sum'),
    BB=('b_b', 'sum')
).reset_index()

table['NRR'] = ((table['RS'] / (table['BF'] / 6)) - (table['RC'] / (table['BB'] / 6))).round(3)

print(table[['name', 'Mat', 'Won', 'Lost', 'Tied_NR', 'Pts', 'NRR']].sort_values(by=['Pts', 'NRR'], ascending=False).to_string(index=False))
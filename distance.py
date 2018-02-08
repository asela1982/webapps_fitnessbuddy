def closestBuddies():

    from geopy.distance import vincenty
    import pandas as pd
    import sqlite3
    
    df  = pd.read_sql(sql='SELECT * FROM fitness;',con= sqlite3.connect("db/fitness.sqlite"))

    latestBuddy = df['id'].idxmax(axis=0, skipna=True)
    latestBuddy = df.iloc[latestBuddy]['lat'],df.iloc[latestBuddy]['lng']

    df['results'] = ""

    for i,row in df.iterrows():
        temp = (row['lat'],row['lng'])
        df.loc[i,'results']=vincenty(latestBuddy, temp).miles

    df = df.sort_values(by='results')[1:5]
    return df
def closestBuddies():

    from geopy.distance import vincenty
    import pandas as pd

    # pymysql
    import pymysql
    # pymysql.install_as_MySQLdb()
    
    connection_string ="mysql://baff6e90fa899d:cc8fb5c8@us-cdbr-iron-east-05.cleardb.net/heroku_69314c212045914"
    engine = create_engine(connection_string)
    conn = engine.connect()
    df  = pd.read_sql(sql='SELECT * FROM fitness;',con=conn)

    latestBuddy = df['id'].idxmax(axis=0, skipna=True)
    latestBuddy = df.iloc[latestBuddy]['lat'],df.iloc[latestBuddy]['lng']

    df['results'] = ""

    for i,row in df.iterrows():
        temp = (row['lat'],row['lng'])
        df.loc[i,'results']=vincenty(latestBuddy, temp).miles

    df = df.sort_values(by='results')[1:5]
    return df
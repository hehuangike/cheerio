import pandas as pd

import models

df = pd.read_excel('京东商品评论.xlsx',sheet_name='Sheet1')
for i in range(0, len(df.index.values)):
    content = df.iloc[i,3]
    arthur = df.iloc[i,0]
    time_string = df.iloc[i,4]
    time = pd.to_datetime(time_string)
    link = df.iloc[i,10]

    models.collect.objects.create(
        content = content,
        author = arthur,
        time = time,
        link = link,
    )

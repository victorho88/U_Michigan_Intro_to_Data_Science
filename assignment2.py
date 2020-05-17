import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')

#Question 1
def answer_one():
    return df['Gold'].idxmax()

#Question 2
def answer_two():
    return (df['Gold']-df['Gold.1']).idxmax()

#Question 3
def answer_three():
    only_gold = df.where((df['Gold'] > 0) & (df['Gold.1'] > 0))
    only_gold = only_gold.dropna()
    return (abs((only_gold['Gold'] - only_gold['Gold.1']) / only_gold['Gold.2'])).idxmax()

#Question 4
def answer_four():
    df['Points'] = (df['Gold.2'] * 3 + df['Silver.2'] * 2 + df['Bronze.2'] * 1)
    return df['Points']
                       
#Question 5
census_df = pd.read_csv('census.csv')

def answer_five():
    new_df = census_df[census_df['SUMLEV'] == 50]
    return new_df.groupby('STNAME').count()['SUMLEV'].idxmax()

#Question 6
def answer_six():
    new_df = census_df[census_df['SUMLEV'] == 50]
    most_populous_counties = new_df.sort_values('CENSUS2010POP', ascending=False).groupby('STNAME').head(3)
    return most_populous_counties.groupby('STNAME').sum().sort_values('CENSUS2010POP', ascending=False).head(3).index.tolist()

#Question 7
def answer_seven():
    new_df = census_df[census_df['SUMLEV'] == 50]
    new_df = census_df.loc[[6, 9, 10, 11, 12, 13, 14]]
    new_df["MaxDiff"] = abs(new_df.max(axis=1) - new_df.min(axis=1))
    most_change = new_df.sort_values(by=["MaxDiff"], ascending = False)
    return most_change.iloc[0][0]

#Question 8
def answer_eight():
    counties = census_df[census_df['SUMLEV'] == 50]
    region = counties[(counties['REGION'] == 1) | (counties['REGION'] == 2)]
    washington = region[region['CTYNAME'].str.startswith("Washington")]
    grew = washington[washington['POPESTIMATE2015'] > washington['POPESTIMATE2014']]
    return grew[['STNAME', 'CTYNAME']]

import pandas as pd
import numpy as np

energy = pd.read_excel('/Users/victorho/Desktop/Assignment3/Energy Indicators.xls', skip_footer=38, skiprows=17, parse_cols='C:F')
energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy["Energy Supply"] *= 1000000
energy.replace('...', np.nan,inplace = True)
energy['Country'] = energy['Country'].replace({'China, Hong Kong Special Administrative Region':'Hong Kong','United Kingdom of Great Britain and Northern Ireland':'United Kingdom','Republic of Korea':'South Korea','United States of America':'United States','Iran (Islamic Republic of)':'Iran'})
energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")


world_bank = pd.read_csv('/Users/victorho/Desktop/Assignment3/world_bank.csv', skiprows=4)
world_bank['Country Name'] = world_bank['Country Name'].replace({"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"})

scimago = pd.read_excel('/Users/victorho/Desktop/Assignment3/scimagojr-3.xlsx')

print(scimago)

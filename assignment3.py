def answer_one():
    import pandas as pd
    import numpy as np
    energy = pd.read_excel('Energy Indicators.xls', skip_footer=38, skiprows=17, parse_cols='C:F')
    col_names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.columns = col_names
    energy.loc[energy['Energy Supply'] == '...'] = np.NaN
    energy[['Energy Supply', 'Energy Supply per Capita']] = energy[['Energy Supply', 'Energy Supply per Capita']].apply(pd.to_numeric)
    energy['Energy Supply'] = energy['Energy Supply']*10**6
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    energy['Country'] = energy['Country'].str.replace(r"([0-9]+)$","")
    replace_dict={"Republic of Korea": "South Korea",
                  "United States of America": "United States",
                  "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                  "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy['Country'].replace(to_replace=replace_dict, inplace=True)
    energy.reset_index()
    energy = energy.set_index('Country')
    
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    replace_dict = {"Korea, Rep.": "South Korea", 
                    "Iran, Islamic Rep.": "Iran",
                    "Hong Kong SAR, China": "Hong Kong"
                   }
    GDP['Country Name'].replace(to_replace=replace_dict, inplace=True)
    years_to_keep = np.arange(2006, 2016).astype(str)
    GDP = GDP[np.append(['Country Name'],years_to_keep)]
    GDP.reset_index()
    GDP = GDP.rename(columns={'Country Name': 'Country'})
    GDP = GDP.set_index('Country')
    
    ScimEn = pd.read_excel('scimagojr-3.xlsx', header=0)
    ScimEn.reset_index()
    ScimEn = ScimEn.set_index('Country')
    first_merge = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
    result = pd.merge(ScimEn, first_merge, how='outer', left_index=True, right_index=True)
    result = result.reset_index().dropna(thresh=result.shape[1]-10).set_index('Country')
    result = result.loc[result['Rank']<=15]
    return result
  
  def answer_two():
    import pandas as pd
    import numpy as np
    energy = pd.read_excel('Energy Indicators.xls', skip_footer=38, skiprows=17, parse_cols='C:F')
    col_names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.columns = col_names
    energy.loc[energy['Energy Supply'] == '...'] = np.NaN
    energy[['Energy Supply', 'Energy Supply per Capita']] = energy[['Energy Supply', 'Energy Supply per Capita']].apply(pd.to_numeric)
    energy['Energy Supply'] = energy['Energy Supply']*10**6
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    energy['Country'] = energy['Country'].str.replace(r"([0-9]+)$","")
    replace_dict={"Republic of Korea": "South Korea",
                  "United States of America": "United States",
                  "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                  "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy['Country'].replace(to_replace=replace_dict, inplace=True)
    energy.reset_index()
    energy = energy.set_index('Country')
    en_shape = energy.shape
    
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    replace_dict = {"Korea, Rep.": "South Korea", 
                    "Iran, Islamic Rep.": "Iran",
                    "Hong Kong SAR, China": "Hong Kong"
                   }
    GDP['Country Name'].replace(to_replace=replace_dict, inplace=True)
    years_to_keep = np.arange(2006, 2016).astype(str)
    GDP = GDP[np.append(['Country Name'],years_to_keep)]
    GDP.reset_index()
    GDP = GDP.rename(columns={'Country Name': 'Country'})
    GDP = GDP.set_index('Country')
    GDP_shape = GDP.shape
    
    ScimEn = pd.read_excel('scimagojr-3.xlsx', header=0)
    ScimEn.reset_index()
    ScimEn = ScimEn.set_index('Country')
    ScimEn_shape = ScimEn.shape
    
    first_merge = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
    result = pd.merge(ScimEn, first_merge, how='outer', left_index=True, right_index=True)
    #result = result.reset_index().dropna(thresh=result.shape[1]-10).set_index('Country')
    result = result.shape[0]-15
    
    return result
  
  def answer_three():
    import numpy as np
    Top15 = answer_one()
    years_to_keep = np.arange(2006, 2016).astype(str)
    Top15['avgGDP'] = Top15[years_to_keep].mean(axis=1)
    
    return Top15['avgGDP'].sort_values(ascending=False)
  
  def answer_four():
    Top15 = answer_one()
    Top15["AvgGDP"] = answer_three()
    Top15.sort_values("AvgGDP", ascending=False, inplace=True)
    final = Top15.iloc[5]['2015']
    initial = Top15.iloc[5]['2006']
    return abs(final - initial)
  
  def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()
  
  
def answer_six():
    Top15 = answer_one()
    return Top15['% Renewable'].argmax(), Top15['% Renewable'].max()
  
  def answer_seven():
    Top15 = answer_one()
    Top15["Ratio"] = Top15["Self-citations"] / Top15["Citations"]
    return Top15["Ratio"].argmax(), Top15["Ratio"].max()
  
  def answer_eight():
    Top15 = answer_one()
    Top15["Population"] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    final = Top15.sort_values("Population", ascending=False)
    return final.iloc[2].name
  
  def answer_nine():
    Top15 = answer_one()
    Top15["Population"] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15["Citable docs per Capita"] = Top15["Citable documents"] / Top15["Population"]
    return Top15["Citable docs per Capita"].corr(Top15['Energy Supply per Capita'])
  
  def answer_ten():
    Top15 = answer_one()
    reference = Top15["% Renewable"].median(axis=0)
    Top15["HighRenew"] = Top15.apply(lambda x: 1 if x["% Renewable"] > reference else 0, axis=1)
    Top15.sort_values(by='Rank', inplace=True)
    return Top15["HighRenew"] 
  
  def answer_eleven():
    import numpy as np
    import pandas as pd
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia',
                      'United States':'North America', 
                      'Japan':'Asia',
                      'United Kingdom':'Europe',
                      'Russian Federation':'Europe',
                      'Canada':'North America',
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    Top15 = Top15.reset_index()
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    result = Top15.copy()
    result = result[['Continent', 'PopEst']]
    result = result.groupby('Continent')['PopEst'].agg({'size': np.size,'sum': np.sum,'mean': np.mean,'std': np.std})
    idx = pd.IndexSlice

    return result

  
 def answer_twelve():
    import numpy as np
    import pandas as pd
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia',
                      'United States':'North America', 
                      'Japan':'Asia',
                      'United Kingdom':'Europe',
                      'Russian Federation':'Europe',
                      'Canada':'North America',
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    Top15 = Top15.reset_index()
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    Top15['% Renewable'] = pd.cut(Top15['% Renewable'], 5)
    result = Top15.groupby(['Continent', '% Renewable'])['Country'].count()
    result = result.reset_index()
    #result.drop('Country', axis=1, inplace=True)
    
    result = result.set_index(['Continent', '% Renewable'])
    return result['Country']
  
  def answer_thirteen():
    Top15 = answer_one()
    Top15["Population"] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    return Top15['Population'].apply(lambda x: '{0:,}'.format(x))

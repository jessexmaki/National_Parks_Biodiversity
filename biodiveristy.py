import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

species = pd.read_csv('species_info.csv',encoding='utf-8')
species.head()

observations = pd.read_csv('observations.csv', encoding='utf-8')
observations.head()

print(f"number of species:{species.scientific_name.nunique()}")

print(f"number of categories:{species.category.nunique()}")
print(f"categories:{species.category.unique()}")

species.groupby("category").size()

print(f"na values:{species.conservation_status.isna().sum()}")

print(species.groupby("conservation_status").size())

print(f"number of parks:{observations.park_name.nunique()}")
print(f"unique parks:{observations.park_name.unique()}")

print(f"number of observations:{observations.observations.sum()}")

species.fillna('No Intervention', inplace=True)
species.groupby("conservation_status").size()

conservationCategory = species[species.conservation_status != "No Intervention"]\
    .groupby(["conservation_status", "category"])['scientific_name']\
    .count()\
    .unstack()

conservationCategory

ax = conservationCategory.plot(kind = 'bar', figsize=(8,6), 
                               stacked=True)
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species");

species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected'])\
                        .scientific_name.nunique()\
                        .reset_index()\
                        .pivot(columns='is_protected',
                                      index='category',
                                      values='scientific_name')\
                        .reset_index()
category_counts.columns = ['category', 'not_protected', 'protected']

category_counts

category_counts['percent_protected'] = category_counts.protected / \
                                      (category_counts.protected + category_counts.not_protected) * 100

category_counts

from scipy.stats import chi2_contingency

contingency1 = [[30, 146],
              [75, 413]]
chi2_contingency(contingency1)

contingency2 = [[30, 146],
               [5, 73]]
chi2_contingency(contingency2)

from itertools import chain
import string

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

common_Names = species[species.category == "Mammal"]\
    .common_names\
    .apply(remove_punctuations)\
    .str.split().tolist()

common_Names[:6]

cleanRows = []

for item in common_Names:
    item = list(dict.fromkeys(item))
    cleanRows.append(item)
    
cleanRows[:6]

res = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in cleanRows))
res[:6]

words_counted = []

for i in res:
    x = res.count(i)
    words_counted.append((i,x))

pd.DataFrame(set(words_counted), columns =['Word', 'Count']).sort_values("Count", ascending = False).head(10)

species['is_bat'] = species.common_names.str.contains(r"\bBat\b", regex = True)

species.head(10)

species[species.is_bat]

bat_observations = observations.merge(species[species.is_bat])
bat_observations

bat_observations.groupby('park_name').observations.sum().reset_index()

obs_by_park = bat_observations.groupby(['park_name', 'is_protected']).observations.sum().reset_index()
obs_by_park

plt.figure(figsize=(16, 4))
sns.barplot(x=obs_by_park.park_name, y= obs_by_park.observations, hue=obs_by_park.is_protected)
plt.xlabel('National Parks')
plt.ylabel('Number of Observations')
plt.title('Observations of Bats per Week')
plt.show()
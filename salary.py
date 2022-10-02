from wordcloud import WordCloud, STOPWORDS

import data_loader
import pandas
import matplotlib.pyplot as plt
import re
from langdetect import detect
import numpy

suj_data_loader = data_loader.StartUpJobsDataLoader()
suj_data_loader.load_detail_data()

plt.style.use('grayscale')

def get_level(row):
    levels = []
    if row["junior"]:
        levels.append("jun")
    if row["medior"]:
        levels.append("med")
    if row["senior"]:
        levels.append("sen")
    if len(levels) == 0:
        levels.append("N/A")
    elif len(levels) == 3:
        levels.remove("med")
    return "-".join(levels)

data = suj_data_loader.data
data["has_salary"] = ~data["salary"].isna()
data = data.dropna(subset="salary")
level_column_expanded = data["salary"].apply(pandas.Series)
data = data.merge(right=level_column_expanded, left_index=True, right_index=True)
data["diff"] = data["max"] - data["min"]
data["diff_rel"] = (data["max"] - data["min"]) / data["min"]
level_column_expanded = data["level"].apply(pandas.Series)
data = data.merge(right=level_column_expanded, left_index=True, right_index=True)
data["level"] = data.apply(get_level, axis=1)
# print(data[["min", "max", "diff", "level"]])
data_plot = pandas.DataFrame(data.groupby("level")[["diff_rel", "diff", "min", "max"]].median()).reset_index()
data_plot = data_plot.sort_values("min")
fig, ax = plt.subplots(figsize=(5.7, 3))
ax.barh(y=data_plot["level"], left=data_plot["min"], width=data_plot["max"]-data_plot["min"])
# data_plot.plot(kind="barh", left="min", height="max")
print(data_plot)

ax.set_xlabel('Salary in CZK')
fig.savefig('foo6.png', bbox_inches='tight')

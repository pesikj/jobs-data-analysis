import data_loader
import pandas
import matplotlib.pyplot as plt

suj_data_loader = data_loader.StartUpJobsDataLoader()
suj_data_loader.load_detail_data()
data = suj_data_loader.data
plt.style.use('grayscale')

level_column_expanded = data["level"].apply(pandas.Series)
data = data.merge(right=level_column_expanded, left_index=True, right_index=True)
data = data.explode("skills")
data["skills"] = data["skills"].replace({"Communication Skills": "Comm. Skills", "Project Management": "Proj. Mgnt", "Online Marketing": "Online Mkt", "Sales Management": "Sales Mgnt"})
skill_column_flat_merged_grouped = pandas.DataFrame(data.groupby("skills")[["junior", "medior", "senior"]].sum())
skill_column_flat_merged_grouped["total"] = skill_column_flat_merged_grouped["junior"] + skill_column_flat_merged_grouped["senior"] + skill_column_flat_merged_grouped["medior"]
skill_column_flat_merged_grouped = skill_column_flat_merged_grouped.sort_values("total", ascending=False)
print(skill_column_flat_merged_grouped.head(20))

# skill_column_flat_merged_grouped = skill_column_flat_merged_grouped[~skill_column_flat_merged_grouped.index.isin(["Project Management", "Communication Skills", "Online Marketing", "Sales Management"])]
# skill_column_flat_merged_grouped = skill_column_flat_merged_grouped.set_index("skills")

ax = skill_column_flat_merged_grouped.head(20)[["junior", "medior", "senior"]].plot(kind="bar", figsize=(5.7, 3))
ax.set_xlabel('Required Skills')
ax.set_ylabel('Count of Advertisements')
plt.savefig('foo4.png', bbox_inches='tight')

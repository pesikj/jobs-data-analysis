import data_loader
import pandas
import matplotlib.pyplot as plt

suj_data_loader = data_loader.StartUpJobsDataLoader()
suj_data_loader.load_detail_data()
data = suj_data_loader.data

plt.style.use('grayscale')
data["technologies_count"] = data['technologies'].str.len()
data["technologies_count"] = data["technologies_count"].fillna(0)
# print(data["technologies_count"])
print(data.groupby("technologies_count").size())
print(data.shape)

# technologies = data.explode("technologies")
# technologies["technologies"] = technologies["technologies"].replace({"Google Analytics": "GA", "AWS (Amazon Web Services)": "AWS", "Microsoft Office": "Office"})
# technologies = technologies.groupby("technologies").size()
# technologies = pandas.DataFrame(technologies).sort_values(by=0, ascending=False)
#
# plt.figure(figsize=(3,4))
#
# ax = technologies.head(20).plot(kind="bar", figsize=(5.7, 3))
# ax.set_xlabel('Used Technologies')
# ax.set_ylabel('Count of Advertisements')
# ax.get_legend().remove()
#
# # plt.savefig('foo.png', bbox_inches='tight')
# plt.savefig('foo3.png', bbox_inches='tight')

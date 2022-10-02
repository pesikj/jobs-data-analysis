from wordcloud import WordCloud, STOPWORDS

import data_loader
import pandas
import matplotlib.pyplot as plt
import re
from langdetect import detect
test = detect("War doesn't show who's right, just who's left.")

suj_data_loader = data_loader.StartUpJobsDataLoader()
# suj_data_loader.load_detail_data(10)
data = suj_data_loader.data

data["description"] = data["description"].apply(lambda x: re.sub('<[^<]+?>', '', x))
data["lang"] = data["description"].apply(lambda x: detect(x))
data = data.groupby("lang").size()
print(data)


# data["language"] =

# data["name"] = data["name"].str.split()
# data = data.explode("name")
# data = data[~data["name"].isin(["pro", "&amp;", "do", "se", "na", "Hledáme", "for", "000", "CDN77", "ka", "týmu"])]
# data["name"] = data["name"].str.lower()
# data = data[data["name"].str.len() > 1]
# data = pandas.DataFrame(data.groupby("name").size()).sort_values(0, ascending=False)
# data.to_csv("positions.csv")


# data_name = " ".join(data["name"].tolist())
#
# wordcloud = WordCloud(background_color='white',
#                       stopwords=stopwords,
#                       min_font_size=10, colormap='Greys').generate(data_name)
#
# # plot the WordCloud image
# plt.figure(figsize=(5.9, 3), facecolor=None)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.tight_layout(pad=0)
#
# plt.savefig('foo5.png', bbox_inches='tight')

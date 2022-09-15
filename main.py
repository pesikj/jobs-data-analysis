import data_loader
import pandas
import matplotlib.pyplot as plt

suj_data_loader = data_loader.StartUpJobsDataLoader()
skill_column_flat = suj_data_loader.load_detail_data()

data = suj_data_loader.data
exploded = data.groupby("full_remote").size()
exploded = pandas.DataFrame(exploded)
exploded = exploded.sort_values(0, ascending=False)
exploded.to_excel("full_remote.xlsx")

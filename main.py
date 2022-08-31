import data_loader

suj_data_loader = data_loader.StartUpJobsDataLoader()
skill_column_flat = suj_data_loader.load_skills_data()
print(skill_column_flat.head())

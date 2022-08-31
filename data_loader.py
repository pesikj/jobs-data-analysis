from typing import List, Dict

import pandas
import requests
import json
from abc import ABC, abstractmethod
import os
import shutil
import time
import random
from requests_html import HTML
from collections import Counter


class DataLoader(ABC):
    @abstractmethod
    def _download_batch(self, page=1):
        pass

    @abstractmethod
    def _save_batch(self, data):
        pass

    @abstractmethod
    def load_saved_data(self):
        pass

    @abstractmethod
    def download_data_in_range(self, start, end, pause=10):
        pass

    @abstractmethod
    def download_record_detail(self, record_id):
        pass


class JobDescriptionDetail:
    def get_key_skills(self) -> Dict:
        with open(self.file_name, encoding='utf-8') as soubor:
            obsah = soubor.read()
        html = HTML(html=obsah)
        skills = None
        level = {"junior": 0, "medior": 0, "senior": 0}
        for el_div in html.find('div[class="mb-4"]'):
            el_div_list = el_div.find("dt")
            if len(el_div_list) == 0:
                continue
            el_dt = el_div_list[0]
            if el_dt.text.strip() == "Klíčové dovednosti":
                skills = el_div.find("dd")[0].text
                skills = skills.split(",")
                skills = [x.strip() for x in skills]
            if el_dt.text.strip() == "Požadovaná zkušenost":
                level_text = el_div.find("dd")[0].text
                if "juniory" in level_text:
                    level["junior"] = 1
                if "senior" in level_text:
                    level["senior"] = 1
                if "medior" in level_text or ("junior" in level_text and "senior" in level_text):
                    level["medior"] = 1
        # print(f"No skills found for {self.record_id}")
        return {"skills": skills, "level": level}

    def __init__(self, record_id: int):
        self.record_id = record_id
        self.record_detail_folder = "record_details/startup_jobs"
        target_directory = os.path.join(self.record_detail_folder, str(record_id))
        self.file_name = os.path.join(target_directory, f"{record_id}.html")


class StartUpJobsDataLoader(DataLoader):
    def _download_batch(self, page=1):
        link_value = f"https://www.startupjobs.cz/api/nabidky?page={page}"
        response = requests.get(link_value)
        response = json.loads(response.text)
        data = response["resultSet"]
        self._save_batch(data)

    def _save_batch(self, data):
        data = pandas.DataFrame(data)
        if os.path.exists(self.filename):
            saved_data = pandas.read_json(self.filename)
            data = pandas.concat([saved_data, data])
            data = data.drop_duplicates(subset="id")
        data.to_json(self.filename, orient="records")

    def download_data_in_range(self, start, end, pause=10):
        for i in range(start, end + 1):
            self._download_batch(i)
            print(f"Downloaded batch no. {i}")

    def load_saved_data(self) -> pandas.DataFrame:
        if not os.path.exists(self.filename):
            return pandas.DataFrame()
        data = pandas.read_json(self.filename)
        data = data.set_index("id")
        self.data = data
        return data

    def load_skills_data(self):
        skill_column = []
        index_column = []
        skill_column_flat = []
        for index, row in self.data.iterrows():
            job_description_detail = JobDescriptionDetail(index)
            skill_row = job_description_detail.get_key_skills()
            skill_column_flat.append(skill_row)
            if len(skill_row) > 0:
                skill_column.append(job_description_detail.get_key_skills())
                index_column.append(index)
        skill_series = pandas.Series(skill_column, index=index_column)
        self.data["skills"] = skill_series
        return pandas.DataFrame(skill_column_flat)

    def download_record_detail(self, record_id):
        url = self.data.loc[record_id, "url"]
        response = requests.get(url)
        target_directory = os.path.join(self.record_detail_folder, str(record_id))
        if os.path.exists(target_directory):
            shutil.rmtree(target_directory)
        os.mkdir(target_directory)
        with open(os.path.join(target_directory, f"{record_id}.html"), "w", encoding="utf-8") as f:
            f.write(response.text)

    def download_details_all_records(self):
        for index, _ in self.data.iterrows():
            self.download_record_detail(index)
            print(f"Detail record {index} downloaded")
            time.sleep(random.randint(5, 15))

    def __init__(self):
        self.filename = "start_up_jobs.json"
        self.record_detail_folder = "record_details/startup_jobs"
        self.data = self.load_saved_data()

from typing import List, Dict

import pandas
import requests
import json
from abc import ABC, abstractmethod
import os
import re
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


class JobDescriptionDetail:
    def get_details(self) -> Dict:
        with open(self.file_name, encoding='utf-8') as soubor:
            obsah = soubor.read()
        html = HTML(html=obsah)
        skills = []
        technologies = []
        benefits = []
        locality = []
        employment_types = []
        employment_form = []
        full_remote = False
        salary = None
        level = {"junior": 0, "medior": 0, "senior": 0}
        amount_re = re.compile(r"\d{3,6}-\d{3,6}")
        amount_re_val = re.compile(r"\d{3,6}")
        for el_div in html.find('div[class="flex pr-6 items-center"]'):
            if len(el_div.find('img[src="/build/web/images/icons/salary.svg"]')) > 0:
                text = el_div.find('span[class="pl-2"]')[0].text
                text = text.replace(" ", "").replace(" ", "")
                results = amount_re.findall(text)
                if len(results) == 1:
                    results_numbers = amount_re_val.findall(text)
                    results_numbers = [int(str(x).replace(" ", "")) for x in results_numbers]
                    salary = {"min": results_numbers[0], "max": results_numbers[1], "set_as": "interval"}
                    if "Kč/měsíc" in text:
                        salary["unit"] = "CZK/month"
                        break
                    elif "Kč/hodina" in text:
                        salary["unit"] = "CZK/hour"
                        break
                results = amount_re_val.findall(text)
                if len(results) == 1:
                    results_numbers = [int(str(x).replace(" ", "").replace(" ", "")) for x in results]
                    salary = {"val": results_numbers[0], "set_as": "value"}
                    if "Kč/měsíc" in text.replace(" ", "").replace(" ", ""):
                        salary["unit"] = "CZK/month"
                        break
                    elif "Kč/hodina" in text.replace(" ", "").replace(" ", ""):
                        salary["unit"] = "CZK/hour"
                        break
                    elif "€" not in text:
                        if results_numbers[0] > 1000:
                            salary["unit"] = "CZK/month"
                        else:
                            salary["unit"] = "CZK/hour"
                        break
                print(text, self.record_id)
        for el_div in html.find('div[class="mb-4"]'):
            if not full_remote:
                for dd_el in el_div.find("dd"):
                    if "Remote spolupráce" in dd_el.text:
                        full_remote = True
                        break
            el_div_list = el_div.find("dt")
            if len(el_div_list) == 0:
                continue
            el_dt = el_div_list[0]
            if el_dt.text.strip() == "Klíčové dovednosti":
                skills = el_div.find("dd")[0].text
                skills = skills.split(",")
                skills = [x.strip() for x in skills]
            elif el_dt.text.strip() == "Požadovaná zkušenost":
                level_text = el_div.find("dd")[0].text
                if "juniory" in level_text:
                    level["junior"] = 1
                if "senior" in level_text:
                    level["senior"] = 1
                if "medior" in level_text or ("junior" in level_text and "senior" in level_text):
                    level["medior"] = 1
            elif el_dt.text.strip() == "Technologie používané na pozici":
                technologies = el_div.find("dd")[0].text
                technologies = technologies.split(",")
                technologies = [x.strip() for x in technologies]
            elif el_dt.text.strip() == "Firemní benefity":
                benefits = [el_img_ben.attrs["alt"] for el_img_ben in el_div.find("dd")[0].find("img")]
            elif el_dt.text.strip() == "Lokalita":
                locality = el_div.find("dd")[0].text.replace("\n", "<br>").split("<br>")
                locality = [x.replace(", Česko", "") for x in locality]
                locality = [re.sub(r"\d{1}", "", x) for x in locality]
                locality = [x.strip() for x in locality]
            elif el_dt.text.strip() == "Úvazek":
                employment_types = el_div.find("dd")[0].text.split(",")
                employment_types = [x.strip() for x in employment_types]
            elif el_dt.text.strip() == "Forma spolupráce":
                employment_form = el_div.find("dd")[0].text.split(",")
                employment_form = [x.strip() for x in employment_form]
        # print(f"No skills found for {self.record_id}")
        return {"skills": skills, "level": level, "technologies": technologies, "benefits": benefits, "locality": locality, "employment_types": employment_types, "employment_form": employment_form, "full_remote": full_remote, "salary": salary}

    def download_record_detail(self):
        record_id = self.record_id
        url = self.record_url
        response = requests.get(url)
        target_directory = os.path.join(self.record_detail_folder, str(record_id))
        if os.path.exists(target_directory):
            shutil.rmtree(target_directory)
        os.mkdir(target_directory)
        with open(os.path.join(target_directory, f"{record_id}.html"), "w", encoding="utf-8") as f:
            f.write(response.text)

    def __init__(self, record_id, record_url):
        self.record_id = record_id
        self.record_url = record_url
        self.record_detail_folder = "record_details/startup_jobs"
        target_directory = os.path.join(self.record_detail_folder, str(record_id))
        self.file_name = os.path.join(target_directory, f"{record_id}.html")
        if not os.path.exists(self.file_name):
            self.download_record_detail()


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

    def load_detail_data(self, n=None):
        skill_column = []
        index_column = []
        skill_column_flat = []
        locality_column = []
        employment_type_column = []
        employment_form_column = []
        full_remote_column = []
        technology_column = []
        level_column = []
        salary_column = []
        counter = 0
        for index, row in self.data.iterrows():
            job_description_detail = JobDescriptionDetail(index, row["url"])
            skill_row = job_description_detail.get_details()
            skill_column.append(skill_row["skills"])
            locality_column.append(skill_row["locality"])
            employment_type_column.append(skill_row["employment_types"])
            employment_form_column.append(skill_row["employment_form"])
            full_remote_column.append(skill_row["full_remote"])
            technology_column.append(skill_row["technologies"])
            level_column.append(skill_row["level"])
            salary_column.append(skill_row["salary"])
            index_column.append(index)
            if n and n <= counter:
                break
            counter += 1
        skill_series = pandas.Series(skill_column, index=index_column)
        locality_series = pandas.Series(locality_column, index=index_column)
        employment_type_series = pandas.Series(employment_type_column, index=index_column)
        employment_form_series = pandas.Series(employment_form_column, index=index_column)
        full_remote_series = pandas.Series(full_remote_column, index=index_column)
        technology_series = pandas.Series(technology_column, index=index_column)
        level_series = pandas.Series(level_column, index=index_column)
        salary_series = pandas.Series(salary_column, index=index_column)
        self.data["skills"] = skill_series
        self.data["locality"] = locality_series
        self.data["employment_type"] = employment_type_series
        self.data["employment_form"] = employment_form_series
        self.data["full_remote"] = full_remote_series
        self.data["technologies"] = technology_series
        self.data["level"] = level_series
        self.data["salary"] = salary_series
        return pandas.DataFrame(skill_column_flat)

    def download_details_all_records(self):
        for index, _ in self.data.iterrows():
            self.download_record_detail(index)
            print(f"Detail record {index} downloaded")
            time.sleep(random.randint(5, 15))

    def __init__(self):
        self.filename = "start_up_jobs.json"
        self.record_detail_folder = "record_details/startup_jobs"
        self.data = self.load_saved_data()

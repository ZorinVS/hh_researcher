import os

CURRENT_FILE_PATH = os.path.abspath(__file__)
ROOT_PATH = os.path.join(os.path.dirname(CURRENT_FILE_PATH), "data")

HH_DATA_PATH = os.path.join(ROOT_PATH, "hh_data.json")
VACANCIES_JSON_PATH = os.path.join(ROOT_PATH, "vacancies.json")

if __name__ == "__main__":
    print(ROOT_PATH)
    print(HH_DATA_PATH)
    print(VACANCIES_JSON_PATH)

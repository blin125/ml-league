import requests
import os
import customErrors as cE
import concurrent.futures

class lolDataProcessor:
    def __init__(self, data_url=None, image_base_url=None):
        self.data_url = data_url or "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json"
        self.image_base_url = image_base_url or "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"
        self.data_list = [] 
        self.categories = {}

    def fetchJson(self):
        """ Fetches json data from Riot's API """

        response = requests.get(self.data_url)

        if response.status_code == 200:
            json_data = response.json()
            return json_data

        else:
            raise cE.FailFetch(f"Failed to fetch data. Status code: {response.status_code}")

    def fetch_champions(self, key):
        """ Fetches champion data from Riot's json """

        json_data = self.fetchJson()
        champions = json_data[key]
        self.data_list = list(champions.keys())
        
    def download_champion_image(self, champion, version):
        champion_folder = os.path.join("champions_img", champion)
        os.makedirs(champion_folder, exist_ok=True)
        champion_url = self.image_base_url + champion + '_' + version + '.jpg'
        image_path = os.path.join(champion_folder, f"{champion}_{version}.jpg")

        try:
            response = requests.get(champion_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                print(f"Champion {champion} version-- {version} successfully added")
            # else:
            #     print(f"Champion {champion} version-- {version} not added")
        except Exception as e:
            print(e)

    def downloadAllChampions(self, version):
        if not self.data_list:
            raise cE.EmptyChampionList("Champion list is empty. Check fetch_champions() first.")

        base_folder = "champions_img"
        os.makedirs(base_folder, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_champion_image, champion, version) for champion in self.data_list]
            concurrent.futures.wait(futures)

    def classification(self):

        json_data = self.fetchJson()

        for champion, tags in json_data["data"].items():
            for tag in tags.get('tags', []):
                if tag not in self.categories:
                    self.categories[tag] = []
                self.categories[tag].append(champion)

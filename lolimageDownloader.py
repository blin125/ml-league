import requests
import os
import customErrors as cE
import concurrent.futures

class LolImageDownloader:
    def __init__(self, data_url, image_base_url):
        self.data_url = data_url
        self.image_base_url = image_base_url
        self.champion_list = [] 

    def fetch_champions(self):
        """Fetches champion data from Riot's API."""

        response = requests.get(self.data_url)

        if response.status_code == 200:
            json_data = response.json()
            champions = json_data["data"]
            self.champion_list = list(champions.keys())

        else:
            raise cE.FailFetch(f"Failed to fetch data. Status code: {response.status_code}")
        
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
        if not self.champion_list:
            raise cE.EmptyChampionList("Champion list is empty. Check fetch_champions() first.")

        base_folder = "champions_img"
        os.makedirs(base_folder, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_champion_image, champion, version) for champion in self.champion_list]
            concurrent.futures.wait(futures)

''' Script to download the champion images based on the LolImageDownloader class'''
try:
    data_downloader = LolImageDownloader(
        "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json",
        "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"
    )
    data_downloader.fetch_champions()

    # The actual location of the images is not clear, so in this range, it will cover roughly 1700 skins
    for version in range(0,65):
        data_downloader.downloadAllChampions(str(version))

except cE.FailFetch as ff:
    print(f"Error: {ff}")
except cE.EmptyChampionList as ecl:
    print(f"Error: {ecl}")
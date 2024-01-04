import requests
import os
import customErrors

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
            raise customErrors.FailFetch(f"Failed to fetch data. Status code: {response.status_code}")
        
    def downloadAllChampions(self, version):
        """ Downloads all base images of the League Of Legends Champions """

        if not self.champion_list:
            raise customErrors.EmptyChampionList("Champion list is empty. Check fetch_champions() first.")

        base_folder = "champions_img"
        os.makedirs(base_folder, exist_ok = True)

        try:
            for champion in self.champion_list:
                champion_folder = os.path.join(base_folder, champion)
                os.makedirs(champion_folder, exist_ok = True)
                champion_url = self.image_base_url + champion + '_' + version + '.jpg'
                image_path = os.path.join(champion_folder, f"{champion}_{version}.jpg")
                try:
                    response = requests.get(champion_url)
                    response.raise_for_status()

                    with open(image_path, 'wb') as image_file:
                        image_file.write(response.content)

                except requests.exceptions.RequestException as e:
                    # Clean up downloaded images if any download fails
                    self.clean_up_images(base_folder, version)
                    raise RuntimeError(f"Transaction failed. Error downloading image for {champion}: {e}")

        except ValueError as ve:
            print(f"Error: {ve}")

    def clean_up_images(self, folder, version):
        """ Cleans up downloaded images in case of a failure."""
        for champion in self.champion_list:
            image_path = os.path.join(folder, champion, f"{champion}_{version}.jpg")
            if os.path.exists(image_path):
                os.remove(image_path)


try:
    data_downloader = LolImageDownloader(
        "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json",
        "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"
    )
    data_downloader.fetch_champions()
    version = '0'
    data_downloader.downloadAllChampions(version)

except customErrors.FailFetch as ff:
    print(f"Error: {ff}")
except customErrors.EmptyChampionList as ecl:
    print(f"Error: {ecl}")
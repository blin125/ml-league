import os
import customErrors as cE
import lolimageDownloader as lol
from sklearn.model_selection import train_test_split

lolHelper = lol.LolImageDownloader(
    "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json",
    "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"
)

json_data = lolHelper.fetchJson()

train_data = 'data\\train_data'
val_data = 'data\\validate_data'
category_folder = "categories"
champion_folder = "champions_img"
categories = {}

# def symb_links(data_folder, category, champion_list):
#     for champion_img in champion_list:
#         src_path = os.path.join(champion_folder, champion_img)
#         dest_path = os.path.join(data_folder, category, champion_img)
#         os.makedirs(os.path.dirname(dest_path), exist_ok=True)
#         os.symlink(src_path, dest_path)

for champion, tags in json_data["data"].items():
    for tag in tags.get('tags', []):
        if tag not in categories:
            categories[tag] = []
        categories[tag].append(champion)
        

for category in os.listdir(category_folder):
    category_path = os.path.join(category_folder, category)

    

    # champion_list = os.listdir(category_path)
    # print(champion_list) 
    # train_champ, val_champ = train_test_split(champion_list, test_size=0.2, random_state=42)

    # symb_links(train_data, category, train_champ)
    # symb_links(val_data, category, val_champ)

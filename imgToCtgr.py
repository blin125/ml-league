import os
from lolDataProcessor import lolDataProcessor as dataProc
import shutil

dataProc = dataProc()
dataProc.classification()
src_base_dir = os.path.join(os.getcwd(), 'champions_img')
dest_base_dir = os.path.join(os.getcwd(), 'tags')

for tag, champions in dataProc.categories.items():
    for chp in champions:
        src_champ_path = os.path.join(src_base_dir, chp)
        dest_tag_path = os.path.join(dest_base_dir, tag)
        os.makedirs(dest_tag_path, exist_ok=True)
        shutil.copytree(src_champ_path, os.path.join(dest_tag_path, chp))

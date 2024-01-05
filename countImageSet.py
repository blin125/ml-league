import os

def count_images(folder_path):
    try:
        files = os.listdir(folder_path)
        file_count = len([f for f in files])

        return file_count

    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
        return 0

folder_path = os.getcwd() + "\champions_img"
files = os.listdir(folder_path)
file_count = [count_images(folder_path + '\\' + f) for f in files]
size = len(file_count)
sum_skins = sum(file_count)
print(f'The number of Champions: {size}')
print(f'The number of skins: {sum_skins}')
print(f'The average number of skins per champion: {sum(file_count) / size}')
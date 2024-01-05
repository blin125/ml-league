from lolDataProcessor import lolDataProcessor as dataProc
import customErrors as cE;

def download_images(version_start, version_end):
    ''' Script to download the champion images based on the lolDataProcessor class'''
    try:
        data_proc = dataProc()
        data_proc.fetch_champions("data")

        # The actual location of the images is not clear, so in the range (0 - 65), it will cover roughly 1700+ skins
        for version in range(version_start, version_end):
            data_proc.downloadAllChampions(str(version))

    except cE.FailFetch as ff:
        print(f"Error: {ff}")
    except cE.EmptyChampionList as ecl:
        print(f"Error: {ecl}")

def show_classification():
    data_proc = dataProc()
    data_proc.classification()
    print(data_proc.categories)


download_images(0,1)
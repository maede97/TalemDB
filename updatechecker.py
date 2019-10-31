import requests
import config

def __download_updates():
    # get current path
    # download zip and unzip it
    # copy database
    pass

def __extract_zip():
    pass

def check_for_updates():
    print(config.CURRENT_VERSION)

    __download_updates()
    __extract_zip()

    # make request to json api of github (releases)
    # check with current tag
    # if new one found, download the new zip folder and extract it


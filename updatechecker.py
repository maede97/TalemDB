import requests
import config
import zipfile


def download_updates(url, target_path):
    # get current path
    # download zip and unzip it
    # copy database
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()

def extract_zip(file, directory):
    with zipfile.ZipFile(file,"r") as zip_ref:
        zip_ref.extractall(directory)

def check_versions(current, online):
    """ returns true if newest version is installed, otherwise false"""
    if(online == current):
        # we have the newest release
        return True
    else:
        latest_version = online[1:] # remove v in front
        latest_version = latest_version.split(".")
        curr = current[1:].split(".")
        latest_version = [int(i) for i in latest_version]
        curr = [int(i) for i in curr]
        for i in range(min(len(curr), len(latest_version))):
            if(latest_version[i] > curr[i]):
                return False
            elif(latest_version[i] < curr[i]):
                return None
        if(len(curr) < len(latest_version)):
            return False
        return True

def check_for_updates():
    r = requests.get("https://api.github.com/repos/maede97/TalemDB/releases/latest")

    if(r.ok):
        json = r.json()

        latest_version = json["tag_name"]

        if(check_versions(config.CURRENT_VERSION, latest_version)):
            pass
        else:
            download_updates(json['assets'][0]["browser_download_url"], json['assets'][0]['name'])
            extract_zip(json['assets'][0]['name'], latest_version)


import requests
import config
import zipfile
import shutil
import os

def move_files(folder):
    """downloaded zip contains a folder named TalemDB, where all files are, so copy all one up"""
    files = os.listdir(folder+"/TalemDB")
    for f in files:
        shutil.move(folder+"/TalemDB/"+f, folder)
    # delete empty folder
    os.rmdir(folder+"/TalemDB")
def download_updates(url, target_path):
    """download zip to target path"""
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()

def extract_zip(file, directory):
    """extract zip contents to directory"""
    with zipfile.ZipFile(file,"r") as zip_ref:
        zip_ref.extractall(directory)
    os.unlink(file)

def copy_database(directory):
    """ copy database to directory"""
    shutil.copy2(config.DATABASE, directory)

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

def download_and_export_updates():
    try:
        r = requests.get("https://api.github.com/repos/maede97/TalemDB/releases/latest")
        if(r.ok):
            json = r.json()

            latest_version = json["tag_name"]
            if(check_versions(config.CURRENT_VERSION, latest_version)):
                return False
            else:
                download_updates(json['assets'][0]["browser_download_url"], json['assets'][0]['name'])
                extract_zip(json['assets'][0]['name'], "../TalemDB_"+latest_version) # extract to folder one higher
                move_files("../TalemDB_"+latest_version)
                copy_database("../TalemDB_"+latest_version)
                return True
    except requests.exceptions.ConnectionError:
        return False
    

def check_for_updates():
    """ check for updates
    returns:
        - True: no update found
        - False: update was found
        - None: there was an error, check log
    """
    try:
        r = requests.get("https://api.github.com/repos/maede97/TalemDB/releases/latest")
        if(r.ok):
            json = r.json()

            latest_version = json["tag_name"]
            if(check_versions(config.CURRENT_VERSION, latest_version)):
                return True
            else:
                return False
    except requests.exceptions.ConnectionError:
        return None